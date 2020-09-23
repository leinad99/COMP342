import socket

HOST = '127.0.0.1'
PORT = 50000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT));
    s.listen()
    print('Socket is listening at port ' + PORT)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            if data == b'7':
                conn.send(b"hey now, it's jackpot day')
            if data == b'q':
                conn.close()