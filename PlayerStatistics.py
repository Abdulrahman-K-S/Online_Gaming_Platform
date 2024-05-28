from connection import c
import random

c.set_keyspace("game")

c.execute("""
CREATE TABLE IF NOT EXISTS player_statistics (
    player_id int PRIMARY KEY,
    combat_stats map<text, int>,
    resource_stats map<text, int>,
    progression_stats map<text, int>
)
""")

def initialize_player_statistics():
    return {
        'combat_stats': {'damage_dealt': 0, 'enemies_defeated': 0},
        'resource_stats': {'collection': 0, 'crafting_materials': 0},
        'progression_stats': {'levels': 1, 'quests_completed': 0, 'playtime_hours': 0}
    }

def update_combat_stats(player_stats, damage_dealt, enemies_defeated):
    player_stats['combat_stats']['damage_dealt'] += damage_dealt
    player_stats['combat_stats']['enemies_defeated'] += enemies_defeated

def update_resource_stats(player_stats, collection, crafting_materials):
    player_stats['resource_stats']['collection'] += collection
    player_stats['resource_stats']['crafting_materials'] += crafting_materials

def update_progression_stats(player_stats, levels=0, quests_completed=0, playtime_hours=0):
    player_stats['progression_stats']['levels'] += levels
    player_stats['progression_stats']['quests_completed'] += quests_completed
    player_stats['progression_stats']['playtime_hours'] += playtime_hours

def print_statistics(player_stats):
    print("Combat Stats:")
    for stat, value in player_stats['combat_stats'].items():
        print(f"- {stat.replace('_', ' ').capitalize()}: {value}")
    print("\nResource Stats:")
    for stat, value in player_stats['resource_stats'].items():
        print(f"- {stat.replace('_', ' ').capitalize()}: {value}")
    print("\nProgression Stats:")
    for stat, value in player_stats['progression_stats'].items():
        print(f"- {stat.replace('_', ' ').capitalize()}: {value}")

def get_player_statistics(player_id):
    result = c.execute("""SELECT combat_stats, resource_stats, progression_stats FROM player_statistics WHERE player_id = %s""", (player_id,))
    row = result.one()
    if row:
        return {
            'combat_stats': dict(row.combat_stats),
            'resource_stats': dict(row.resource_stats),
            'progression_stats': dict(row.progression_stats)
        }
    else:
        return None


def generate_dummy_statistics():
    combat_stats = {'damage_dealt': random.randint(100, 1000), 'enemies_defeated': random.randint(50, 200)}
    resource_stats = {'collection': random.randint(500, 1000), 'crafting_materials': random.randint(100, 500)}
    progression_stats = {'levels': random.randint(1, 50), 'quests_completed': random.randint(10, 100), 'playtime_hours': int(random.uniform(10, 100))}
    return combat_stats, resource_stats, progression_stats

def create_dummy_statistics(player_id):
    combat_stats, resource_stats, progression_stats = generate_dummy_statistics()
    c.execute("""
    INSERT INTO player_statistics (player_id, combat_stats, resource_stats, progression_stats)
    VALUES (%s, %s, %s, %s)
    """, (player_id, combat_stats, resource_stats, progression_stats))


def main():
    player_id = 4  
    create_dummy_statistics(player_id)
    player_stats = get_player_statistics(player_id)
    if player_stats:
        print(f"Player {player_id} Statistics:")
        print_statistics(player_stats)
    else:
        print("Player statistics not found.")

main()
