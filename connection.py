import redis # type: ignore

def getRedisConnection():
    """getRedisConnection

    This method establishes a connection & returns that
    connection.

    Return:
        (redis.client.Redis): The connection established.
    """
    r = redis.Redis(
        host='localhost',
        port='6379',
        password='',
        decode_responses=True)
    return r
