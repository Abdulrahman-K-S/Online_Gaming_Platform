import redis
from cassandra.cluster import Cluster


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


def getCassandraConnection():
    """getCassandraConnection

    This method establishes a connection & returns that
    connection

    Return:
        ():
    """
    cluster = Cluster(['localhost'])
    session = cluster.connect('game')
    return session


r = getRedisConnection()
c = getCassandraConnection()
