import uuid
import requests

BASE_URL = "http://127.0.0.1:8000"


def unique_text(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_test_note(
    title: str = None,
    content: str = None,
    category: str = "Testing",
    tags: list[str] = None,
):
    """Helper function to create a note for tests."""

    if title is None:
        title = unique_text("Test Note")

    if content is None:
        content = "This is test content for pytest."

    if tags is None:
        tags = ["test"]

    note_data = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
    }

    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    return response.json()


############################################
# CRUD TESTS
############################################


def test_create_note():
    """Test creating a new note with POST /notes."""

    note_data = {
        "title": unique_text("Create Test"),
        "content": "This note was created during automated testing.",
        "category": "Testing",
   #     "tags": ["pytest", "create"],
    }

    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "created_at" in data
    assert data["title"] == note_data["title"]
    assert data["content"] == note_data["content"]
    assert data["category"] == "category"
    assert "pytest" in data["tags"]
    assert "create" in data["tags"]


def test_list_notes():
    """Test listing all notes with GET /notes."""

    response = requests.get(f"{BASE_URL}/notes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_note_by_id():
    """Test getting one specific note by ID."""

    created_note = create_test_note(
        title=unique_text("Get By ID"),
        content="This note is used to test GET by ID.",
        category="Testing",
        tags=["get", "single"],
    )

    note_id = created_note["id"]

    response = requests.get(f"{BASE_URL}/notes/{note_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == created_note["title"]
    assert data["content"] == created_note["content"]


def test_update_note():
    """Test full update with PUT /notes/{id}."""

    created_note = create_test_note(
        title=unique_text("Before PUT"),
        content="Old content",
        category="OldCategory",
        tags=["old"],
    )

    note_id = created_note["id"]

    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": "UpdatedCategory",
        "tags": ["updated", "put"],
    }

    response = requests.put(
        f"{BASE_URL}/notes/{note_id}",
        json=updated_data,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"
    assert data["category"] == "UpdatedCategory"
    assert "updated" in data["tags"]
    assert "put" in data["tags"]


def test_delete_note():
    """Test deleting a note with DELETE /notes/{id}."""

    created_note = create_test_note(
        title=unique_text("Delete Test"),
        content="This note will be deleted.",
        category="Testing",
        tags=["delete"],
    )

    note_id = created_note["id"]

    delete_response = requests.delete(f"{BASE_URL}/notes/{note_id}")

    assert delete_response.status_code == 204

    get_response = requests.get(f"{BASE_URL}/notes/{note_id}")

    assert get_response.status_code == 404


############################################
# FILTER TESTS
############################################


def test_filter_by_category():
    """Test filtering notes by category."""

    category = unique_text("Category")

    created_note = create_test_note(
        title=unique_text("Category Filter"),
        content="This note is used for category filter testing.",
        category=category,
        tags=["filter"],
    )

    response = requests.get(f"{BASE_URL}/notes?category={category}")

    assert response.status_code == 200

    notes = response.json()

    assert len(notes) >= 1

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert note["category"] == category


def test_filter_by_search():
    """Test search filter in title and content."""

    search_word = unique_text("meeting")

    created_note = create_test_note(
        title=f"Important {search_word}",
        content="This content is used for search testing.",
        category="Testing",
        tags=["search"],
    )

    response = requests.get(f"{BASE_URL}/notes?search={search_word}")

    assert response.status_code == 200

    notes = response.json()

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        text = f"{note['title']} {note['content']}".lower()
        assert search_word.lower() in text


def test_filter_by_tag():
    """Test filtering notes by tag."""

    tag = unique_text("urgent").lower()

    created_note = create_test_note(
        title=unique_text("Tag Filter"),
        content="This note is used for tag filter testing.",
        category="Testing",
        tags=[tag, "pytest"],
    )

    response = requests.get(f"{BASE_URL}/notes?tag={tag}")

    assert response.status_code == 200

    notes = response.json()

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert tag in note["tags"]


def test_combined_filters():
    """Test category + tag + search filters together."""

    category = unique_text("Work")
    tag = unique_text("urgent").lower()
    search_word = unique_text("meeting")

    created_note = create_test_note(
        title=f"Project {search_word}",
        content=f"This is an important {search_word} note.",
        category=category,
        tags=[tag, "combined"],
    )

    response = requests.get(
        f"{BASE_URL}/notes"
        f"?category={category}"
        f"&tag={tag}"
        f"&search={search_word}"
    )

    assert response.status_code == 200

    notes = response.json()

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert note["category"] == category
        assert tag in note["tags"]

        searchable_text = f"{note['title']} {note['content']}".lower()
        assert search_word.lower() in searchable_text


def test_date_filtering():
    """Test created_after and created_before filters."""

    created_note = create_test_note(
        title=unique_text("Date Filter"),
        content="This note is used for date filter testing.",
        category="Testing",
        tags=["date"],
    )

    response = requests.get(
        f"{BASE_URL}/notes" "?created_after=2000-01-01" "&created_before=2999-12-31"
    )

    assert response.status_code == 200

    notes = response.json()

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids


############################################
# ERROR TESTS
############################################


def test_create_note_missing_field():
    """Test validation error when required field is missing."""

    invalid_note = {
        "title": "Invalid Note",
        "category": "Testing",
        "tags": ["invalid"],
    }

    response = requests.post(f"{BASE_URL}/notes", json=invalid_note)

    assert response.status_code == 422


def test_get_nonexistent_note():
    """Test 404 when getting a non-existing note."""

    response = requests.get(f"{BASE_URL}/notes/999999999")

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data


def test_update_nonexistent_note():
    """Test 404 when updating a non-existing note."""

    updated_data = {
        "title": "Does not exist",
        "content": "This note does not exist.",
        "category": "Testing",
        "tags": ["error"],
    }

    response = requests.put(
        f"{BASE_URL}/notes/999999999",
        json=updated_data,
    )

    assert response.status_code == 404


def test_delete_nonexistent_note():
    """Test 404 when deleting a non-existing note."""

    response = requests.delete(f"{BASE_URL}/notes/999999999")

    assert response.status_code == 404


############################################
# DAY 3 HOMEWORK FEATURE TESTS
############################################


def test_notes_statistics():
    """Test GET /notes/stats endpoint."""

    create_test_note(
        title=unique_text("Stats Test"),
        content="This note is used for statistics testing.",
        category="StatsCategory",
        tags=["stats", "pytest"],
    )

    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total_notes" in data
    assert "by_category" in data
    assert "top_tags" in data
    assert "unique_tags_count" in data

    assert isinstance(data["total_notes"], int)
    assert isinstance(data["by_category"], dict)
    assert isinstance(data["top_tags"], list)
    assert isinstance(data["unique_tags_count"], int)

    assert data["total_notes"] >= 1
    assert "StatsCategory" in data["by_category"]


def test_list_categories():
    """Test GET /categories endpoint."""

    category = unique_text("CategoryList")

    create_test_note(
        title=unique_text("Category List Test"),
        content="This note is used for category list testing.",
        category=category,
        tags=["category"],
    )

    response = requests.get(f"{BASE_URL}/categories")

    assert response.status_code == 200

    categories = response.json()

    assert isinstance(categories, list)
    assert category in categories


def test_notes_by_category():
    """Test GET /categories/{category}/notes endpoint."""

    category = unique_text("CategoryNotes")

    created_note = create_test_note(
        title=unique_text("Notes By Category"),
        content="This note is used for notes by category testing.",
        category=category,
        tags=["category"],
    )

    response = requests.get(f"{BASE_URL}/categories/{category}/notes")

    assert response.status_code == 200

    notes = response.json()

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert note["category"] == category


def test_patch_note_title_only():
    """Test PATCH updates only the title."""

    created_note = create_test_note(
        title="Original Title",
        content="Original content",
        category="PatchCategory",
        tags=["patch", "original"],
    )

    note_id = created_note["id"]

    patch_data = {
        "title": "Patched Title Only",
    }

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json=patch_data,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "Patched Title Only"
    assert data["content"] == "Original content"
    assert data["category"] == "PatchCategory"
    assert "patch" in data["tags"]
    assert "original" in data["tags"]


def test_patch_multiple_fields():
    """Test PATCH updates several provided fields but not all fields."""

    created_note = create_test_note(
        title="Before Patch",
        content="Before content",
        category="BeforeCategory",
        tags=["before"],
    )

    note_id = created_note["id"]

    patch_data = {
        "title": "After Patch",
        "content": "After content",
    }

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json=patch_data,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "After Patch"
    assert data["content"] == "After content"
    assert data["category"] == "BeforeCategory"
    assert "before" in data["tags"]


############################################
# BONUS TESTS 
############################################


def test_list_tags():
    """Test GET /tags endpoint."""

    tag = unique_text("taglist").lower()

    create_test_note(
        title=unique_text("Tag List Test"),
        content="This note is used for tag list testing.",
        category="Testing",
        tags=[tag],
    )

    response = requests.get(f"{BASE_URL}/tags")

    assert response.status_code == 200

    tags = response.json()

    assert isinstance(tags, list)
    assert tag in tags


def test_notes_by_tag():
    """Test GET /tags/{tag}/notes endpoint."""

    tag = unique_text("tagnotes").lower()

    created_note = create_test_note(
        title=unique_text("Notes By Tag"),
        content="This note is used for notes by tag testing.",
        category="Testing",
        tags=[tag],
    )

    response = requests.get(f"{BASE_URL}/tags/{tag}/notes")

    assert response.status_code == 200

    notes = response.json()

    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert tag in note["tags"]


def test_unicode_note():
    """Test creating a note with unicode/special characters."""

    note_data = {
        "title": "Unicode Test äöü Привет 🚗",
        "content": "Testing unicode characters in API content.",
        "category": "Unicode",
        "tags": ["unicode", "special"],
    }

    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == note_data["title"]
    assert data["content"] == note_data["content"]
    assert data["category"] == "Unicode"
