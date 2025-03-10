from datetime import datetime, timedelta


import jwt
from fastapi import security,Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials


from errors.exception import AuthException
from utils.sql import check_if_instance_exist
from models.admins import Admin
from config.setting import settings



class AuthToken:
    """
    This class is used to provide
    authentication and authorization functionality
    for the third party connectivity
    """


    @staticmethod
    def encode_auth_token_for_admin(admin: dict) -> str:
        """
        Generates the auth token for the admin
        """
        try:
            payload = {
                "exp": datetime.utcnow()
                + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE),
                "iat": datetime.utcnow(),
                "sub": admin.email,
                'role': admin.role.name,
            }
            return jwt.encode(
                payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )
        except Exception as e:
            raise ValueError(e.args[0])

    @staticmethod
    def verify_auth_token(auth_token: str) -> str:
        print(auth_token)
        """
        Verifies the auth token
        """
        try:
            payload = jwt.decode(
                auth_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise AuthException(
                msg="Signature expired. Please log in again", code=403
            )
        except jwt.InvalidTokenError:
            raise AuthException(
                msg="Invalid token. Please log in again.", code=403
            )
        



    @staticmethod
    def verify_admin_token(token: str)-> dict:
        """Verify admin token and return user data"""
        admin_email = AuthToken.verify_auth_token(token)
        db_admin = check_if_instance_exist(Admin, 'email', admin_email)
        if not db_admin:
            raise AuthException(msg="Invalid token", code=404)
        return db_admin
    
    @staticmethod
    def verify_token_and_return_role(token: str) -> str:
        """Verify token and return role"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return {"role": payload["role"], "email": payload["sub"]}
        except jwt.ExpiredSignatureError:
            raise AuthException(msg="Signature expired. Please log in again", code=403)
        except jwt.InvalidTokenError:
            raise AuthException(msg="Invalid token. Please log in again.", code=403)
    
    
    


    
bearerschema = security.HTTPBearer()



def get_current_admin_and_role(credentials: HTTPAuthorizationCredentials = Security(bearerschema)):
    token = credentials.credentials
    return AuthToken.verify_token_and_return_role(token)

    