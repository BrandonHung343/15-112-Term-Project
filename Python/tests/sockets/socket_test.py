import sys, socket
def main():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 4000
    BUFFER_SIZE = 1024
    
    sys.stdout.write("It has begun \n")
    s = socket.socket()
    s.bind((TCP_IP, TCP_PORT))
    sys.stdout.write("Listening on point " + TCP_IP + '\n')
    s.listen(1)
    
    connection, address = s.accept()
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag
    sys.stdout.write("It has begun \n")
    sys.stdout.flush()
    
    while True:
        connection.send("Hello World")

if __name__ == '__main__':
    main()