from app.models import Claim, ResponseSource
from app.services.export_service import export_csv, export_json
from datetime import datetime, timezone


class TestExportService:
    def test_export_csv(self, db_session):
        source = ResponseSource(model_name="GPT-4o", prompt="test", raw_text="raw")
        db_session.add(source)
        db_session.commit()

        claim = Claim(claim_text="Test claim", status="verified", source_id=source.id,
                      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc))
        db_session.add(claim)
        db_session.commit()
        db_session.refresh(claim)

        csv_data = export_csv([claim])
        assert "Test claim" in csv_data
        assert "verified" in csv_data
        assert "GPT-4o" in csv_data

    def test_export_json(self, db_session):
        source = ResponseSource(model_name="Claude 3.5", prompt="test", raw_text="raw")
        db_session.add(source)
        db_session.commit()

        claim = Claim(claim_text="JSON claim", status="false", source_id=source.id,
                      created_at=datetime(2024, 2, 1, tzinfo=timezone.utc))
        db_session.add(claim)
        db_session.commit()
        db_session.refresh(claim)

        json_data = export_json([claim])
        assert "JSON claim" in json_data
        assert "false" in json_data
        assert "Claude 3.5" in json_data

    def test_export_empty_list(self):
        csv_data = export_csv([])
        assert "id" in csv_data

        json_data = export_json([])
        assert json_data == "[]"
