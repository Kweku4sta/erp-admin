
from schemas.users import UserIn
from utils import sql
from models.users import User
from models.companies import Company
class UserController:

    @staticmethod
    def create_user(user: UserIn) -> dict:
        """Create User
        This method creates a user
        """
        user = User(**user)
        sql.add_object_to_database(user)
        return user.json_data()
