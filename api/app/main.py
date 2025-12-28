from fastapi import FastAPI

from app.db.models import Base
from app.db.session import engine
from app.routes.clans import router as clans_router

app = FastAPI(title="Clan API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"startup DB init failed: {e}")

app.include_router(clans_router)

@app.get("/health")
def health():
    return {"status": "ok"}
