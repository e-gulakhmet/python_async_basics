# Вытаскивает таску из списка тасок, каждая таска является генератором.
# Запускает итерацию таски, тем самым запуская код внутри функции генератора
# Затем снова добавляет эту таску в конец список тасок
# Таким образом мы выполняем части тасок по очереди, переходя от одной таски к другой


def string_gen(value: str):
    for e in value:
        yield e


def int_get(value: int):
    for i in range(value):
        yield i


tasks = [string_gen('test'), int_get(10)]

while tasks:
    task = tasks.pop(0)

    try:
        v = next(task)
        print(v)
        tasks.append(task)
    except StopIteration:
        pass
