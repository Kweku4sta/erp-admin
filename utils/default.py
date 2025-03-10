from utils import session
from models.users import User
from models.admins import Admin
from models.roles import Role
from models.companies import Company
from utils.common import get_password_hash



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


default_sytem_admin = {
    "email": "sytemadmin@remcash.com",
    "full_name": "System Admin",
    "password": "password",

}

default_role = {
    "name": "system_admin",
    "description": "System Admin Role"
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
    




# create default role and system admin and assign to system admin

def create_default_system_admin():
    with session.CreateDBSession() as db_session:
        system_admin = db_session.query(Admin).filter(Admin.email == default_sytem_admin["email"]).first()
        if not system_admin:
            role = db_session.query(Role).filter(Role.name == default_role["name"]).first()
            if not role:
                role = Role(**default_role)
                db_session.add(role)
                db_session.commit()
                db_session.refresh(role)
            default_sytem_admin["role_id"] = role.id
            default_sytem_admin["password"] = get_password_hash(default_sytem_admin["password"])
            system_admin = Admin(**default_sytem_admin)
            db_session.add(system_admin)
            db_session.commit()
            db_session.refresh(system_admin)
            return system_admin
        return system_admin



    

    
