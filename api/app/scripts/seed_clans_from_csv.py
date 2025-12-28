import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Clan
from app.db.session import SessionLocal


def parse_created_at_utc(s: Optional[str]) -> datetime:
    if s is None:
        return datetime.now(timezone.utc)

    raw = s.strip()
    if raw == "":
        return datetime.now(timezone.utc)

    try:
        dt = datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.now(timezone.utc)


def upsert_by_name(db: Session, *, name: str, region: str, created_at: datetime) -> bool:
    existing = db.query(Clan).filter(Clan.name == name).first()
    if existing is not None:
        return False

    clan = Clan(name=name, region=region, created_at=created_at)
    db.add(clan)
    db.commit()
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="seed clans table from csv")
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=str(Path(__file__).parent / "clan_sample_data.csv"),
        help="path to clan_sample_data.csv",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path).expanduser().resolve()
    if not csv_path.exists():
        raise FileNotFoundError(f"missing csv: {csv_path}")

    inserted = 0
    skipped = 0
    errors = 0

    db: Session = SessionLocal()
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or "").strip()
                region = (row.get("region") or "").strip().upper()
                created_at = parse_created_at_utc(row.get("created_at"))

                if not name or not region:
                    skipped += 1
                    continue

                if len(region) != 2 or not region.isalpha():
                    skipped += 1
                    continue

                try:
                    did_insert = upsert_by_name(db, name=name, region=region, created_at=created_at)
                    if did_insert:
                        inserted += 1
                    else:
                        skipped += 1
                except Exception:
                    db.rollback()
                    errors += 1

    finally:
        db.close()

    print(f"seed complete: inserted={inserted}, skipped={skipped}, errors={errors}")
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
