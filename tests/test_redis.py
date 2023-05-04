from ..src.endpoints.auth import redis_conn


def test_redis_conn():
    redis_conn.set("TEST_KEY", "TEST_VALUE")
    assert redis_conn.get("TEST_KEY") == "TEST_VALUE"
