class Counter:
    def __init__(self):
        self.n = 0
    def add(self, x):
        self.n += x
    def value(self):
        return self.n

# walrus example
if (n := 5) > 3:
    pass
