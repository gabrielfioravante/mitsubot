import os, random

class AudioQueue:
    def __init__(self):
        self.Q = []
        self.fill()
        
    def enqueue(self, audio_file: str):
        self.Q.append(audio_file)
        
    def dequeue(self): 
        if len(self.Q) > 1:
            self.Q.pop(0)
        else:
            self.fill()

    def front(self) -> str:
        return self.Q[0]

    def fill(self):
        self.Q = os.listdir('./audio')
        random.shuffle(self.Q)

    def get_formatted(self) -> str:
        return '\n'.join(self.Q)
