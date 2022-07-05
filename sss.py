from collections import defaultdict

channel_ids = {}
channel_ids['viewCount']='3323'
channel_ids = defaultdict(lambda: 0, channel_ids)
print(channel_ids['sub'])