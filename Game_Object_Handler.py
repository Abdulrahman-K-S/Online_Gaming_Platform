from connection import c as cassandra
import uuid


# Functions
def insert_game_object(game_id, object_id, obj_type, pos_x, pos_y, pos_z, attributes):
    query = """
    INSERT INTO GameObject (game_id, object_id, type, position_x, position_y, position_z, attributes)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cassandra.execute(query, (game_id, object_id, obj_type, pos_x, pos_y, pos_z, attributes))

def get_game_objects(game_id):
    query = "SELECT * FROM GameObject WHERE game_id = %s"
    rows = cassandra.execute(query, (game_id,))
    return rows

def delete_game_object(game_id, object_id):
    query = "DELETE FROM GameObject WHERE game_id = %s AND object_id = %s"
    cassandra.execute(query, (game_id, object_id))
    
# Example usage
game_id = uuid.uuid4()
object_id = "AKM"

# Insert data
insert_game_object(game_id, object_id, 'Weapon', 200, 5, 0, {'ammoCapacity': '30', 'damage': '55', 'recoil' : '+15'})

# Query data
objects = get_game_objects(game_id)
for obj in objects:
    print(obj)
    
delete_game_object(game_id, object_id)