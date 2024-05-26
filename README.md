# <p align='center'>Online Gaming Platform</p>

<br>

## Tabel of Contents
- []()

# Game State Data (Real-Time Updates) `real_time_stats.py`

Real time updates is an essential key aspect of any game, as we need to continuasly know where certain valubale items are and not only items but also the player to be able to execute certain formulas like generating the enemy spawn zone or calculating their view distance.

As such we choose to contain these valubale information in the Redis DBMS as its read/write execution is really fast and is perfect for what we want to achieve.

<details>
<summary><b>View function details (Click to Show/Unshow)</b></summary>

- `def update_player_location(player_id, position):`
    - This method is responsible of updating the player's location (currently we're concerned with x & y position only)
    - Its parameters are:
        - `player_id`: The player's id that we want to update their position.
        - `position`: A dictionary containing the new x & y position.
- `def get_player_location(player_id):`
    - This method is responsible of retrieving the player's location from the redis DBMS
    - Its parameters are:
        - `player_id`: The player's id we want to retrieve their position.
- `def update_game_event(event_id, player_id, event_type, details)`
    - This method is responsible of updating the event's details, which are whom triggered the event, what type of event it is, and extra details on the evnet.
    - Its parameters are:
        - `event_id`: The id of the event we wish to update.
        - `player_id`: The player whom triggered the event update.
        - `event_type`: The type of event which can only at the moment be either `'item_pickup'` or `'enemy_defeated'`.
        - `details`: Extra details about the evnet like the item id that was picked up or the enemy id that was defeated.
- `def get_game_event(event_id):`
    - This method is responsible of retrieving the game event's details
    - Its parameters are:
        - `event_id`: The if of the event we want its details retrieved.
- `def update_world_resource(resource_id, resource,type, quantity, location):`
    - This method is responsible of updating the resource's details.
    - Its parameters are:
        - `resource_id`: The resoruce id we wish to update.
        - `resource_type`: The type of the resource.
        - `quantity`: The quantity of the resource available.
        - `location`: The x & y location of the resource.
- `def get_world_resource(resource_id):`
    - This method is responsible of retrieving the resource details.
    - Its parameters are:
        - `resource_id`: The resource id we want to retrieve it's details.

</details>
