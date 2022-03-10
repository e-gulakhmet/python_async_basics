# Корутина - генераторы, которые в процессе работы могут принимать из вне какие-то данные


def coroutine(func):
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        f.send(None)
        return f
    return wrapper


def subgen():
    for i in 'enes':
        yield i


def delegator(g):
    for i in g:
        yield i


# sg = subgen()
# d = delegator(sg)
# next(d)
# 'e'
# next(d)
# 'n'
