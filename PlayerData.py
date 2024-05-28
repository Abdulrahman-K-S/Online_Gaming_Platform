from connection import c
from uuid import uuid4


c.set_keyspace("game")

c.execute("""
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
""")

def get_initial_player_id():
    result = c.execute("SELECT MAX(player_id) FROM player_profiles").one()
    return result.system_max_player_id + 1 if result.system_max_player_id is not None else 1

# Keep track of the current player_id in memory
current_player_id = get_initial_player_id()

def generate_unique_player_id():
    global current_player_id
    unique_id = current_player_id
    current_player_id += 1
    return unique_id

def create_player_profile(achievements, email, friend_list, inventory, profile_picture, username, password):
    player_id = generate_unique_player_id()
    c.execute("""
    INSERT INTO player_profiles (player_id, achievements, email, friend_list, inventory, profile_picture, username, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (player_id, achievements, email, friend_list, inventory, profile_picture, username, password))
    return player_id

def get_player_profile(player_id):
    result = c.execute("""
    SELECT * FROM player_profiles WHERE player_id = %s
    """, (player_id,))
    return result.one()

def get_username(player_id):
    result = c.execute("""
    SELECT username FROM player_profiles WHERE player_id = %s
    """, (player_id,))
    return result.one()

def update_player_profile(player_id, achievements=None, email=None, friend_list=None, inventory=None, profile_picture=None, username=None, password=None):
    updates = []
    params = []

    if achievements is not None:
        updates.append("achievements = %s")
        params.append(achievements)
    if email is not None:
        updates.append("email = %s")
        params.append(email)
    if friend_list is not None:
        updates.append("friend_list = %s")
        params.append(friend_list)
    if inventory is not None:
        updates.append("inventory = %s")
        params.append(inventory)
    if profile_picture is not None:
        updates.append("profile_picture = %s")
        params.append(profile_picture)
    if username is not None:
        updates.append("username = %s")
        params.append(username)
    if password is not None:
        updates.append("password = %s")
        params.append(password)

    if updates:
        update_query = f"UPDATE player_profiles SET {', '.join(updates)} WHERE player_id = %s"
        params.append(player_id)
        c.execute(update_query, tuple(params))

def delete_player_profile(player_id):
    c.execute("""
    DELETE FROM player_profiles WHERE player_id = %s
    """, (player_id,))

def add_friend(player_id, friend_id, friend_username):
    c.execute("""
    UPDATE player_profiles SET friend_list[%s] = %s WHERE player_id = %s
    """, (friend_id, friend_username, player_id))

def main():
    player_id = create_player_profile(
        achievements=['First Kill', 'Top Scorer'],
        email='malak@example.com',
        friend_list={generate_unique_player_id(): 'friend1'},
        inventory={'sword': 1, 'shield': 1},
        profile_picture='http://ndbbvf.com/profile.jpg',
        username='destroyer',
        password='axe'
    )
    print(f"Created player profile with ID: {player_id}")

    # Retrieving the player profile
    profile = get_player_profile(player_id)
    print(f"Retrieved player profile: {profile}")

    # Updating the player profile
    update_player_profile(player_id, achievements=['First Kill', 'Top Scorer', 'Champion'])
    profile = get_player_profile(player_id)
    print(f"Updated player profile: {profile}")

    # Adding a friend to the friend list
    new_friend_id = generate_unique_player_id()
    add_friend(player_id, new_friend_id, 'newfriend')
    profile = get_player_profile(player_id)
    print(f"Added friend to player profile: {profile}")

    # Deleting the player profile
    delete_player_profile(player_id)
    print(f"Deleted player profile with ID: {player_id}")

main()