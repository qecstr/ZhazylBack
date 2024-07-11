from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import app.models as models
import sqlalchemy as sql
from app.Patients.routes import router

from app.services.serviceRoutes import router as serviceRoutes
from app.database import engine
from app.adminPanel.route import admin as adminRouter
from app.Clinics.routes import router as clinicsRouter
from app.orders.routes import router as ordersRouter
from app.Profiles.routesPatientProfile import routerProfiles as patientProfile
from app.Profiles.routesDoctorsProfile import routerProfiles as doctorsProfile
from app.Profiles.routesClinicsProfile import routerProfiles as clinicsProfile
from app.Doctors.routes import router as doctorsRouter

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
#patients = sql.Table('Patients', sql.MetaData(), autoload_with=engine)
#doctors = sql.Table('Doctors', sql.MetaData(), autoload_with=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET','POST','DELETE'],
    allow_headers=["*"],
)
app.include_router(router, prefix="", tags=["PatientRegistration"])
app.include_router(patientProfile, prefix="", tags=["patientProfile"])
app.include_router(doctorsProfile, prefix="", tags=["doctorsProfile"])
app.include_router(clinicsProfile, prefix="", tags=["clinicsProfile"])
app.include_router(serviceRoutes, prefix="", tags=["services"])
app.include_router(adminRouter, prefix="", tags=["Admin"])
app.include_router(clinicsRouter, prefix="", tags=["Clinic"])
app.include_router(ordersRouter, prefix="", tags=["Orders"])
app.include_router(doctorsRouter, prefix="", tags=["doctorsRegistration"])