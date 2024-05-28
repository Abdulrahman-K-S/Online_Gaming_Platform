# <p align='center'>Online Gaming Platform</p>

<br>

## Tabel of Contents
- [Introduction](#introduction)
    - [Player Data](#1-player-data-playerprofilespy-cassandra)
    - [Game Data](#2-game-data-game_info_handlerpy-cassandra)
    - [Game Object Data](#3-game-object-data-game_object_handlerpy-cassandra)
    - [Game State Data](#4-game-state-data-real-time-updates-real_time_statspy-redis)
    - [Leaderboard Management](#5-leaderboard-management-leaderboardmanagementpy-redis)
    - [Social Features](#6-social-features-social_featurespy-redis)
    - [Player Statistics](#7-player-statistics-playerstatisticspy-cassandra)
    - [Game Analytics](#8--game-analytics-game_analyticspy-cassandra)
- [Contributers](#contributers)

<br>

# Introduction

The ever-growing popularity of online gaming demands robust data management solutions to handle real-time updates, complex interactions, and diverse player data.

This project challenges us to design a data model for an online gaming platform with leaderboards, utilizing a combination of multiple data management systems (**DBMS**).

This project outlines the data requirements for an online gaming platform featuring real-time leaderboards and a rich user experience.

<br>

## 1. Player Data `PlayerProfiles.py` (Cassandra)
The idea behind this script is to manage player profiles within a game. Player profiles include details such as achievements, email, friend list, inventory, profile picture, username, and password.


### Present Tables

#### player_profiles
Let's start with the foundation: the table that will serve as the basis for storing our players' profiles. It consists of the following fields:
```sql
CREATE TABLE IF NOT EXISTS player_profiles (
    player_id int PRIMARY KEY,
    achievements list<text>,
    email text,
    friend_list map<int, text>,
    inventory map<text, int>,
    profile_picture text,
    username text,
    password text
)
```

- Purpose: To store detailed player profiles including achievements, email, friend list, inventory, profile picture, username, and password.
- Rationale:
    - Cassandra's Strength: Apache Cassandra is chosen for this because it excels at handling large volumes of data and provides high availability with its distributed architecture.
    - Use Case Fit: Player profiles are relatively static and do not require frequent updates, making Cassandra a good fit for this type of data.

<details>
<summary><b>View functions & their details (Click to Show/Unshow)</b></summary>

1. `def get_initial_player_id():`
    - Retrieves the initial player ID from the database.

2. `def generate_unique_player_id():`
    - Generates a unique player ID.

3. `def create_player_profile(achievements, email, friend_list, inventory, profile_picture, username, password):`
    - Creates a new player profile with the provided details.
    - Parameters:
        - `achievements`: List of achievements.
        - `email`: Email address of the player.
        - `friend_list`: Dictionary mapping friend IDs to usernames.
        - `inventory`: Dictionary representing the player's inventory.
        - `profile_picture`: URL or path to the player's profile picture.
        - `username`: Player's username.
        - `password`: Player's password.

4. `def get_player_profile(player_id):`
    - Retrieves the profile of a player based on the player ID.

5. `def get_username(player_id):`
    - Retrieves the username of a player based on the player ID.

6. `def update_player_profile(player_id, achievements, email, friend_list, inventory, profile_picture, username, password):`
    - Updates the profile of a player with the provided details.

7. `def delete_player_profile(player_id):`
    - Deletes the profile of a player based on the player ID.

8. `def add_friend(player_id, friend_id, friend_username):`
    - Adds a friend to the friend list of a player.
    - Parameters:
        - `player_id`: ID of the player.
        - `friend_id`: ID of the friend to be added.
        - `friend_username`: Username of the friend to be added.

9. `def print_profile(profile):`
    - Prints the details of a player's profile.
    - Parameters:
        - `profile`: Player profile object containing details to be printed.
</details>

## 2. Game Data `Game_Info_Handler.py` (Cassandra)
Every game needs to have its own tables so that we can distingues the various games that our company could create/develop.

### Game Info Table
This is the table that houses the various games our company could establish so that we can easily track their different aspects.

Its datatypes are:
```sql
CREATE TABLE GameInfo (
    game_id UUID PRIMARY KEY,
    name TEXT,
    type TEXT,
    current_state TEXT,
    world_layout TEXT
);
```

- Purpose: To store information about various games developed by the company.
- Rationale:
    - High Availability and Scalability: Cassandra provides the necessary scalability to handle data for potentially numerous games.
    - Consistency: The relatively static nature of game info means strong consistency requirements can be relaxed.

## 3. Game Object Data `Game_Object_Handler.py` (Cassandra)
As we need to have for each game its own attributes we need to have for each object in the game their own attributes as well.

Its datatypes are:
### Game Object Table
```sql
CREATE TABLE GameObject (
    game_id UUID,
    object_id TEXT,
    type TEXT,
    position_x INT,
    position_y INT,
    position_z INT,
    attributes MAP<TEXT, TEXT>,
    PRIMARY KEY (game_id, object_id)
);
```

- Purpose: To store attributes and positions of game objects within each game.
- Rationale:
    - Scalable Data Model: Each game can have many objects, and Cassandra’s wide-row storage model fits well with this requirement.

## 4. Game State Data (Real-Time Updates) `real_time_stats.py` (Redis)

Real time updates is an essential key aspect of any game, as we need to continuasly know where certain valubale items are and not only items but also the player to be able to execute certain formulas like generating the enemy spawn zone or calculating their view distance.

As such we choose to contain these valubale information in the Redis DBMS as its read/write execution is really fast and is perfect for what we want to achieve.

### Present Tables

#### Player Location
This part houses the location of a player. The directory of the folder that houses all the player locations are in `game:players:player:<player_id>:location`.

It's data type is:
```js
'position': {
    str: int
},
'timestamp': timestamp
```

#### Game Events
This part houses all the game events triggered by the player, which is currently only concerned with `'item_pickup'` or `'enemy_defeated'`. The directory of the folder that houses all the events are in `game:event:<event_id>`.

It's data type is:
```js
'event_id': uuid4
'event_type': str
'player_id': int
'details': {
    str: str
}
'timestamp': timestamp
```

#### World Resource
This part houses the data of the world resources. The directory of the folder that houses all the world resources are in `game:world:resource:<resource_id>`.

It's data type is:
```js
'type': str,
'quantity': int,
'location': {
    str: int
},
'timestamp': timestamp
```

- Purpose: To store real-time data for player locations, game events, and world resources.
- Rationale:
    - Low Latency: Redis is used for real-time updates due to its low-latency data access and high-speed read/write capabilities.
    - In-Memory Storage: The in-memory nature of Redis ensures quick access and updates, which is crucial for real-time game state management.

<details>
<summary><b>View functions & their details (Click to Show/Unshow)</b></summary>

1. `def update_player_location(player_id, position):`
    - This method is responsible of updating the player's location (currently we're concerned with x & y position only)
    - Its parameters are:
        - `player_id`: The player's id that we want to update their position.
        - `position`: A dictionary containing the new x & y position.

2. `def get_player_location(player_id):`
    - This method is responsible of retrieving the player's location from the redis DBMS
    - Its parameters are:
        - `player_id`: The player's id we want to retrieve their position.

3. `def update_game_event(event_id, player_id, event_type, details)`
    - This method is responsible of updating the event's details, which are whom triggered the event, what type of event it is, and extra details on the evnet.
    - Its parameters are:
        - `event_id`: The id of the event we wish to update.
        - `player_id`: The player whom triggered the event update.
        - `event_type`: The type of event which can only at the moment be either `'item_pickup'` or `'enemy_defeated'`.
        - `details`: Extra details about the evnet like the item id that was picked up or the enemy id that was defeated.

4. `def get_game_event(event_id):`
    - This method is responsible of retrieving the game event's details
    - Its parameters are:
        - `event_id`: The if of the event we want its details retrieved.

5. `def update_world_resource(resource_id, resource,type, quantity, location):`
    - This method is responsible of updating the resource's details.
    - Its parameters are:
        - `resource_id`: The resoruce id we wish to update.
        - `resource_type`: The type of the resource.
        - `quantity`: The quantity of the resource available.
        - `location`: The x & y location of the resource.

6. `def get_world_resource(resource_id):`
    - This method is responsible of retrieving the resource details.
    - Its parameters are:
        - `resource_id`: The resource id we want to retrieve it's details.
</details>

<br>

## 5. Leaderboard Management `LeaderboardManagement.py` (Redis)

The purpose of this script is to manage leaderboards within a game, allowing for the addition of scores and retrieval of top scorers. Its directory is in `game:<game_id>:leaderboard:<leaderboard>`

It's data type is:
```js
'str': int
```

- Purpose: To manage leaderboards within the game, allowing for the addition of scores and retrieval of top scorers.
- Rationale:
    - Fast Access: Redis's sorted sets provide an efficient way to maintain and query leaderboards.
    - Real-Time Updates: The need for real-time score updates and retrieval makes Redis a suitable choice.
    
<details>
<summary><b>View functions & their details (Click to Show/Unshow)</b></summary>

1. `def add_score(game_id, leaderboard, username, score):`
    - Adds a score to the specified leaderboard.
    - Parameters:
        - `game_id`: ID of the game.
        - `leaderboard`: Name of the leaderboard.
        - `username`: Username of the player.
        - `score`: Score to be added.

2. `def get_top_scorers(leaderboard, num_top=3):`
    - Retrieves top scorers from the specified leaderboard.
    - Parameters:
        - `leaderboard`: Name of the leaderboard.
        - `num_top`: Number of top scorers to retrieve (default is 3).
    - Returns:
        - List of tuples containing (username, score) for top scorers.

</details>

## 6. Social Features `social_features.py` (Redis)

This file will contain all the social & guild features for the game.

### Present Tables

#### Guild
As to implement the guild features we needed to first have a guild to build upon which is the core case of this table. The folder which houses all the guilds made by the players are in `guild:<guild_name>:<guild_name>`

It's data type is:
```js
`guild_name`: str
'member_count': int
'members': [
    {str: any}
]
'decription': str
'updated_at': timestamp
'created_at': timestamp
```


#### Guild Messages
This part houses the ingame chat of the guild members in a certain guild. The directory of the guild chat is in `guild:<guild_name>:<guild_name>:char_history`

It's data type is:
```js
int: {str, int}
```

### InGame Chat
This part houses the ingame chat of the game. The directory of the char will be in `game:<game_id>:game_chat`

It's data type is:
```js
'message_id': int,
'player_name': str,
'content': str,
'timestamp': timestamp
```

- Purpose: To manage guild features and in-game chat functionalities.
- Rationale:
    - Real-Time Interaction: Redis is chosen for social features due to its ability to handle real-time data effectively.
    - In-Memory Speed: Quick access to guild information and chat messages is critical for an engaging social experience in the game.

<details>
<summary><b>View functions & their details (Click to Show/Unshow)</b></summary>

1. `def create_guild(guild_name, description, member_count, members):`
    - This method's responsibility is to create a new guild and in cases where the guild is already present in the system return a message indicating that it's already created.
    - Parameters are:
        - `guild_name`: The unique identifier of the guilds in our system.
        - `description`: The description of the guild to be displayed.
        - `member_count`: The number of members in the guild which is set to 1 by default. For display purposes.
        - `members`: A list of dictionaries containing the player's id, player's name, and their membership type in the guild.

2. `def add_guild_member(guild_name, member_info):`
    - This method's responsibility is to add a member to an already exisiting guild and in case there is no exisiting guild display a message indiciating that.
    - Parameters are:
        - `guild_name`: The unique identifier to lookup with if the guild exists or not.
        - `member_info`: The member details to be added to the `members` attribute in the guild.
</details>

## 7. Player Statistics `PlayerStatistics.py` (Cassandra)
The idea behind this script is to create a system for tracking and managing player statistics within a game. By storing metrics such as combat performance, resource management, and progression in a database, the game can provide a more immersive and personalized experience for players. These statistics can be used to enhance gameplay features such as leaderboards, achievements, and personalized feedback. 

### Present Tables

#### player_statistics
Let's begin with the foundation: the table that will serve as the basis for tracking our players' progress. 
It's data type is:

```sql 
CREATE TABLE IF NOT EXISTS player_statistics (
    player_id int PRIMARY KEY,
    combat_stats map<text, int>,
    resource_stats map<text, int>,
    progression_stats map<text, int>
)
```

- Purpose: To track and manage player statistics within the game.
- Rationale:
    - Scalability and Availability: Cassandra's architecture is suitable for handling large volumes of statistical data across numerous players.
    - Flexibility: The use of maps allows for flexible addition and modification of various statistics without altering the table schema.

<details>
<summary><b>View functions & their details (Click to Show/Unshow)</b></summary>

1. `def initialize_player_statistics():`
    -Initializes the default statistics structure for a new player, including combat, resource, and progression stats.
    
2. `def update_combat_stats(player_id, damage_dealt, enemies_defeated):`
    -Updates the combat statistics of a player with the provided damage dealt and enemies defeated values.
    -Parameters:
        -`player_id`: Integer representing the ID of the player.
        -`damage_dealt`: Integer representing the amount of damage dealt by the player.
        -`enemies_defeated`: Integer representing the number of enemies defeated by the player.

3. `def update_resource_stats(player_id, collection, crafting_materials):`
    -Updates the resource statistics of a player with the provided collection and crafting materials values.
    -Parameters:
        -`player_id`: Integer representing the ID of the player.
        -`collection`: Integer representing the amount of resources collected by the player.
        -`crafting_materials`: Integer representing the amount of crafting materials obtained by the player.

4. `def update_progression_stats(player_id, levels, quests_completed, playtime_hours):`
    -Updates the progression statistics of a player with the provided level, quests completed, and playtime hour values.
    -Parameters:
        -`player_id`: Integer representing the ID of the player.
        -`levels`: Optional integer representing the levels achieved by the player .
        -`quests_completed`: Optional integer representing the number of quests completed by the player .
        -`playtime_hours`: Optional integer representing the hours of playtime accumulated by the player .

5. `def print_statistics(player_stats,player_id):`
    -Prints out the combat, resource, and progression statistics of a player based on the provided player ID.
    -Parameters:
        -`player_id`: Integer representing the ID of the player.
        -`player_stats`: Dictionary containing the player's statistics.

6. `def get_player_statistics(player_id):`
    -Retrieves the combat, resource, and progression statistics of a player from the database based on the provided player ID.
    -Parameters:
        -`player_id`: Integer representing the ID of the player.
</details>

## 8. Game Analytics `game_analytics.py` (Cassandra)

This section is dedicated to the statistics that could be done for the program through cassandra.

### Present Tables

#### Game Event Table
This table is concerned with the various events that could occure and get triggered by the player, which is then saved with the details of which event type it was for analytical purposes.

It's data type is:
```sql
CREATE TABLE GameEvents (
    event_id UUID,
    event_type TEXT,
    player_id INT,
    timestamp TIMESTAMP,
    event_details MAP<TEXT, TEXT>,
    PRIMARY KEY (event_id)
);
```

#### Resource Utilization Table
This table is concerned with the various resources being used and what happens to these resources. This is a crucial table as with it we could identify what needs to be changed or improved for better quality.

Its data type is:
```sql
CREATE TABLE ResourceUtilization (
    resource_id UUID,
    timestamp TIMESTAMP,
    resource_type TEXT,
    usage_metrics MAP<TEXT, DOUBLE>,
    PRIMARY KEY (resource_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

- Purpose: To collect and analyze game events and resource utilization data for insights and optimization.
- Rationale:
    - Time-Series Data: Cassandra’s support for time-series data and its efficient handling of high write throughput makes it suitable for storing analytical data.
    - Query Performance: The clustering order by timestamp ensures efficient querying of recent data.

# Contributers
Abdulrahman Khaled [Github](https://github.com/Abdulrahman-K-S)

Omar Elabasery [Github](https://github.com/OmarElabasery)

Malak Mohamed [Github](https://github.com/MalakHalawany)

<a href = "https://github.com/Abdulrahman-K-S/Online_Gaming_Platform/graphs/contributors">
   <img src = "https://contrib.rocks/image?repo=Abdulrahman-k-s/Online_Gaming_Platform"/>
 </a>