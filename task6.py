import redis

r = redis.Redis(host='localhost', port=6379)


class Incr:
    def __init__(self, key: str):
        self.key: str = key
        self.val: int

    def increment_counter(self):
        r.set(self.key, int(r.get(self.key)) + 1)

    def get_counter(self):
        if r.get(self.key) is None:
            return 0
        return r.get(self.key)


if __name__ == '__main__':
    incr = Incr('counter1')
    print(incr.get_counter())
    incr.increment_counter()
    incr.increment_counter()
    print(incr.get_counter())
    incr.increment_counter()
    print(incr.get_counter())
