import pytest
import requests

from persons_table import create_app
from persons_table.models import (
    DatabaseHandler,
    Person,
    bulk_insert_into_db,
    db,
    get_API_response,
    serialize_API_data,
)
from tests.mock_json import mock_json

# ---------- Testing working with API(response is mocked) and Database functionality----------- #


@pytest.fixture
def app_and_client():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../tests/db_for_testing.db"
    with app.test_client() as client:
        yield app, client


class MockResponse:
    """To help mocking requests.get.json("""

    @staticmethod
    def json():
        return mock_json


def test_serialization_functionality_with_mock(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    return_from_API_json = get_API_response(1000)
    result = serialize_API_data(return_from_API_json["results"])
    assert type(result) is list
    for item in result:
        assert isinstance(item, Person)


def test_create_table_with_1000_entries(monkeypatch, app_and_client):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    app = app_and_client[0]
    with app.app_context():
        db.drop_all()
        DatabaseHandler.create_table()
        DatabaseHandler.rerecord_data(1000)
        assert DatabaseHandler.count_entries() == 1000


def test_bulk_insert_into_db(monkeypatch, app_and_client):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    app = app_and_client[0]
    with app.app_context():
        return_from_API_json = get_API_response(1000)
        input_for_db = serialize_API_data(return_from_API_json["results"])
        bulk_insert_into_db(input_for_db)
        assert DatabaseHandler.count_entries() == 2000


def test_get_all_records_query(app_and_client):
    app = app_and_client[0]
    with app.app_context():
        query = DatabaseHandler.all_records_query()
        assert query.count() == 2000
        assert isinstance(query.first(), Person)


def test_get_person_data(app_and_client):
    app = app_and_client[0]
    with app.app_context():
        person_data = DatabaseHandler.get_person_data(2)
        assert isinstance(person_data, Person)
        assert person_data.id == 2


def test_delete_person(app_and_client):
    app = app_and_client[0]
    with app.app_context():
        assert DatabaseHandler.count_entries() == 2000
        DatabaseHandler.delete_person(10)
        assert DatabaseHandler.count_entries() == 1999


def test_generate_random_person_id(app_and_client):
    app = app_and_client[0]
    with app.app_context():
        random_id = DatabaseHandler.generate_random_person_id()
        assert bool(DatabaseHandler.get_person_data(random_id))


# ------------ Testing Flask Rendering and Routing ---------------- #


def test_rendering_index_page(app_and_client):
    client = app_and_client[1]
    slash_page_rv = client.get("/")
    assert slash_page_rv.status_code == 200
    slash_index_page_rv = client.get("/index")
    assert slash_index_page_rv.status_code == 200
    slash_index_slash_1_page_rv = client.get("/index/1")
    assert slash_index_slash_1_page_rv.status_code == 200


def test_rendering_random_page(app_and_client):
    client = app_and_client[1]
    rv = client.get("/random", follow_redirects=True)
    assert rv.status_code == 200


def test_rendering_new_person_page(app_and_client):
    client = app_and_client[1]
    rv = client.get("/new_person", follow_redirects=True)
    assert rv.status_code == 200


def test_rendering_personal_page(app_and_client):
    client = app_and_client[1]
    rv = client.get("/person/15", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/person/16", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/person/23", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/person/42", follow_redirects=True)
    assert rv.status_code == 200


def test_rendering_edit_person_page(app_and_client):
    client = app_and_client[1]
    rv = client.get("/edit-person/15", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/edit-person/16", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/edit-person/23", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/edit-person/42", follow_redirects=True)
    assert rv.status_code == 200


def test_delete_person_functionality(app_and_client):
    client = app_and_client[1]
    app = app_and_client[0]
    with app.app_context():
        assert DatabaseHandler.count_entries() == 1999
    rv = client.get("/delete-person/15", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/delete-person/16", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/delete-person/23", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/delete-person/42", follow_redirects=True)
    assert rv.status_code == 200
    assert DatabaseHandler.count_entries() == 1995


# --------- test of API Response (response is not mocked) ----------- #
def test_API_response():
    result = get_API_response(10)
    assert isinstance(result, dict)
    assert bool(result)
