from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session

from app.db.schemas import ClanCreate, ClanOut
from app.db.session import get_db
from app.db import repository

router = APIRouter(prefix="/clans", tags=["clans"])

@router.post("", response_model=ClanOut, status_code=status.HTTP_201_CREATED)
def create_clan(payload: ClanCreate, db: Session = Depends(get_db)):
    existing = repository.get_clan_by_name_exact(db, name=payload.name.strip())
    if existing is not None:
        raise HTTPException(status_code=409, detail="clan name already exists")

    return repository.create_clan(db, name=payload.name, region=payload.region)

@router.get("", response_model=List[ClanOut])
def list_clans(db: Session = Depends(get_db)):
    return repository.list_clans(db)

@router.get("/search", response_model=List[ClanOut])
def search_clans(
    name: str = Query(..., min_length=3, description="contains search, minimum 3 characters"),
    db: Session = Depends(get_db),
):
    q = name.strip()
    if len(q) < 3:
        raise HTTPException(status_code=400, detail="name must be at least 3 characters")
    return repository.search_clans_by_name_contains(db, q=q)

@router.delete(
    "/{clan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "deleted"},
        404: {"description": "clan not found"},
    },
)
def delete_clan(clan_id: UUID, db: Session = Depends(get_db)) -> Response:
    ok = repository.delete_clan_by_id(db, clan_id=clan_id)
    if not ok:
        raise HTTPException(status_code=404, detail="clan not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
