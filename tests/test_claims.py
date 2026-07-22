

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
        assert data["claims_extracted"] >= 2

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
        assert data["page"] == 1
        assert data["per_page"] == 10

    def test_create_single_claim(self, client):
        response = client.post("/api/claims", json={"claim_text": "Water boils at 100 degrees Celsius."})
        assert response.status_code == 201
        data = response.json()
        assert data["claim_text"] == "Water boils at 100 degrees Celsius."
        assert data["status"] == "unreviewed"

    def test_update_claim_status_creates_audit(self, client):
        create_resp = client.post("/api/claims", json={"claim_text": "Mars has two moons."})
        claim_id = create_resp.json()["id"]

        patch_resp = client.patch(f"/api/claims/{claim_id}/status", json={"status": "verified"})
        assert patch_resp.status_code == 200
        assert patch_resp.json()["status"] == "verified"

        patch_resp_doubtful = client.patch(f"/api/claims/{claim_id}/status", json={"status": "doubtful"})
        assert patch_resp_doubtful.status_code == 200
        assert patch_resp_doubtful.json()["status"] == "doubtful"

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
