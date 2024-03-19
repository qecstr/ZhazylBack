from fastapi import FastAPI
import app.models as models
import sqlalchemy as sql
from app.Patients.routes import router
from app.Profiles.routes import routerProfiles
from app.database import engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
#patients = sql.Table('Patients', sql.MetaData(), autoload_with=engine)
#doctors = sql.Table('Doctors', sql.MetaData(), autoload_with=engine)
app.include_router(router, prefix="", tags=[""])
app.include_router(routerProfiles, prefix="", tags=[""])
