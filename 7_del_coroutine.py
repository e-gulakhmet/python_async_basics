# Корутина - генераторы, которые в процессе работы могут принимать из вне какие-то данные


def init_as_coroutine(func):
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        f.send(None)
        return f
    return wrapper


@init_as_coroutine
def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print('......', message)
    return 'Return from subgen'


@init_as_coroutine
def delegator(g):
    while True:
        try:
            data = yield
            g.send(data)
        except:
            pass
    # yield from g


@init_as_coroutine
def yield_from_delegator(g):
    result = yield from g
    print(result)
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except:
    #         pass


# sg = subgen()
# d = delegator(sg)
# d.send('Ok')
# .......... Ok