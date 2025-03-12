from typing import Dict
from concurrent.futures import ThreadPoolExecutor

from fastapi.exceptions import HTTPException

from schemas.kyc_accounts import KycAccountIn, KycAccountUpdate, KycParams
from utils import sql
from models.kyc_accounts import KycAccount
from utils import session
from services.auditlog import AuditLogger
from utils.filter import DynamicQuery
from fastapi_pagination import Page


class KycAccountController:

    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_kyc_account(kyc_account_data: KycAccountIn) -> Dict[str, any]:
        """Create Kyc Account
        This method creates a kyc account
        """
        kyc_account = KycAccount(**kyc_account_data)
        kyc_account = sql.add_object_to_database(kyc_account)
        KycAccountController.executor.submit(AuditLogger.log_activity, kyc_account_data["created_by_id"], f"Created the kyc account:{kyc_account_data['account_type']}", "CREATE")
        return kyc_account.json_data()
    

    @staticmethod
    def get_kyc_account(kyc_account_id: int) -> Dict[str, any]:
        """Get Kyc Account
        This method gets a kyc account
        """
        kyc_account = sql.get_object_by_id_from_database(KycAccount, kyc_account_id)
        if kyc_account:
            return kyc_account.json_data()
        return []
    

    @staticmethod
    def get_kyc_accounts(params: KycParams) -> Page[KycAccount]:
        """Get Kyc Accounts
        This method gets all kyc accounts
        """
        with session.CreateDBSession() as db_session:
            kyc_accounts_query = DynamicQuery(db_session, params, KycAccount)
            kyc_accounts_query.add_joined_loads()
            kyc_accounts = kyc_accounts_query.paginate()
            return kyc_accounts

    
    @staticmethod
    def delete_kyc_account(kyc_account_id: int, created_by_id) -> Dict[str, any]:
        """Delete Kyc Account
        This method deletes a kyc account

        Args:
            kyc_account_id (int): [description]
            created_by_id ([type]): [description]
        
        Returns:
            Dict[str, any]: [description]
        """
        kyc_account = sql.hard_delete_object_from_database(KycAccount, kyc_account_id)
        if kyc_account:
            KycAccountController.executor.submit(AuditLogger.log_activity, created_by_id, f"Deleted the kyc account:{kyc_account_id}", "DELETE")
            return {"message": "Kyc Account deleted successfully",
                    "status": True
                    }
        raise HTTPException(status_code=404, detail="Kyc Account not found")
    

    @staticmethod
    def update_kyc_account(kyc_account_id: int, kyc_account_data: KycAccountUpdate) -> Dict[str, any]:
        """Update Kyc Account
        This method updates a kyc account
        """
        created_by_id = kyc_account_data["created_by_id"]
        kyc_account_data.pop("created_by_id")
        kyc_account_data = {k: v for k, v in kyc_account_data.items() if v is not None}
        kyc_account = sql.update_object_in_database(KycAccount, kyc_account_data, kyc_account_id)
        if kyc_account:
            KycAccountController.executor.submit(AuditLogger.log_activity, created_by_id, f"Updated the kyc account:{kyc_account.id} for {kyc_account.company.name}", "UPDATE")
            return kyc_account.json_data()
        raise HTTPException(status_code=404, detail="Kyc Account not found")

        