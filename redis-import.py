from sys import argv
import redis

r = redis.StrictRedis()
print(argv[0])
print(argv[1])
with open(argv[1], "r") as f:
    names = f.readlines()
    names = [n.strip() for n in names]
    r.delete('restaurants')
    r.lpush('restaurants', *names)

