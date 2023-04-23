import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemas.search_schema import SearchSettings
from db.repositories.search_db import get_search_from_db, add_search_to_db


def test_get_search_from_db_bad_request(session):
    result = get_search_from_db(search_id="random_bad_id", session = session)
    assert result is None


def test_add_search_to_db(data: dict, session):
    search_config = SearchSettings(**data["standard"])
    result = add_search_to_db(search_config, session = session)
    assert (type(result) == str) is True


def test_get_search_from_db(data: dict, session):
    search_config = SearchSettings(**data["standard"])
    search_id = add_search_to_db(search_config, session = session)

    result = get_search_from_db(search_id, session = session)
    assert SearchSettings.from_orm(result) == SearchSettings(**data["standard"])
