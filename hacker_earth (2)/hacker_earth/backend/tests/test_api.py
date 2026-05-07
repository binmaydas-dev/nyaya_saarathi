import os
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_upload_demo_mode():
    # Since demo mode doesn't actually process the file, we can send a dummy text file
    # masquerading as a PDF just to pass the initial extension check.
    files = {"file": ("dummy.pdf", b"%PDF-1.4 mock content", "application/pdf")}
    response = client.post("/upload?demo_mode=true", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["processing_mode"] == "mock_demo"
    assert "analytics" in data
    assert "id" in data

def test_export_endpoint():
    # First get a demo ID
    files = {"file": ("dummy.pdf", b"%PDF-mock", "application/pdf")}
    upload_res = client.post("/upload?demo_mode=true", files=files)
    export_id = upload_res.json()["id"]
    
    # Test JSON export
    res_json = client.get(f"/export/{export_id}?format=json")
    assert res_json.status_code == 200
    assert res_json.json()["id"] == export_id
    
    # Test TXT export
    res_txt = client.get(f"/export/{export_id}?format=txt")
    assert res_txt.status_code == 200
    assert "NYAYAMITRA LEGAL SUMMARY" in res_txt.text
