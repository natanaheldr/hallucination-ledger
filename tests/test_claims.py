class TestClaimsAPI:
    def test_extract_endpoint(self, client):
        payload = {
            "raw_text": "The Eiffel Tower was built in 1889. It is the tallest structure in Paris. The moon is made of cheese.",
            "model_name": "GPT-4o",
            "prompt": "Tell me about Paris",
        }
        response = client.post("/api/claims/extract", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["source_id"] is not None
        assert data["claims_extracted"] >= 1

    def test_extract_empty_text(self, client):
        response = client.post("/api/claims/extract", json={
            "raw_text": "",
            "model_name": "GPT-4o",
        })
        assert response.status_code == 422

    def test_list_claims_paginated(self, client):
        response = client.get("/api/claims?page=1&per_page=10")
        assert response.status_code == 200
        data = response.json()
        assert "claims" in data
        assert "total" in data
        assert "total_pages" in data
        assert data["page"] == 1
        assert data["per_page"] == 10

    def test_create_single_claim(self, client):
        response = client.post("/api/claims", json={"claim_text": "Water boils at 100 degrees Celsius."})
        assert response.status_code == 201
        data = response.json()
        assert data["claim_text"] == "Water boils at 100 degrees Celsius."
        assert data["status"] == "unreviewed"
        assert data["confidence"] is not None

    def test_update_claim_status_creates_audit(self, client):
        create_resp = client.post("/api/claims", json={"claim_text": "Mars has two moons."})
        claim_id = create_resp.json()["id"]

        patch_resp = client.patch(f"/api/claims/{claim_id}/status", json={"status": "verified"})
        assert patch_resp.status_code == 200
        assert patch_resp.json()["status"] == "verified"

        patch_resp_doubtful = client.patch(f"/api/claims/{claim_id}/status", json={"status": "doubtful"})
        assert patch_resp_doubtful.status_code == 200
        assert patch_resp_doubtful.json()["status"] == "doubtful"

        audit_resp = client.get(f"/api/claims/{claim_id}/audits")
        assert audit_resp.status_code == 200
        audits = audit_resp.json()
        assert len(audits) >= 2

    def test_update_invalid_status(self, client):
        create_resp = client.post("/api/claims", json={"claim_text": "Test claim."})
        claim_id = create_resp.json()["id"]

        response = client.patch(f"/api/claims/{claim_id}/status", json={"status": "invalid_status"})
        assert response.status_code == 422

    def test_delete_claim(self, client):
        create_resp = client.post("/api/claims", json={"claim_text": "Temporary claim."})
        claim_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/api/claims/{claim_id}")
        assert delete_resp.status_code == 200

        list_resp = client.get("/api/claims")
        deleted_ids = [c["id"] for c in list_resp.json()["claims"]]
        assert claim_id not in deleted_ids

    def test_claim_not_found(self, client):
        response = client.patch("/api/claims/99999/status", json={"status": "verified"})
        assert response.status_code == 404

    def test_export_csv(self, client):
        client.post("/api/claims", json={"claim_text": "Export test claim."})
        response = client.get("/api/claims/export?format=csv")
        assert response.status_code == 200
        assert "claim_text" in response.text or "Export test claim" in response.text

    def test_export_json(self, client):
        client.post("/api/claims", json={"claim_text": "JSON export claim."})
        response = client.get("/api/claims/export?format=json")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_filter_by_status(self, client):
        client.post("/api/claims", json={"claim_text": "Verified claim one."})
        created = client.post("/api/claims", json={"claim_text": "False claim two."})
        claim_id = created.json()["id"]
        client.patch(f"/api/claims/{claim_id}/status", json={"status": "false"})

        verified_resp = client.get("/api/claims?status=verified")
        assert verified_resp.status_code == 200

        false_resp = client.get("/api/claims?status=false")
        assert false_resp.status_code == 200
        assert false_resp.json()["total"] >= 1

    def test_search_claims(self, client):
        client.post("/api/claims", json={"claim_text": "Unique search term zebra."})
        response = client.get("/api/claims?search=zebra")
        assert response.status_code == 200
        assert response.json()["total"] >= 1

    def test_bulk_status_update(self, client):
        c1 = client.post("/api/claims", json={"claim_text": "Bulk claim alpha."})
        c2 = client.post("/api/claims", json={"claim_text": "Bulk claim beta."})
        c3 = client.post("/api/claims", json={"claim_text": "Bulk claim gamma."})
        ids = [c1.json()["id"], c2.json()["id"], c3.json()["id"]]

        resp = client.post("/api/claims/bulk-status", json={"claim_ids": ids, "status": "verified"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["updated"] == 3
        assert data["status"] == "verified"

        for cid in ids:
            list_resp = client.get("/api/claims?page=1&per_page=100")
            found = [c for c in list_resp.json()["claims"] if c["id"] == cid]
            assert len(found) == 1
            assert found[0]["status"] == "verified"

    def test_bulk_status_empty(self, client):
        resp = client.post("/api/claims/bulk-status", json={"claim_ids": [99999], "status": "verified"})
        assert resp.status_code == 404

    def test_get_claim_audits(self, client):
        create_resp = client.post("/api/claims", json={"claim_text": "Audit trail test."})
        claim_id = create_resp.json()["id"]

        client.patch(f"/api/claims/{claim_id}/status", json={"status": "verified"})
        client.patch(f"/api/claims/{claim_id}/status", json={"status": "false"})

        resp = client.get(f"/api/claims/{claim_id}/audits")
        assert resp.status_code == 200
        audits = resp.json()
        assert len(audits) == 2
        assert audits[0]["old_status"] == "unreviewed"
        assert audits[0]["new_status"] == "verified"
        assert audits[1]["old_status"] == "verified"
        assert audits[1]["new_status"] == "false"

    def test_audits_not_found(self, client):
        resp = client.get("/api/claims/99999/audits")
        assert resp.status_code == 404

    def test_source_crud(self, client):
        create_resp = client.post("/api/sources", json={
            "model_name": "Claude 3 Opus",
            "prompt": "What is the capital of France?",
            "raw_text": "The capital of France is Paris.",
        })
        assert create_resp.status_code == 201
        source_id = create_resp.json()["id"]

        get_resp = client.get(f"/api/sources/{source_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["model_name"] == "Claude 3 Opus"

        list_resp = client.get("/api/sources")
        assert any(s["id"] == source_id for s in list_resp.json())

        delete_resp = client.delete(f"/api/sources/{source_id}")
        assert delete_resp.status_code == 200

        get_after = client.get(f"/api/sources/{source_id}")
        assert get_after.status_code == 404

    def test_stats_endpoint(self, client):
        resp = client.get("/api/sources/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "total" in data
        assert "verified" in data
        assert "verified_pct" in data
        assert "false_pct" in data
        assert "by_model" in data
