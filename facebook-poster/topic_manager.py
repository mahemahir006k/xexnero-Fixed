import json
import random
import os
import time

TOPIC_FILE = "topics.json"


class TopicManager:

    _data_cache = None
    _data_cache_time = 0

    def __init__(self):
        if not os.path.exists(TOPIC_FILE):
            raise FileNotFoundError(f"{TOPIC_FILE} not found.")

    def _load(self):
        now = time.time()
        if self.__class__._data_cache is not None and now - self.__class__._data_cache_time < 60:
            return json.loads(json.dumps(self.__class__._data_cache))

        with open(TOPIC_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.__class__._data_cache = data
        self.__class__._data_cache_time = now
        return json.loads(json.dumps(data))

    def _save(self, data):
        with open(TOPIC_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.__class__._data_cache = data
        self.__class__._data_cache_time = time.time()

    def get_next_topic(self):

        data = self._load()

        topics = data["topics"]
        used = data["used"]

        remaining = [t for t in topics if t not in used]

        if not remaining:
            data["used"] = []
            remaining = topics

        topic = random.choice(remaining)

        data["used"].append(topic)

        self._save(data)

        return topic

    