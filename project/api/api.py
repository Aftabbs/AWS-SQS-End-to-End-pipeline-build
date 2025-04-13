from fastapi import FastAPI, HTTPException
from shared.utils import get_redis_connection

REDIS_HOST = "redis" 
REDIS_PORT = 6379
redis_client = get_redis_connection(REDIS_HOST, REDIS_PORT)

app = FastAPI() 

@app.get("/stats/global")
def get_global_stats():
    global_key = "global:stats"
    global_stats = redis_client.hgetall(global_key)

    if not global_stats:
        raise HTTPException(status_code=404, detail="Global stats not found.")

    return {
        "total_orders": int(global_stats.get("total_orders", 0)),
        "total_revenue": float(global_stats.get("total_revenue", 0.0)),
    }

@app.get("/users/{user_id}/stats")
def get_user_stats(user_id: str):
    user_key = f"user:{user_id}"
    if not redis_client.exists(user_key):
        raise HTTPException(status_code=404, detail=f"Stats for user {user_id} not found.")

    user_stats = redis_client.hgetall(user_key)
    return {
        "user_id": user_id,
        "order_count": int(user_stats.get("order_count", 0)),
        "total_spend": float(user_stats.get("total_spend", 0.0)),
    }
