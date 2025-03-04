from typing import Dict
from concurrent.futures import ThreadPoolExecutor

from fastapi.exceptions import HTTPException

from schemas.kyc_accounts import KycAccountIn, KycAccountUpdate, KycParams
from utils import sql
from models.kyc_accounts import KycAccount
from utils import session
from services.auditlog import AuditLogger


class KycAccountController:

    executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def create_kyc_account(kyc_account_data: KycAccountIn) -> Dict[str, any]:
        """Create Kyc Account
        This method creates a kyc account
        """
        kyc_account = KycAccount(**kyc_account_data)
        sql.add_object_to_database(kyc_account)
        KycAccountController.executor.submit(AuditLogger.log_activity, kyc_account_data["created_by_id"], f"Created the kyc account:{kyc_account_data['name']}", "CREATE")
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
    def get_kyc_accounts(params: KycParams) -> Dict[str, any]:
        """Get Kyc Accounts
        This method gets all kyc accounts
        """
        kyc_accounts = sql.get_all_objects_from_database(KycAccount, True, params.page_size, params.page)
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
        with session.CreateDBSession() as db_session:
            kyc_account = db_session.query(KycAccount).filter(KycAccount.id == kyc_account_id).first()
            if kyc_account:
                for key, value in kyc_account_data.items():
                    setattr(kyc_account, key, value)
                db_session.commit()
                KycAccountController.executor.submit(AuditLogger.log_activity, kyc_account_data["created_by_id"], f"Updated the kyc account:{kyc_account_id}", "UPDATE")
                return kyc_account.json_data()
            raise HTTPException(status_code=404, detail="Kyc Account not found")