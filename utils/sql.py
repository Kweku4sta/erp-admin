
from typing import Any

from utils import session


def add_object_to_database(item: Any) -> dict:
    """
    Add an item to the database
    Args:
        db (object): contain the session for the
                database operations
        item(Any): The item to insert
    returns:
        bool
    """
    with session.CreateDBSession() as database_session:
        database_session.add(item)
        database_session.commit()
        database_session.refresh(item)
        return item
    
def get_all_objects_from_database(model: Any) -> Any:
    """
    Get all items from the database
    Args:
        db (object): contain the session for the
                database operations
        model(Any): The model to query
    returns:
        Any
    """
    with session.CreateDBSession() as database_session:
        return database_session.query(model).all()
    
def get_object_by_id_from_database(model: Any, id: int) -> Any:
    """
    Get an item from the database by id
    Args:
        db (object): contain the session for the
                database operations
        model(Any): The model to query
        id(int): The id of the item to query
    returns:
        Any
    """
    with session.CreateDBSession() as database_session:
        return database_session.query(model).filter(model.id == id).first()
    

    def feel_free_to_create_more_functions():
        pass
    
