
import redis
from datetime import datetime

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def add_user_stats(user_id, spend, order_date):
    redis_client.zincrby('users:spend', spend, user_id)

    redis_client.hset(f'user:{user_id}:dates', order_date, spend)

def get_top_n_users_by_spend(n):

    return redis_client.zrevrange('users:spend', 0, n - 1, withscores=True)

def filter_by_date_range(start_date, end_date):
    """
    Retrieves users' stats filtered by a date range.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    results = {}

    for key in redis_client.scan_iter("user:*:dates"):
        user_id = key.split(":")[1]
        user_dates = redis_client.hgetall(key)
        user_total = sum(
            float(spend) for date, spend in user_dates.items()
            if start <= datetime.strptime(date, "%Y-%m-%d") <= end
        )
        if user_total > 0:
            results[user_id] = user_total

    return results

if __name__ == "__main__":
    # Adding mock data
    add_user_stats("U123", 500, "2025-01-10")
    add_user_stats("U456", 300, "2025-01-09")
    
    print("Top 2 Users by Spend:", get_top_n_users_by_spend(2))
    
    print("Users Spend from 2025-01-08 to 2025-01-10:", filter_by_date_range("2025-01-08", "2025-01-10"))
