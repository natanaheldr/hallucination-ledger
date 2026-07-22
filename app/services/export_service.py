import csv
import io
import json
from datetime import datetime


def export_csv(claims: list) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "claim_text", "status", "model_name", "created_at"])
    for claim in claims:
        model_name = claim.source.model_name if claim.source else ""
        created = claim.created_at.isoformat() if isinstance(claim.created_at, datetime) else str(claim.created_at)
        writer.writerow([claim.id, claim.claim_text, claim.status, model_name, created])
    return output.getvalue()


def export_json(claims: list) -> str:
    data = []
    for claim in claims:
        model_name = claim.source.model_name if claim.source else None
        created = claim.created_at.isoformat() if isinstance(claim.created_at, datetime) else str(claim.created_at)
        updated = claim.updated_at.isoformat() if isinstance(claim.updated_at, datetime) else str(claim.updated_at)
        data.append({
            "id": claim.id,
            "claim_text": claim.claim_text,
            "status": claim.status,
            "model_name": model_name,
            "source_url": claim.source_url,
            "notes": claim.notes,
            "created_at": created,
            "updated_at": updated,
        })
    return json.dumps(data, indent=2, ensure_ascii=False)
