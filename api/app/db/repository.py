from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Clan

def create_clan(db: Session, *, name: str, region: str) -> Clan:
    clan = Clan(
        name=name.strip(),
        region=region.strip().upper(),
        created_at=datetime.now(timezone.utc),
    )
    db.add(clan)
    db.commit()
    db.refresh(clan)
    return clan

def list_clans(db: Session) -> List[Clan]:
    stmt = select(Clan).order_by(Clan.created_at.desc())
    return list(db.execute(stmt).scalars().all())

def search_clans_by_name_contains(db: Session, *, q: str) -> List[Clan]:
    stmt = (
        select(Clan)
        .where(Clan.name.ilike(f"%{q}%"))
        .order_by(Clan.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())

def delete_clan_by_id(db: Session, *, clan_id: UUID) -> bool:
    clan = db.get(Clan, clan_id)
    if clan is None:
        return False

    db.delete(clan)
    db.commit()
    return True

def get_clan_by_name_exact(db: Session, *, name: str) -> Optional[Clan]:
    stmt = select(Clan).where(Clan.name == name)
    return db.execute(stmt).scalars().first()
