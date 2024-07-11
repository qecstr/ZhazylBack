import app.OAuth2Config as Auth
from app.schemas import AdminJson
from app.adminPanel.model import AdminModel
from sqlalchemy.orm import Session
from app.schemas import TokenDataForAdmins as TokenData
from app.adminPanel import route
def create_Admin(json: AdminJson, db: Session):
    admin = AdminModel(
        login=json.login,
        password=Auth.get_password_hash(json.password)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)



def check_admin(json: AdminJson, db:Session):
    return db.query(AdminModel).filter(AdminModel.login == json.login).first()
def get_admin(token_data:TokenData, db:Session):

    temp = db.query(AdminModel).filter(AdminModel.login == token_data.username).first()
    admin = AdminJson(login=temp.login, password=temp.password)
    return admin
