def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body and "total" in body
    assert body["total"] >= 1
    assert len(body["items"]) >= 1


def test_search_notes_paginated_and_sorted(client):
    client.post("/notes/", json={"title": "Alpha", "content": "needle one"})
    client.post("/notes/", json={"title": "Beta", "content": "needle two"})
    client.post("/notes/", json={"title": "Gamma", "content": "other"})

    r = client.get("/notes/search/", params={"q": "needle", "page": 1, "page_size": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2
    assert body["page"] == 1
    assert body["page_size"] == 10

    r = client.get(
        "/notes/search/",
        params={"q": "needle", "sort": "title_asc", "page": 1, "page_size": 10},
    )
    assert r.status_code == 200
    titles = [n["title"] for n in r.json()["items"]]
    assert titles == ["Alpha", "Beta"]

    r = client.get("/notes/search/", params={"q": "needle", "page": 2, "page_size": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 2
    assert len(body["items"]) == 1
    assert body["page"] == 2


def test_search_case_insensitive(client):
    client.post("/notes/", json={"title": "Case", "content": "HelloWorld"})
    r = client.get("/notes/search/", params={"q": "helloworld"})
    assert r.status_code == 200
    assert r.json()["total"] >= 1


def test_update_and_delete_note(client):
    r = client.post("/notes/", json={"title": "Edit me", "content": "before"})
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "Edited", "content": "after"})
    assert r.status_code == 200
    assert r.json()["title"] == "Edited"
    assert r.json()["content"] == "after"

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Edited"

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_note_validation_errors(client):
    r = client.post("/notes/", json={"title": "", "content": "x"})
    assert r.status_code == 422

    r = client.put("/notes/99999", json={"title": "Nope", "content": "missing"})
    assert r.status_code == 404

    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_notes_pagination_boundaries(client):
    for i in range(3):
        client.post("/notes/", json={"title": f"N{i}", "content": f"c{i}"})

    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 1

    r = client.get("/notes/", params={"page": 5, "page_size": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert body["items"] == []

    r = client.get("/notes/", params={"page_size": 500})
    assert r.status_code == 422


def test_extract_endpoint(client):
    content = "Plan #project\n- [ ] write docs\n- TODO: ship it!\n#backend"
    r = client.post("/notes/", json={"title": "Extract", "content": content})
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/extract", params={"apply": False})
    assert r.status_code == 200
    body = r.json()
    assert "project" in body["hashtags"]
    assert "backend" in body["hashtags"]
    assert "write docs" in body["action_items"]
    assert body["applied"] is False
    assert body["created_action_item_ids"] == []

    r = client.post(f"/notes/{note_id}/extract", params={"apply": True})
    assert r.status_code == 200
    body = r.json()
    assert body["applied"] is True
    assert len(body["created_action_item_ids"]) >= 1

    r = client.get("/action-items/")
    assert r.status_code == 200
    descs = [i["description"] for i in r.json()["items"]]
    assert "write docs" in descs
