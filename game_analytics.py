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
