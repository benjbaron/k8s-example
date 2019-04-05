#!/usr/bin/env python

import os
import sys
import time
import rediswq
import random

host="redis"
# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")

print(os.environ)

nb_items = 10
if len(sys.argv) > 1:
    nb_items = int(sys.argv[1])

q = rediswq.RedisWQ(name="job2", host="redis")
print("Worker with sessionID: " +  q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))
print("Adding %d items to the work queue" % nb_items)

fruits = ['banana', 'cherry', 'apple', 'strawberry', 'raspberry', 'plum']

for i in range(nb_items):
    fruit = random.choice(fruits)
    q.put(fruit)
    print("Added " + fruit)

print("Done adding items")
