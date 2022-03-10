import socket
from select import select


ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ser_socket.bind(('localhost', 5000))
ser_socket.listen()

to_monitor = []


# У нас есть один процесс, который может выполняться это ser_socket, добавляем его в to_monitor.]
# Ждем пока ему нужно будет выполниться.
# Если подключается новый клиент, то в ready_to_read появляется ser_socket.
# Затем проходимся по каждому сокету в ready_to_read, видим, что полученный сокет является ser_socket.
# Выполняем функцию создания клиентского сокета, чтобы держать коннект с клиентом.
# Затем добавляем этот сокет в список to_monitor.
# Теперь у нас есть клиентский сокет и серверный, получаем, что если какой-то новый пользователь подключается к серверу,
# то мы создаем новый клиентский сокет, закидываем его в to_monitor, если какой-то из наших сокетов готов для чтения
# нами, то select вернет нам его.
# Таким образом мы смогли реализовать асинхронность, так как процессы теперь не завязаны друг на друге, они могут
# выполняться независимо друг от друга
# Если придет коннект от нового компа, нам не нужно ждать пока прекратиться коннект с прошлым клиентом, мы просто
# создадим новый, а клиентский просто будет лежать, пока коннект с прошлым клиентом существует

def accept_connection(server_socket: socket.socket):
    client_socket, address = server_socket.accept()
    print("Новое подключение от:", address)
    print("Добавляю новый процесс в to_monitor:", address, '\n')
    to_monitor.append(client_socket)


def send_message(client_socket: socket.socket):
    request = client_socket.recv(4096)
    print('Получено новое сообщение по клиентскому сокету:', request)
    if request:
        print('Отправляю новое сообщение', '\n')
        client_socket.send('HelloWorld'.encode())
    else:
        print('Сообщение не получено, закрываю клиентский сокет', '\n')
        client_socket.close()


def event_loop():
    print('event_loop')
    while True:
        print('Получаем открытые для чтения процессы')
        print('to_monitor', [obj.fileno() for obj in filter(lambda s: s.fileno(), to_monitor)])
        ready_to_read, _, _ = select(filter(lambda s: s.fileno(), to_monitor), [], [])
        print('ready_to_read', ready_to_read)

        print('Проходимся по каждому сокету в read_to_read')
        for sock in ready_to_read:
            print('sock', sock.fileno())
            if sock is ser_socket:
                print('Сокет является серверным сокетом')
                accept_connection(sock)
                print('Получили новое подключение', '\n')
            else:
                print('Сокет является клиентским сокетом')
                send_message(sock)
                print('Отправили сообщение клиенту', '\n')


if __name__ == '__main__':
    to_monitor.append(ser_socket)
    event_loop()
