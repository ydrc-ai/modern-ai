def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1


def test_filter_action_items_by_completed(client):
    open_id = client.post("/action-items/", json={"description": "open task"}).json()["id"]
    done_id = client.post("/action-items/", json={"description": "done task"}).json()["id"]
    client.put(f"/action-items/{done_id}/complete")

    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == open_id
    assert body["items"][0]["completed"] is False

    r = client.get("/action-items/", params={"completed": True})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == done_id


def test_bulk_complete_action_items(client):
    ids = []
    for desc in ("a", "b", "c"):
        ids.append(client.post("/action-items/", json={"description": desc}).json()["id"])

    r = client.post("/action-items/bulk-complete", json={"ids": ids[:2]})
    assert r.status_code == 200
    updated = r.json()
    assert len(updated) == 2
    assert all(item["completed"] is True for item in updated)

    r = client.get("/action-items/", params={"completed": False})
    assert r.json()["total"] == 1
    assert r.json()["items"][0]["id"] == ids[2]


def test_bulk_complete_missing_ids_rolls_back(client):
    real_id = client.post("/action-items/", json={"description": "keep open"}).json()["id"]
    r = client.post("/action-items/bulk-complete", json={"ids": [real_id, 99999]})
    assert r.status_code == 404

    r = client.get("/action-items/", params={"completed": False})
    # real item should still be open because the transaction rolled back
    open_ids = [i["id"] for i in r.json()["items"]]
    assert real_id in open_ids


def test_action_items_pagination(client):
    for i in range(3):
        client.post("/action-items/", json={"description": f"item {i}"})

    r = client.get("/action-items/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2

    r = client.get("/action-items/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    assert len(r.json()["items"]) == 1
