from concurrent.futures import ThreadPoolExecutor


from fastapi import HTTPException
from fastapi_pagination import Page, Params

from schemas.users import UserIn
from utils import sql
from models.users import User
from models.companies import Company
from utils.common import get_password_hash
from utils import session
from services.auditlog import AuditLogger
from services.stream import KafkaStreamProducer
from config.setting import settings
from utils.filter import DynamicQuery




class UserController:

    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_user(user: UserIn) -> dict:
        """Create User
        This method creates a user
        """
        user['password'] = get_password_hash(settings.DEFAULT_USER_PASSWORD)
        user = User(**user)
        user=sql.add_object_to_database(user)
        if user.is_transact_portal_user:
            UserController.executor.submit(KafkaStreamProducer.send_json_data_to_topic, "remcashtransactuser", user.json_kafka())
        UserController.executor.submit(AuditLogger.log_activity, user.created_by_id, f"Created the user:{user.full_name}", "CREATE")
        return user.json_data()
    


    @staticmethod
    def change_user_transact_portal_status(user_id: int, status: bool) -> dict:
        """Change User Transact Portal Status
        This
        Args:
            user_id (int): [description]
            status (bool): [description]
        return:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            user = db_session.query(User).filter(User.id == user_id).first()
            if user:
                user.is_transact_portal_user = status
                db_session.commit()
                db_session.refresh(user)
                if user.status != status:
                    UserController.executor.submit(KafkaStreamProducer.send_json_data_to_topic, "remcashtransactuser", user.json_kafka())
                UserController.executor.submit(AuditLogger.log_activity, user.created_by_id, f"Changed the user:{user.full_name} transact portal status to {status}", "UPDATE")
                return user.json_data()
            raise HTTPException(status_code=404, detail="User not found")
            


    @staticmethod
    def get_user(user_id: int) -> dict:
        """Get User
        This method gets a user

        Args:
            user_id (int): [description]

        Returns:
            dict: [description]

        """
        user = sql.get_object_by_id_from_database(User, user_id)
        if user:
            return user.json_data()
        raise HTTPException(status_code=404, detail="User not found")
    
    @staticmethod
    def get_users(users_params) -> list:
        """Get Users
        This method gets all users
        Args:
            users_params (dict): users parameters

        Returns:
            list: [description]
        """
        with session.CreateDBSession() as db_session:
            users_query = DynamicQuery(db_session,users_params, User)
            users_query.add_joined_loads()
            return users_query.paginate()


    
    def update_user(user_id: int, user_data: dict) -> dict:
        """Update User
        This method updates a user

        Args:
            user_id (int): [description]
            user_data (dict): [description]

        Returns:
            dict: [description]
        """

        created_by_id = user_data["created_by_id"]
        user_data.pop("created_by_id")
        user_data = {key: value for key, value in user_data.items() if value is not None}

        user = sql.update_object_in_database(User, user_data, user_id)
        if user:
            if user.is_transact_portal_user:
                UserController.executor.submit(KafkaStreamProducer.send_json_data_to_topic, "remcashtransactuser", user.json_kafka())
            UserController.executor.submit(AuditLogger.log_activity, created_by_id, f"Updated the user:{user_data['full_name']}", "UPDATE")
            return user.json_data()
        raise HTTPException(status_code=404, detail="User not found")






        with session.CreateDBSession() as db_session:
            user = db_session.query(User).filter(User.id == user_id).first()
            if user:
                created_by_id = user_data["created_by_id"]
                user_data.pop("created_by_id")
                user_data = {key: value for key, value in user_data.items() if value is not None}
                for key, value in user_data.items():
                    setattr(user, key, value) 
                db_session.commit()
                db_session.refresh(user)
                if user.is_transact_portal_user:
                    UserController.executor.submit(KafkaStreamProducer.send_json_data_to_topic, "remcashtransactuser", user.json_kafka())
                UserController.executor.submit(AuditLogger.log_activity,created_by_id, f"Updated the user:{user_data['full_name']}", "UPDATE")
                return user.json_data()
            raise HTTPException(status_code=404, detail="User not found")
            

    @staticmethod
    def delete_user(user_id: int,created_by_id: int) -> dict:
        """Delete User
        This method deletes a user

        Args:
            user_id (int): [description]
            created_by_id (int): [description]

        Returns:
            dict: [description]
        """
        user = sql.hard_delete_object_from_database(User, user_id)
        if user:
            UserController.executor.submit(AuditLogger.log_activity, created_by_id, f"Deleted the user:{user_id}", "DELETE")
            return {"message": "User deleted successfully",
                    "status": True
                    }
        raise HTTPException(status_code=404, detail="User not found")
    

    @staticmethod
    def deactivate_user(user_id: int, created_by_id: int) -> dict:
        """Deactivate User
        This method deactivates a user

        Args:
            user_id (int): [description]
            created_by_id (int): [description]

        Returns:
            dict: [description]
        """
        user = sql.deactivate_object_in_database(User, user_id)
        if user:
            UserController.executor.submit(AuditLogger.log_activity, created_by_id, f"Deactivated the user:{user_id}", "DEACTIVATE")
            return {"message": "User deactivated successfully",
                    "status": True
                    }
        raise HTTPException(status_code=404, detail="User not found")
        
        
