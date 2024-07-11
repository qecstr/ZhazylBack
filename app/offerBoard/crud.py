from jose import jwt
from sqlalchemy.orm import Session
from app.offerBoard.models import OfferBoard
from app.schemas import offerBoardJson
from app.Profiles.crudClinicsProfile import getClinicsProfileByUser
from app import OAuth2Config as Auth

def create_offer(
        offer: offerBoardJson,
        db: Session,
        token: str
):
    decoded_token = Auth.decode_access_token(token)
    clinicsProfile = getClinicsProfileByUser(decoded_token,db)
    offer = OfferBoard(
        clinic_name = clinicsProfile.name,
        address = clinicsProfile.address ,
        worktime = offer.worktime,
        phone =  offer.phone,
        clinic_id =  clinicsProfile.id,
        text = offer.text
    )

    db.add(offer)
    db.commit()
    db.refresh(offer)


def getAll(db:Session):
    return db.query(OfferBoard).all()

def delete(offer:offerBoardJson ,db:Session,token:str):
    decoded_token = Auth.decode_access_token(token)
    clinic_id = getClinicsProfileByUser(decoded_token,db).id
    offer = db.query(OfferBoard).get(OfferBoard.text == offer.text,
                                     OfferBoard.phone == offer.phone,
                                     OfferBoard.clinic_id == clinic_id

                                     )
    db.delete(offer)
    db.commit()