from typing import Any
import requests
from requests import Response
import base64

from passlib.context import CryptContext


from fastapi import UploadFile

from errors.exception import InternalProcessingError
from tools.log import Log




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

common_logger = Log(name=f"{__name__}")

HEADERS = {
    "Authorization": "Basic c2VydmljZV9rZXk6c2VjcmV0",
    "x-subscription-key": "subscription_key",
}

TIMEOUT = 6000
BLACKLIST_STATUS_CODES = (500, 403, 422, 401)


def raise_internal_processing_error(response: Response) -> None:
    """
    Raise InternalProcessingError
    """
    if response.status_code in BLACKLIST_STATUS_CODES:
        common_logger.error(
            f"{raise_internal_processing_error.__name__} - {response.text}"
        )
        raise InternalProcessingError(
            msg={"message": "Internal Processing Error, Please try again"}, code=500
        )


def send_request(method: str, url: str, data: dict[Any, Any]= None) -> requests.Response:
    """
    Send a request to the specified url with the specified data and headers.
    """
    try:
        response = requests.request(
            method,
            url,
            json=data,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        raise_internal_processing_error(response)
        return response
    except InternalProcessingError:
        raise InternalProcessingError(
            msg={"message": "Internal Processing Error, Please try again"}, code=500
        )
    except Exception as e:
        common_logger.error(f"{send_request.__name__} - {str(e.args[0])}")
        raise InternalProcessingError(
            msg={"message": "Internal Server Error"}, code=500
        )
    


def nia_verification(ghana_card: UploadFile, ghancard_pin:str) -> dict:
    """
    Verify NIA
    """
    try:
        image = ghana_card.file.read()
        data = {"image": image}
        url = "https://nia-verification.com"
        method = "POST"
        response = send_request(method, url, data)
        return response.json()
    except Exception as e:
        common_logger.error(f"{nia_verification.__name__} - {str(e.args[0])}")
        raise InternalProcessingError(
            msg={"message": "Internal Server Error"}, code=500
        )
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)




