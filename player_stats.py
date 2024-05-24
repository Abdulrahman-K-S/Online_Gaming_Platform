from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
session = cluster.connect('userspace')

res = session.execute('SELECT * FROM userspace.users;')

playerdict = {}

for row in res:
    print(row)

# def login(player_id):
#     pass # start monitoring playtime

# def logout(player_id):
#     pass # accumulate playtime

# def pickup_item(player_id, item_id):
#     pass # put item in inventory and get +5 Exp

# def kill_enemy(player_id, points):
#     pass # increment kills and get +points Exp
    
# def main():
#     # player 1 logs in,
#     #  picks up sword (item_id=1234) (show inventory),
#     #  kills an enemy to get 10 Exp (show exp),
#     #  then logs out (show total playtime).
#     # do the above logic twice.

session.shutdown()
cluster.shutdown()