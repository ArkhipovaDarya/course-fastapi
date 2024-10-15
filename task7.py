import redis

r = redis.Redis(host='localhost', port=6379)


class Todos:
    def __init__(self, key: str):
        self.key = key

    def add_task(self, todo):
        r.lpush(self.key, todo)

    def get_tasks(self):
        return [element.decode('utf-8') for element in r.lrange(self.key, 0, -1)]

    def remove_task(self, todo):
        r.lrem(self.key, 0, todo)


if __name__ == '__main__':
    task = Todos('tasks1')
    print(task.get_tasks())
    task.add_task("first task")
    print(task.get_tasks())
    task.add_task("second task")
    print(task.get_tasks())
    task.remove_task("first task")
    print(task.get_tasks())
