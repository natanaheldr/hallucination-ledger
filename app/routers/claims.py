from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Claim, ClaimAudit, ResponseSource
from app.schemas import ClaimCreate, ClaimStatusUpdate, ExtractRequest, ClaimOut, ClaimsResponse
from app.services.claim_extractor import extract_claims

router = APIRouter(prefix="/api/claims", tags=["claims"])


@router.get("", response_model=ClaimsResponse)
def list_claims(
    status: str | None = Query(None),
    search: str | None = Query(None),
    source_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Claim)

    if status:
        query = query.filter(Claim.status == status)
    if search:
        query = query.filter(Claim.claim_text.ilike(f"%{search}%"))
    if source_id:
        query = query.filter(Claim.source_id == source_id)

    total = query.count()
    total_pages = (total + per_page - 1) // per_page
    claims = query.order_by(Claim.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for c in claims:
        cd = ClaimOut.model_validate(c)
        cd.model_name = c.source.model_name if c.source else None
        result.append(cd)

    return ClaimsResponse(claims=result, total=total, page=page, per_page=per_page, total_pages=total_pages)


@router.post("", response_model=ClaimOut, status_code=201)
def create_claim(body: ClaimCreate, db: Session = Depends(get_db)):
    if body.source_id:
        source = db.query(ResponseSource).filter(ResponseSource.id == body.source_id).first()
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

    claim = Claim(
        source_id=body.source_id,
        claim_text=body.claim_text,
        status="unreviewed",
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)

    cd = ClaimOut.model_validate(claim)
    cd.model_name = claim.source.model_name if claim.source else None
    return cd


@router.post("/extract")
def extract_and_create(body: ExtractRequest, db: Session = Depends(get_db)):
    if not body.raw_text.strip():
        raise HTTPException(status_code=400, detail="No text provided")

    source = ResponseSource(
        model_name=body.model_name,
        prompt=body.prompt,
        raw_text=body.raw_text,
    )
    db.add(source)
    db.commit()
    db.refresh(source)

    extracted = extract_claims(body.raw_text)
    created_claims = []
    for claim_text in extracted:
        claim = Claim(
            source_id=source.id,
            claim_text=claim_text,
            status="unreviewed",
        )
        db.add(claim)
        db.commit()
        db.refresh(claim)

        cd = ClaimOut.model_validate(claim)
        cd.model_name = source.model_name
        created_claims.append(cd)

    return {"source_id": source.id, "claims_extracted": len(created_claims), "claims": created_claims}


@router.patch("/{claim_id}/status", response_model=ClaimOut)
def update_claim_status(claim_id: int, body: ClaimStatusUpdate, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    valid_statuses = {"unreviewed", "verified", "doubtful", "false"}
    if body.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    old_status = claim.status
    claim.status = body.status
    if body.source_url is not None:
        claim.source_url = body.source_url
    if body.notes is not None:
        claim.notes = body.notes

    audit = ClaimAudit(claim_id=claim.id, old_status=old_status, new_status=body.status)
    db.add(audit)
    db.commit()
    db.refresh(claim)

    cd = ClaimOut.model_validate(claim)
    cd.model_name = claim.source.model_name if claim.source else None
    return cd


@router.delete("/{claim_id}")
def delete_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    db.delete(claim)
    db.commit()
    return {"detail": "Claim deleted"}


@router.get("/export")
def export_claims(
    format: str = Query("csv", pattern="^(csv|json)$"),
    status: str | None = Query(None),
    source_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    from fastapi.responses import PlainTextResponse, Response

    query = db.query(Claim)
    if status:
        query = query.filter(Claim.status == status)
    if source_id:
        query = query.filter(Claim.source_id == source_id)

    claims = query.order_by(Claim.created_at.desc()).all()

    if format == "csv":
        from app.services.export_service import export_csv
        content = export_csv(claims)
        return PlainTextResponse(content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=ledger_export.csv"})
    else:
        from app.services.export_service import export_json
        content = export_json(claims)
        return Response(content, media_type="application/json", headers={"Content-Disposition": "attachment; filename=ledger_export.json"})
