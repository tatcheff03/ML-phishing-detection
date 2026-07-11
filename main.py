from fastapi import FastAPI
from config.database import engine, Base
import models
import api.auth_api
import api.url_check_api
import api.activity_log_api
import api.anomalies_api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# add cors middleware for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}

app.include_router(api.auth_api.router, prefix="/auth", tags=["auth"])
app.include_router(api.url_check_api.router, prefix="/url", tags=["url"])
app.include_router(api.activity_log_api.router, prefix="/logs", tags=["logs"])
app.include_router(api.anomalies_api.router, prefix="/anomalies", tags=["anomalies"])