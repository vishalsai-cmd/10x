from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_trajectory_post():
    response = client.post("/trajectory", json={
        "wall_width": 5.0,
        "wall_height": 5.0,
        "obstacles": [[1.0, 1.0, 0.25, 0.25]] 
    })
    assert response.status_code == 200
    data = response.json()
    assert "trajectory" in data
    assert len(data["trajectory"]) > 0

def test_get_trajectory():
    response = client.get("/trajectory/1")
    assert response.status_code in [200, 404]  

def test_list_trajectories():
    response = client.get("/trajectories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
