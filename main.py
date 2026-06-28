from fastapi import FastAPI
from config.database import engine, Base
import models
import api.auth_api
import api.url_check_api
import api.activity_log_api
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}

app.include_router(api.auth_api.router, prefix="/auth", tags=["auth"])
app.include_router(api.url_check_api.router, prefix="/url", tags=["url"])
app.include_router(api.activity_log_api.router, prefix="/logs", tags=["logs"])