from utils import session
from models.users import User
from models.companies import Company



default_company = {
    "name": "Remcash",
    "email": "remcash@mail.com",
    "phone_number": "0700000000",
    "street": "Cantoment",
    "city": "Accra",
    "state": "Ghana",
    "postal_code": "00233",
    "nia_verification": True,
    "description": "This is the default company",
    "ghana_card_number": "123456789",
}


default_admin_for_company = {
    "email": "superadmin@gmail.com",	
    "full_name": "Super Admin",
    "password": "password",
    "is_authorizer": True,
    "flag": False
}


def create_default_company():
    with session.CreateDBSession() as db_session:
        company = Company(**default_company)
        db_session.add(company)
        db_session.commit()
        db_session.refresh(company)
        return company
    

def create_default_admin_for_company(company_id):
    with session.CreateDBSession() as db_session:
        default_admin_for_company["company_id"] = company_id
        admin = User(**default_admin_for_company)
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
        return admin
    

def create_default_data():
    with session.CreateDBSession() as db_session:
        company = db_session.query(Company).filter(Company.email == default_company["email"]).first()
        if not company:
            company = create_default_company()
            create_default_admin_for_company(company.id)
        return company
    
