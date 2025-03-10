from concurrent.futures import ThreadPoolExecutor


from schemas.admins import AdminIn, RoleIn
from utils import sql
from models.admins import Admin
from models.roles import Role
from utils.common import get_password_hash, verify_password
from utils import session
from services.auditlog import AuditLogger
from utils.auth import AuthToken
from errors.exception import AuthException
from config.setting import settings





class AdminController:

    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_admin(admin: AdminIn) -> dict:
        """Create User
        This method creates a user
        """
        admin['password'] = get_password_hash(settings.DEFAULT_ADMIN_PASSWORD)
        admin = Admin(**admin)
        db_admin = sql.add_object_to_database(admin)
        AdminController.executor.submit(AuditLogger.log_activity,"SYSTEM ADMIN", f"Created the user:{admin.full_name}", "CREATE")
        # token = AuthToken.encode_auth_token_for_admin(db_admin)
        # return {"token": token, "admin": admin.json_data()}
        return admin.json_data()
    

    @staticmethod
    def add_role(role_data: RoleIn) -> dict:
        """Add Role
        This method adds a role
        """
        role = Role(**role_data)
        sql.add_object_to_database(role)
        AdminController.executor.submit(AuditLogger.log_activity, "SYSTEM ADMIN", f"Created the role:{role.name}", "CREATE")
        return role.json_data()
    

    def update_role(role_id: int, role_data: dict) -> dict:
        """Update Role
        This method updates a role

        Args:
            role_id (int): [description]
            role_data (dict): [description]
        """
        with session.CreateDBSession() as database_session:
            role = database_session.query(Role).filter(Role.id == role_id).first()
            if role.admins:
                raise AuthException(msg="Role is in use, cannot be updated", code=400)
            if role:
                for key, value in role_data.items():
                    setattr(role, key, value)
                database_session.commit()
                database_session.refresh(role)
                AdminController.executor.submit(AuditLogger.log_activity, "SYSTEM ADMIN", f"Updated the role:{role.name}", "UPDATE")
                return role.json_data()
            raise AuthException(msg="Role not found", code=404)
        
        

        
    @staticmethod
    def delete_role(role_id: int) -> dict:
        """Delete Role
        This method deletes a role

        Args:
            role_id (int): [description]
        """
        role = sql.get_object_by_id_from_database(Role, role_id)
        if role:
            if role.admins:
                raise AuthException(code=400, msg="Role is in use, cannot be deleted")
            sql.hard_delete_object_from_database(Role, role_id)
            AdminController.executor.submit(AuditLogger.log_activity, "SYSTEM ADMIN", f"Deleted the role:{role.name}", "DELETE")
            return role.json_data()
        raise AuthException(code=404, msg="Role not found")
    
    @staticmethod
    def get_all_roles() -> list:
        """Get All Roles
        This method gets all roles
        """
        roles = sql.get_all_objects_from_database(Role, False)
        return roles
        return [role.json_data() for role in roles]
    

    @staticmethod
    def get_role_by_id(role_id: int) -> dict:
        """Get Role
        This method gets a role

        Args:
            role_id (int): [description]
        """
        role = sql.get_object_by_id_from_database(Role, role_id)
        if role:
            return role.json_data()
        raise AuthException(code=404, msg="Role not found")
        
    
    @staticmethod
    def get_admin(admin_id: int) -> dict:
        """Get User
        This method gets a user

        Args:
            user_id (int): [description]

        Returns:
            dict: [description]

        """
        admin = sql.get_object_by_id_from_database(Admin, admin_id)
        if admin:
            return admin.json_data()
        raise AuthException(code=404, msg="Admin not found")
    


    @staticmethod
    def login(admin_data: dict) -> dict:
        """Login
        This method logs in an admin

        Args:
            admin_data (dict): [description]

        Returns:
            dict: [description]
        """

        admin = sql.check_if_instance_exist(Admin, 'email', admin_data['email'])
        if admin:
            if admin.reset_password:
                raise AuthException(code=401, msg="Reset password required")
            if verify_password(admin_data['password'], admin.password):
                print(admin.email, admin.role.name, "'try and encode token")
                token = AuthToken.encode_auth_token_for_admin(admin)
                return {"token": token, "admin": admin.json_data()}
            raise AuthException(code=401, msg="Invalid credentials")
        print("Invalid credentials- not found")
        raise AuthException(code=404, msg="Invalid credentials")
    


    @staticmethod
    def delete_admin(admin_id: int) -> dict:
        """Delete User
        This method deletes a user

        Args:
            user_id (int): [description]

        Returns:
            dict: [description]
        """
        admin = sql.hard_delete_object_from_database(Admin, admin_id)
        if admin:
            AdminController.executor.submit(AuditLogger.log_activity, "SYSTEM ADMIN", f"Deleted the user:{admin.full_name}", "DELETE")
            return {"message": "Admin deleted successfully", "staus": True}
        raise AuthException(code=404, msg="Admin not found")
    

    @staticmethod
    def get_all_admins():
        admins = sql.get_all_objects_from_database(Admin, False)
        return [admin.json_data() for admin in admins]
    


    @staticmethod
    def update_admin(admin_id: int, admin_data: dict) -> dict:
        """Update User
        This method updates a admin

        Args:
            admin_id (int): [description]
            admin_data (dict): [description]

        Returns:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            admin = db_session.query(Admin).filter(Admin.id == admin_id).first()
            if admin:
                if admin_data.get("password"):
                    admin_data["password"] = get_password_hash(admin_data["password"])
                for key, value in admin_data.items():
                    setattr(admin, key, value)
                db_session.commit()
                db_session.refresh(admin)
                AdminController.executor.submit(AuditLogger.log_activity, admin_data["created_by_id"], f"Updated the admin:{admin_data['full_name']}", "UPDATE")
                return admin.json_data()
            raise AuthException(code=404, msg="Admin not found")
        

    @staticmethod
    def reset_default_password(admin_id: int, admin_data: dict) -> dict:
        """Reset Default Password
        This method resets the default password

        Args:
            admin_id (int): [description]
            admin (dict): [description]

        Returns:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            admin = db_session.query(Admin).filter(Admin.id == admin_id).first()
            if admin:
                admin.password = get_password_hash(admin_data["password"])
                admin.reset_password = False
                db_session.commit()
                db_session.refresh(admin)
                return admin.json_data()
            raise AuthException(code=404, msg="Admin not found")



        
            
    





