from connection import c as cassandra
import uuid

# Functions
def insert_game_info(game_id, name, game_type, current_state, world_layout):
    query = """
    INSERT INTO GameInfo (game_id, name, type, current_state, world_layout)
    VALUES (%s, %s, %s, %s, %s)
    """
    cassandra.execute(query, (game_id, name, game_type, current_state, world_layout))
    
def get_game_info(game_id):
    query = "SELECT * FROM GameInfo WHERE game_id = %s"
    row = cassandra.execute(query, (game_id,)).one()
    return row

def delete_game_info(game_id):
    query = "DELETE FROM GameInfo WHERE game_id = %s"
    cassandra.execute(query, (game_id,))
    
def game_exists(game_id):
    query = "SELECT * FROM GameInfo WHERE game_id = %s"
    result = cassandra.execute(query, (game_id,))
    
    # Check if any rows are returned
    if result.one() is not None:
        return True
    else:
        return False
    
# Example usage
game_id = uuid.uuid4()

# Insert data
insert_game_info(game_id, 'PUBG', 'Battleground', 'ongoing', '{"map": ["Miramar", "Erangel", "Vekindi"], \
                 "modes": ["Classic", "Arcade", "Team Deathmatch"]}')

# Query data
info = get_game_info(game_id)
print(info)

delete_game_info(game_id)

exist = game_exists(uuid.UUID('e039cb6b-9822-40bb-9ff4-b7c3f3364e87'))
print(exist)