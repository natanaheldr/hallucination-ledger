from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Claim, ResponseSource
from app.schemas import SourceCreate, SourceOut

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(ResponseSource).order_by(ResponseSource.created_at.desc()).all()


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


@router.get("/{source_id}", response_model=SourceOut)
def get_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(ResponseSource).filter(ResponseSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.delete("/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(ResponseSource).filter(ResponseSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
    return {"detail": "Source and all its claims deleted"}


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Claim).count()
    verified = db.query(Claim).filter(Claim.status == "verified").count()
    doubtful = db.query(Claim).filter(Claim.status == "doubtful").count()
    false_count = db.query(Claim).filter(Claim.status == "false").count()
    unreviewed = db.query(Claim).filter(Claim.status == "unreviewed").count()

    verified_pct = round(verified / max(total, 1) * 100, 1)
    false_pct = round(false_count / max(total, 1) * 100, 1)

    by_model = {}
    sources = db.query(ResponseSource).all()
    for source in sources:
        model_claims = db.query(Claim).filter(Claim.source_id == source.id).all()
        if model_claims:
            model_total = len(model_claims)
            model_verified = sum(1 for c in model_claims if c.status == "verified")
            model_false = sum(1 for c in model_claims if c.status == "false")
            model_doubtful = sum(1 for c in model_claims if c.status == "doubtful")
            model_unreviewed = sum(1 for c in model_claims if c.status == "unreviewed")
            by_model[source.model_name] = {
                "total": model_total,
                "verified": model_verified,
                "false": model_false,
                "doubtful": model_doubtful,
                "unreviewed": model_unreviewed,
                "hallucination_rate": round(model_false / max(model_total, 1) * 100, 1),
            }

    return {
        "total": total,
        "verified": verified,
        "doubtful": doubtful,
        "false_count": false_count,
        "unreviewed": unreviewed,
        "verified_pct": verified_pct,
        "false_pct": false_pct,
        "by_model": by_model,
    }
