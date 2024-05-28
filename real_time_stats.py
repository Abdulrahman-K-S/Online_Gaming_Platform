"""
This module contains the functions that will update & retrieve
to & from the redis DBMS about the real time stats which are
player location, game event, and resources.
"""

import json
import time
from typing import Dict, Literal

from connection import r as redis


def update_player_location(player_id: int, position: Dict[str, int]):
    """update_player_location

    This method takes in the playerID that their position has changed
    along with the new x & y position and updates the DBMS with
    the new position of the player in the world.

    Arguments:
        player_id (int): The player's id that their position has changed.
        position (Dict[str, int]): The x & y position of the player.
    """
    timestamp = int(time.time())
    redis.hset(f"game:players:player:{player_id}:location", mapping={
        'position': json.dumps(position),
        'timestamp': timestamp
    })


def get_player_location(player_id: int) -> Dict[str, int]:
    """get_player_location

    This method retrieves the positions of the player if they're
    in the system.

    Arguments:
        player_id (int): The player's id that we want their position retrieved.

    Return:
        (Dict[str, int]): The player's x & y position along with the
                               timestamp.
    """
    player_location = redis.hgetall(f"game:players:player:{player_id}:location")
    if player_location:
        return player_location
    return (f"Player ID {player_id} not found")


def update_game_event(event_id: int, player_id: int,
                      event_type: Literal['item_pickup', 'enemy_defeated'],
                      details: Dict[str, any]) -> int:
    """update_game_event

    This method notifies the DBMS of an event update, these events could
    be either the player has picked up an item or has defeated
    an enemy.

    Arguments:
        event_id (int): The event's id to be updated.
        player_id (int): The player's id that caused the event update.
        event_type (Literal['item_pickup', 'enemy_defeated']): Type of event.
        details (Dict[str, any]): Additional details about the event.
    """
    timestamp = time.time()
    redis.hset(f"game:event:{event_id}", mapping={
        'event_type': event_type,
        'player_id': player_id,
        'details': json.dumps(details),
        'timestamp': timestamp
    })


def get_game_event(event_id: int) -> Dict[str, any]:
    """get_game_event

    This method retrieves the event details for the specific event id
    if it's in the system.

    Arguments:
        event_id (int): The event id that we want its details retrieved.

    Return:
        (Dict[str, any]): The game event details along with the type,
                          player id and the timestamp of the event.
    """
    game_event = redis.hgetall(f"game:event:{event_id}")
    if game_event:
        return game_event
    return (f"Event id {event_id} not found")


def update_world_resource(resource_id: str, resource_type: str, quantity: int,
                          location: Dict[str, int]):
    """update_world_resource

    This method notifies the DBMS of a resource update.

    Arguments:
        resource_id (str): The unique identifier of the resource.
        type (str): The type of the resource (e.g., wood, stone).
        quantity (int): The current quantity of the resource.
        location (Dict[str, int]): The location of the resource, represented as
                                   a dictionary with keys 'x', 'y'.
    """
    timestamp = time.time()
    redis.hset(f"game:world:resource:{resource_id}", mapping={
        'type': resource_type,
        'quantity': quantity,
        'location': json.dumps(location),
        'timestamp': timestamp
    })


def get_world_resource(resource_id: str) -> Dict[str, any]:
    """get_world_resource

    This method retrieves the resource details for the specific resource id
    if it's in the system.

    Arguments:
        resource_id (str): The resource id that we want its details retrieved.

    Return:
        (Dict[str, any]): The resource details.
    """
    game_event = redis.hgetall(f"game:world:resource:{resource_id}")
    if game_event:
        return game_event
    return (f"Event id {resource_id} not found")
