from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func, inspect
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Type, Any, Optional, List
from pydantic import BaseModel


class DynamicQuery:
    def __init__(self, db_session: Session, params: BaseModel, model: Type[Any], join_model: Optional[Type[Any]] = None):
        self.db_session = db_session
        self.params = params
        self.model = model
        self.join_model = join_model
        self.joins: List[str] = [] 

    def apply_filters(self, query):
        """
        Apply filters dynamically based on the query parameters.
        """
        params_dict = self.params.dict(exclude_none=True)

        for param, value in params_dict.items():
            if hasattr(self.model, param):
                column = getattr(self.model, param)
                query = self._apply_filter(query, column, value)
            elif self.join_model and hasattr(self.join_model, param):
                column = getattr(self.join_model, param)
                query = query.join(self.join_model)
                query = self._apply_filter(query, column, value)
            
        return query

    def _apply_filter(self, query, column, value):
        """
        Apply a filter to the query based on the column and value.
        """
        if isinstance(value, list):
            if isinstance(column.type, ARRAY):
                query = query.filter(column.contains(value))
        elif isinstance(value, str):
            query = query.filter(column.ilike(f"%{value}%"))
        elif isinstance(value, bool):
            query = query.filter(column == value)
        else:
            query = query.filter(column == value)

        return query

    def add_joined_loads(self, *relationships: str):
        """
        Add relationships to be loaded eagerly using joinedload.
        If no arguments are provided, join all relationships.
        """
        if not relationships:
            self.joins = self._get_all_relationships()
        else:
            self.joins.extend(relationships)
        return self

    def _get_all_relationships(self):
        """
        Dynamically detect all relationships of the model.
        """
        mapper = inspect(self.model)
        return [rel.key for rel in mapper.relationships]

    def apply_joined_loads(self, query):
        """
        Apply joinedload to the query for the specified relationships.
        """
        for relationship in self.joins:
            if hasattr(self.model, relationship):
                query = query.options(joinedload(getattr(self.model, relationship)))
        return query

    def paginate(self):
        """
        Paginate the results after applying filters and joined loads.
        """
        query = self.db_session.query(self.model)
        query = self.apply_filters(query)
        if self.joins:
            query = self.apply_joined_loads(query)
        
        return paginate(query, Params(page=self.params.page, size=self.params.size))