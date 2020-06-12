import socket
import time
def main():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 6000
    BUFFER_SIZE = 1024
    
    s = socket.socket()
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    connection, address = s.accept()
    print('started')
    word_list = ['free~', '1~', '2~']
    time.sleep(10)
    while True:
        connection.send('0.100_0.200_0.100~'.encode('utf-8'))
        time.sleep(3)
    s.close()
if __name__ == '__main__':
    main()