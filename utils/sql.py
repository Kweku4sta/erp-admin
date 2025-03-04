
from typing import Any, Union


from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import joinedload

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
    
def get_all_objects_from_database(model: Any, paginate_result: bool, per_page: int = None, size: int = None) -> Any:
    """
    Get all items from the database
    Args:
        db (object): contain the session for the
                database operations
        model(Any): The model to query
    returns:
        Any
    """
    # with session.CreateDBSession() as database_session:
        # if paginate_result:
        #     query =  database_session.query(model)
        #     return paginate(query,Params(per_page=per_page, size=size))
        # quer = database_session.query(model)
        # return paginate(quer, Params(per_page=per_page, size=size))
    with session.CreateDBSession() as database_session:
        query = database_session.query(model)
        if paginate_result:
            # query and join all the loads 
            query = query.options(joinedload('*'))
            return paginate(query, Params(per_page=per_page, size=size))
        return query.all()
    
def paginate_objects_from_database(model: Any, page: int, limit: int) -> Any:
    """
    Paginate items from the database
    Args:
        db (object): contain the session for the
                database operations
        model(Any): The model to query
        page(int): The page number
        limit(int): The number of items per page
    returns:
        Any
    """
    with session.CreateDBSession() as database_session:
        return database_session.query(model).paginate(page=page, per_page=limit)
    
def get_object_by_id_from_database(model: Any, id: int, join_loads: Union[str] = None) -> Any:
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
        if join_loads:
            return database_session.query(model).options(joinedload(join_loads)).filter(model.id == id).first()
        return database_session.query(model).filter(model.id == id).first()
    

    def feel_free_to_create_more_functions():
        pass

def hard_delete_object_from_database(model: Any, id: int) -> bool:
        """
        Hard delete an item from the database
        Args:
            db (object): contain the session for the
                    database operations
            model(Any): The model to query
            id(int): The id of the item to query
        returns:
            bool
        """
        with session.CreateDBSession() as database_session:
            item = database_session.query(model).filter(model.id == id).first()
            if item:
                database_session.delete(item)
                database_session.commit()
                return True
            return False
        
def update_object_in_database(model: Any, item: Any, id: int) -> Any:
        """
        Update an item in the database
        Args:
            model(Any): The model to query
            item(Any): The item to update
            data(dict): The data to update the item with
        returns:
            Any
        """
        with session.CreateDBSession() as database_session:
            db_item = database_session.get(model, id)
            if db_item:
                for key, value in item.items():
                    setattr(db_item, key, value)
                database_session.commit()
                return db_item
            return False
        


def deactivate_object_in_database(model: Any, id: int) -> Any:
        """
        Deactivate an item in the database
        Args:
            model(Any): The model to query
            id(int): The id of the item to deactivate
        returns:
            Any
        """
        with session.CreateDBSession() as database_session:
            item = database_session.query(model).filter(model.id == id).first()
            if item:
                item.is_active = False
                database_session.commit()
                return item
            return False

    
    
