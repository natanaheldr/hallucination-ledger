import csv
import io
import json
from datetime import datetime


def export_csv(claims: list) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "claim_text", "status", "confidence", "verification_method", "model_name", "source_url", "notes", "created_at", "updated_at"])
    for claim in claims:
        model_name = claim.source.model_name if claim.source else ""
        created = _format_datetime(claim.created_at)
        updated = _format_datetime(claim.updated_at)
        writer.writerow([
            claim.id,
            claim.claim_text,
            claim.status,
            claim.confidence or "",
            claim.verification_method or "",
            model_name,
            claim.source_url or "",
            claim.notes or "",
            created,
            updated,
        ])
    return output.getvalue()


def export_json(claims: list) -> str:
    data = []
    for claim in claims:
        data.append({
            "id": claim.id,
            "claim_text": claim.claim_text,
            "status": claim.status,
            "confidence": claim.confidence,
            "verification_method": claim.verification_method,
            "model_name": claim.source.model_name if claim.source else None,
            "source_url": claim.source_url,
            "notes": claim.notes,
            "created_at": _format_datetime(claim.created_at),
            "updated_at": _format_datetime(claim.updated_at),
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def _format_datetime(dt) -> str:
    if isinstance(dt, datetime):
        return dt.isoformat()
    return str(dt) if dt else ""
