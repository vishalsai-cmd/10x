from fastapi import APIRouter, Request
from app.planner import generate_trajectory
from app.database import get_db_connection
import json, time

router = APIRouter()

@router.post("/trajectory")
async def compute_trajectory(payload: dict):
    start = time.time()
    width = payload["wall_width"]
    height = payload["wall_height"]
    obstacles = payload.get("obstacles", [])

    traj = generate_trajectory(width, height, obstacles)
    
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO trajectories (wall_width, wall_height, trajectory) VALUES (?, ?, ?)",
        (width, height, json.dumps(traj))
    )
    conn.commit()
    conn.close()

    return {"trajectory": traj, "duration_ms": (time.time() - start) * 1000}

@router.get("/trajectory/{id}")
async def get_trajectory(id: int):
    conn = get_db_connection()
    cur = conn.execute("SELECT * FROM trajectories WHERE id = ?", (id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else {"error": "Not found"}

@router.get("/trajectories")
async def list_trajectories():
    conn = get_db_connection()
    cur = conn.execute("SELECT id, timestamp FROM trajectories ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
