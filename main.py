from fastapi import FastAPI
from database import engine, Base
import models
import api.auth_api
import api.url_check_api
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}

app.include_router(api.auth_api.router, prefix="/auth", tags=["auth"])
app.include_router(api.url_check_api.router, prefix="/url", tags=["url"])