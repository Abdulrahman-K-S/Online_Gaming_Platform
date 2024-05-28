"""
This module contains the game analytics components of
the game.
"""

import time
from connection import c as cassandra


def insert_event(event_id, event_type, event_details, player_id):
    """insert_event

    This method is responsible for adding the events to cassandra for
    analytic purposes.

    Arguments:
        event_id: The unique id of the event.
        event_type: The type of triggered event.
        event_details: Extra details about the event.
        player_id: The player who triggered the event.
    """
    query = \
    """
    INSERT INTO GameEvents (event_id, event_type, timestamp, event_details, player_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    timestamp = int(time.time() * 1000)
    cassandra.execute(query, (event_id, event_type, timestamp, event_details, player_id))


def get_event_by_type(player_id):
    """get_event_by_type

    This function retrieves game events associated with a specific player ID from the
    game_events table in the Cassandra database.

    Arguments:
        player_id (UUID): The unique identifier for the player.
    """
    query_item_pickup = """
    SELECT COUNT(*) AS item_pickup_count
    FROM gameevents
    WHERE player_id = %s AND event_type = 'item_pickup'
    ALLOW FILTERING;
    """
    result_item_pickup = cassandra.execute(query_item_pickup, (player_id,))
    for row in result_item_pickup:
        print(f"Item Pickups: {row.item_pickup_count}")

    query_enemy_defeated = """
    SELECT COUNT(*) AS enemy_defeated_count
    FROM gameevents
    WHERE player_id = %s AND event_type = 'enemy_defeated'
    ALLOW FILTERING;
    """
    result_enemy_defeated = cassandra.execute(query_enemy_defeated, (player_id,))
    for row in result_enemy_defeated:
        print(f"Enemies Defeated: {row.enemy_defeated_count}")

def insert_resource_utilization(resource_id, timestamp, resource_type, usage_metrics):
    """insert_resource_utilization
    
    This function inserts a record into the resource_utilization table in
    the Cassandra database. The record contains information about the utilization
    of a resource at a specific timestamp.

    Arguments:
        resource_id (UUID): The unique identifier for the resource.
        timestamp (datetime): The timestamp when the utilization data was recorded.
        resource_type (str): The type of resource (e.g., CPU, Memory, Network).
        usage_metrics (dict): A dictionary containing usage metrics of the resource,
                              including 'usage', 'temperature', 'load', etc.
    """
    query = """
    INSERT INTO ResourceUtilization (resource_id, timestamp, resource_type, usage_metrics)
    VALUES (%s, %s, %s, %s)
    """
    cassandra.execute(query, (resource_id, timestamp, resource_type, usage_metrics))

