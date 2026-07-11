from backend.app.services.extract import extract_action_items, extract_hashtags


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


def test_extract_checkboxes_and_hashtags():
    text = """
    Sprint plan #backend #Frontend
    - [ ] write API tests
    - [ ] update docs
    - [x] already done should be ignored
    #backend
    """.strip()
    assert extract_hashtags(text) == ["backend", "frontend"]
    items = extract_action_items(text)
    assert items == ["write API tests", "update docs"]
