import pytest
from fastapi.testclient import TestClient
from time import sleep
from wmapi import app

client = TestClient(app)


def test_create_scan():
    response = client.post("/scan/", json={"target": "192.168.0.1-20"})
    assert response.status_code == 422

    response = client.post("/scan/", json={"target": ["192.168.0.1-20"], "ports": [7373], "threads": 10, "timeout": 35})
    assert response.status_code == 200


def test_get_scans():
    response = client.get("/scan/")
    created_scans = response.json()
    assert response.status_code == 200
    assert len(created_scans) == 1


def test_get_scan_by_id():
    response = client.get("/scan/")
    created_scans = response.json()

    response = client.get(f"/scan/{list(created_scans.keys())[0]}")
    scan_info = response.json()

    assert response.status_code == 200
    assert len(scan_info.keys()) > 0

def test_scan():
    response = client.post("/scan/", json={"target": ["https://127.0.0.1"], "ports": [443], "threads": 10, "timeout": 10})
    scan = response.json()
    assert response.status_code == 200

    scan_id = scan['id']

    response = client.get(f"/scan/{scan_id}/start")
    assert response.status_code == 200

    response = client.get(f"/scan/{scan_id}")
    assert response.status_code == 200
    assert response.json()['state'] == 'started'

    sleep(5)

    response = client.get(f"/scan/{scan_id}/stop")
    assert response.status_code == 200

    response = client.get(f"/scan/{scan_id}")
    assert response.status_code == 200
    assert response.json()['state'] == 'stopped'