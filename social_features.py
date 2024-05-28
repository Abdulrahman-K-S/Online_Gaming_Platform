"""
This module contains the social & guild features that
is present in our game.
"""

import json
import time
from typing import Dict, List
from Game_Info_Handler import game_exists
from PlayerData import get_username
from connection import r as redis


def create_guild(guild_name: str, description: str,
                 member_count: int, members: List[Dict[str, any]]):
    """create_guild

    This method is responsible for creating the guild if it's not
    already present in the DBMS.

    Arguments:
        guild_name (str):
        description (str):
        member_count (int):
        member (List[Dict[str, any]]):

    Return:
        (str): A message depending on whether the guild already exists or not.
    """
    exists = redis.exists(f"guild:{guild_name}:{guild_name}")
    if exists:
        return (f"{guild_name} already exists.")

    redis.hset(f"guild:{guild_name}:{guild_name}", mapping={
        'guild name': guild_name,
        'description': description,
        'member_count': member_count,
        'members': json.dumps(members),
        'created_at': int(time.time()),
        'updated_at': int(time.time())
    })
    add_guild_to_player(members[0]['player_id'], guild_name, members[0]['guild_type'])
    return f"Guild {guild_name} created successfully."


def add_guild_member(guild_name: str, member_info: List[Dict[str, any]]):
    """add_guild_member

    This method is responsible for adding a member to the DBMS, but checks if
    that member already exists or not in the guild.

    Arguments:
        guild_name (str): The guild unique name.
        member_info (List[Dict[str, any]]): A list of 3 items which are the
                                            player_id, player_name, and
                                            guild_type

    Return:
        (str): A message depending on whether the guild exists or not &
               whether the member is already present in the guild or not.
    """
    exists = redis.exists(f"guild:{guild_name}:{guild_name}")
    if not exists:
        return (f"{guild_name} doesn't exist.")

    guild_members_json = redis.hget(f"guild:{guild_name}:{guild_name}", "members")
    guild_members = json.loads(guild_members_json)

    player_ids = [member['player_id'] for member in guild_members]
    if member_info['player_id'] not in player_ids:
        guild_members.append(member_info)

        redis.hset(f"guild:{guild_name}:{guild_name}", mapping={
            'members': json.dumps(guild_members),
            'member_count': len(guild_members),
            'updated_at': int(time.time())
        })
        add_guild_to_player(member_info['player_id'], guild_name, member_info['guild_type'])
        return (f"Member added to {guild_name} successfully")
    return (f"{member_info['player_name']} is already a part of {guild_name}")


def add_guild_to_player(player_id: int, guild_name: str, role: str):
    """add_guild_to_player

    This method takes responsibility for adding the guild's name in
    the player account.

    Arguments:
        player_id (int): The player's unique id.
        guild_name (str): The guild's unique name.
        role (str): The role the member being added is in the guild.
    """
    exists = redis.exists(f"guild:{guild_name}:{guild_name}")
    if not exists:
        return (f"{guild_name} doesn't exist.")

    exists = redis.exists(f"game:player:{player_id}:guild")
    if exists:
        return (f"{player_id} is already in a guild.")

    redis.hset(f"game:players:player:{player_id}:guild", mapping={
        'guild_name': guild_name,
        'role': role,
        'joined_at': int(time.time()),
        'last_active': int(time.time())
    })
    return (f"Player id {player_id} has been added to guild {guild_name}")


def add_guild_message(guild_name: str, player_id: int, content: str):
    """add_guild_message

    This method is responsible for adding the messages of the guild,
    if that guild exists, to the DBMS along with whom sent it and when.

    Arguments:
        guild_name (str): The guild's unique identifier.
        player_id (int): The player's unique identifier.
        content (str): The message which the player wrote.
    """
    exists = redis.exists(f"guild:{guild_name}:{guild_name}")
    if not exists:
        return (f"{guild_name} doesn't exist.")

    message = {
        'message_id': int(time.time()) / 100,
        # 'player_name': # Add the getName from cassandra code #,
        'player_id': player_id,
        'content': content,
        'timestamp': int(time.time())
    }
    redis.rpush(f"guild:{guild_name}:chat_history", json.dumps(message))


def add_game_message(game_id, player_id, content):
    """add_game_message

    This method is responsible for adding the message of the game, if
    that game exists, to the Redis DBMS along with whom sent it and when.

    Parameter:
        game_id (uuid): The game's unique identifier.
        player_id (int): The player's unique identifier.
        content (str): The message the player wrote.
    """
    exists = game_exists(game_id)
    if not exists:
        return (f"There is no game with {game_id}!")

    message = {
        'message_id': int(time.time()) / 100,
        'player_name': get_username(player_id),
        'content': content,
        'timestamp': int(time.time())
    }
    redis.rpush("game:game_chat", json.dumps(message))
