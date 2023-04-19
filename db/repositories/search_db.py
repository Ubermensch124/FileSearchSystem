from uuid import uuid4

from sqlalchemy.orm import Session
from pydantic import UUID4

from schemas.search_schema import SearchSettings
from db.models.search_table import Search


def add_search_to_db(search_config: SearchSettings, session: Session):
    new_search_settings = Search(
        search_id=str(uuid4()),
        text=search_config.text,
        file_mask=search_config.file_mask,
        size_value=search_config.size.value,
        size_operator=search_config.size.operator,
        creation_time_value=search_config.creation_time.value,
        creation_time_operator=search_config.creation_time.operator,
    )

    session.add(new_search_settings)
    session.commit()
    session.refresh(new_search_settings)
    
    return new_search_settings.search_id


def get_search_from_db(search_id: UUID4, session: Session):
    search_settings = session.query(Search).filter(Search.search_id == str(search_id)).one()
    return search_settings
