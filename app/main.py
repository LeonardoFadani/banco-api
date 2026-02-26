from fastapi import FastAPI
from app.database import engine, Base
from app.routers.conta_router import router as conta_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(conta_router)