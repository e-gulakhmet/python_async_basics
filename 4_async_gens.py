import socket
from pprint import pprint
from select import select

tasks = []

to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        print('Возвращаем сокет сервера')
        yield 'read', server_socket
        print()
        print('Открываем сокет подключения к клиенту')
        client_socket, address = server_socket.accept()
        print("Новое подключение от:", address)
        # Добавляем генераторную функцию для работы с клинтским сокетом,
        # для обработки конекта с клиентом
        tasks.append(client(client_socket))


def client(client_socket: socket.socket):
    while True:

        print('Возвращаем клиентский сокет для чтения')
        yield 'read', client_socket
        print()
        request = client_socket.recv(4096)
        print('Получено новое сообщение по клиентскому сокету:', request)
        if not request:
            break
        else:
            print('Возвращаем клиентский сокет для написания')
            yield 'write', client_socket
            print('Отправляю новое сообщение', '\n')
            client_socket.send('HelloWorld'.encode())


def event_loop():
    print('Зашли в event_loop \n')
    while any([tasks, to_read, to_write]):

        while not tasks:
            print('Список тасок пустой')
            print('Получаем от select, сокеты, с которыми можно взаимодействовать')
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            # Если какой-то из сокетов готов для чтения или написания, то добавляем этот сокет в список тасок,
            # чтобы потом выполнить ее
            # При этом удаляем этот сокет из списка to_read сокетов, так как он будет выполняться
            for sock in ready_to_read:
                print('Новая таска для чтения')
                tasks.append(to_read.pop(sock))
                print()

            for sock in ready_to_write:
                print('Новая таска для написания')
                tasks.append(to_write.pop(sock))
                print()

        try:
            print('Получаем первую таску из списка тасок')
            task = tasks.pop(0)
            print('Удаляем таску из списка тасок и получаем ее:', task)

            print(' --------- Выполняем таску ---------')
            reason, sock = next(task)
            print('---------- Таска выполнена --------')
            print('Ответ от полученной таски:', reason, ', сокет:', sock, '\n')

            # Задача выполнена, теперь нужно добавить новый сокет в список сокетов с генераторной функцией,
            # которая работает с этим сокетом для чтения или написания
            if reason == 'read':
                print('Добавляем полученный сокет в список сокетов для чтения')
                to_read[sock] = task
            if reason == 'write':
                print('Добавляем полученный сокет в список сокетов для написания')
                to_write[sock] = task

            print('После прохождения по таске получаем:')
            print('to_read:')
            pprint(to_read)
            print('to_write:')
            pprint(to_write)
            print()
        except StopIteration:
            pass


if __name__ == '__main__':
    tasks.append(server())
    event_loop()
