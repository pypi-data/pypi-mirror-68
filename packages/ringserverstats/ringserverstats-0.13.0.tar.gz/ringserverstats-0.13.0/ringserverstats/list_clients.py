from ringserverstats import parse_ringserver_log
import sys

"""
Open stdin and analyse it. Output a list of
"""

events = parse_ringserver_log(''.join(sys.stdin.readlines()))

clients = {}

for e in events:
    if e['client'] in clients.keys():
        clients[e['client']] += 1
    else:
        clients[e['client']] = 0

clients = {k: v for k, v in sorted(clients.items(), key=lambda item: item[1])}

for c in clients.keys():
  print("%4d  %s"%(clients[c], c))
