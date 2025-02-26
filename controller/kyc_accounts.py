from typing import Dict

from schemas.kyc_accounts import KycAccountIn
from utils import sql
from models.kyc_accounts import KycAccount


class KycAccountController:

    @staticmethod
    def create_kyc_account(kyc_account_data: KycAccountIn) -> Dict[str, any]:
        """Create Kyc Account
        This method creates a kyc account
        """
        kyc_account = KycAccount(**kyc_account_data)
        sql.add_object_to_database(kyc_account)
        return kyc_account.json_data()