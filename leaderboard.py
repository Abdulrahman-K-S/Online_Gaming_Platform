# Connect to Redis
from connection import r as redis


def add_score(game_id ,leaderboard, username, score):
    """
    Add score to the specified leaderboard.

    Args:
    - leaderboard: Name of the leaderboard.
    - username: Username of the player.
    - score: Score to be added.
    """
    redis.zadd(f'game:{game_id}:leaderboard:{leaderboard}', {username: score})

def get_top_scorers(leaderboard, num_top=3):
    """
    Retrieve top scorers from the specified leaderboard.

    Args:
    - leaderboard: Name of the leaderboard.
    - num_top: Number of top scorers to retrieve (default is 3).

    Returns:
    - List of tuples containing (username, score) for top scorers.
    """
    return redis.zrevrange(f'leaderboard:{leaderboard}', 0, num_top - 1, withscores=True)

def print_top_scorers(leaderboard, num_top=3):
    """
    Print top scorers from the specified leaderboard.

    Args:
    - leaderboard: Name of the leaderboard.
    - num_top: Number of top scorers to print (default is 3).
    """
    top_scorers = get_top_scorers(leaderboard, num_top)
    print(f"Top Scorers - {leaderboard.capitalize()}:")
    for rank, (username, score) in enumerate(top_scorers, start=1):
        print(f"{rank}. {username}: {score}")

# Example usage:
add_score(920, 'points', 'user1', 100)
add_score(24, 'points', 'user2', 80)
add_score(255, 'points', 'user3', 70)

add_score(150, 'kills', 'user2', 50)
add_score(820, 'kills', 'user1', 45)
add_score(1200, 'kills', 'user3', 40)

add_score(5, 'levels', 'user2', 30)
add_score(60, 'levels', 'user1', 25)
add_score(620, 'levels', 'user3', 20)

add_score(1500, 'gold', 'user2', 500)
add_score(300, 'gold', 'user1', 400)
add_score(22, 'gold', 'user3', 100)

print_top_scorers('points')
print_top_scorers('kills')
print_top_scorers('levels')
print_top_scorers('gold')

