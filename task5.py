import redis

r = redis.Redis(host='localhost', port=6379)


class KeyWorker:
    def __init__(self, key: str):
        self.key = key

    def set_value(self, value: str):
        r.set(self.key, value)

    def get_value(self):
        return r.get(self.key)

    def delete_value(self):
        return r.delete(self.key)


if __name__ == '__main__':
    kw = KeyWorker('keeey')
    kw.set_value('vaaal')
    print(kw.get_value())
    kw.delete_value()
    print(kw.get_value())
