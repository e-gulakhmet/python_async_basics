# Корутина - генераторы, которые в процессе работы могут принимать из вне какие-то данные


def coroutine(func):
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        f.send(None)
        return f
    return wrapper


@coroutine
def average():
    count = 0
    summ = 0
    avg = None

    print('Прошла инициализация \n')
    while True:
        try:
            print('Возвращаем avg и останавливаемся до следующего вызова send()')
            x = yield avg
            print(f'Получили x={x}')
        except StopIteration:
            print('Готово')
            break
        else:
            print('Работаем с полученным x')
            count += 1
            summ += x
            avg = round(summ / count)

    # При вызове StopIteration можно получить значение avg, если сделать:
    # try:
    #   g.throw(StopIteration)
    # except StopIteration as e:
    #   print(e.value)
    return avg
