from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ResponseSource, Claim
from app.schemas import SourceOut, SourceCreate

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    sources = db.query(ResponseSource).order_by(ResponseSource.created_at.desc()).all()
    return sources


@router.post("", response_model=SourceOut, status_code=201)
def create_source(body: SourceCreate, db: Session = Depends(get_db)):
    source = ResponseSource(
        model_name=body.model_name,
        prompt=body.prompt,
        raw_text=body.raw_text,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Claim).count()
    verified = db.query(Claim).filter(Claim.status == "verified").count()
    doubtful = db.query(Claim).filter(Claim.status == "doubtful").count()
    false_count = db.query(Claim).filter(Claim.status == "false").count()
    unreviewed = db.query(Claim).filter(Claim.status == "unreviewed").count()

    by_model = {}
    sources = db.query(ResponseSource).all()
    for source in sources:
        model_claims = db.query(Claim).filter(Claim.source_id == source.id).all()
        if model_claims:
            model_total = len(model_claims)
            model_verified = sum(1 for c in model_claims if c.status == "verified")
            model_false = sum(1 for c in model_claims if c.status == "false")
            by_model[source.model_name] = {
                "total": model_total,
                "verified": model_verified,
                "false": model_false,
            }

    return {
        "total": total,
        "verified": verified,
        "doubtful": doubtful,
        "false_count": false_count,
        "unreviewed": unreviewed,
        "by_model": by_model,
    }
