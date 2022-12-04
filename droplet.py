from utils import randChunkNums

import json
import random

class Droplet:
    def __init__(self, data, seed, total_chunks):
        self.data = data
        self.seed = seed
        self.total_chunks = total_chunks

    def chunkNums(self):
        random.seed(self.seed)
        return randChunkNums(self.total_chunks)

    def toString(self):
        return json.dumps(
            {
                'seed':self.seed,
                'total_chunks':self.total_chunks,
                'data':self.data
            })
