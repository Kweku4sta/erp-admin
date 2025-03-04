from concurrent.futures import ThreadPoolExecutor


from fastapi import HTTPException

from schemas.users import UserIn
from utils import sql
from models.users import User
from models.companies import Company
from utils.common import get_password_hash
from utils import session
from services.auditlog import AuditLogger




class UserController:

    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_user(user: UserIn) -> dict:
        """Create User
        This method creates a user
        """
        user['password'] = get_password_hash(user['password'])
        user = User(**user)
        sql.add_object_to_database(user)
        UserController.executor.submit(AuditLogger.log_activity, user.created_by_id, f"Created the user:{user.full_name}", "CREATE")
        return user.json_data()


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
    def get_users() -> list:
        """Get Users
        This method gets all users

        Returns:
            list: [description]
        """
        users = sql.get_all_objects_from_database(User, True)
        return users
    

    @staticmethod
    def update_user(user_id: int, user_data: dict) -> dict:
        """Update User
        This method updates a user

        Args:
            user_id (int): [description]
            user_data (dict): [description]

        Returns:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            user = db_session.query(User).filter(User.id == user_id).first()
            if user:
                if user_data.get("password"):
                    user_data["password"] = get_password_hash(user_data["password"])
                for key, value in user_data.items():
                    setattr(user, key, value)
                db_session.commit()
                db_session.refresh(user)
                UserController.executor.submit(AuditLogger.log_activity, user_data["created_by_id"], f"Updated the user:{user_data['full_name']}", "UPDATE")
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
        
        
