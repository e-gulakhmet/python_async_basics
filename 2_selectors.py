# https://www.youtube.com/watch?v=ikKGMp4jb_o&list=PLlWXhlUMyooawilqK4lPXRvxtbYiw34S8&index=3

import socket
import selectors


selector = selectors.DefaultSelector()


def server():
    ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser_socket.bind(('localhost', 5000))
    ser_socket.listen()

    print('Регистрируем селектор серверного сокета')
    selector.register(ser_socket, selectors.EVENT_READ, data=accept_connection)
    print('Готово\n')


def accept_connection(server_socket: socket.socket):
    client_socket, address = server_socket.accept()
    print("Новое подключение от:", address)
    print('Регистрируем селектор клиентского сокета')
    selector.register(client_socket, selectors.EVENT_READ, send_message)
    print('Готово\n')


def send_message(client_socket: socket.socket):
    request = client_socket.recv(4096)
    print('Получено новое сообщение по клиентскому сокету:', request)
    if request:
        print('Отправляю новое сообщение', '\n')
        client_socket.send('HelloWorld'.encode())
    else:
        print('Сообщение не получено, закрываю клиентский сокет', '\n')
        print('Удаляем селектор клиентского сокета')
        selector.unregister(client_socket)
        print('Готово\n')


def event_loop():
    print('event_loop')
    while True:
        print('Получаем список картежей, под одному на каждый зарегистрированный объекты, который доступен для чтения')
        events = selector.select()
        for key, _ in events:
            callback = key.data  # Функция, которую нужно вызвать
            callback(key.fileobj)  # key.fileobj - сокет, который стал открыт для чтения


if __name__ == '__main__':
    server()
    event_loop()
