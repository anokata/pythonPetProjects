import socket
sock = socket.socket()
sock.bind(('', 9999))
sock.listen(1)
conn, addr = sock.accept()

data = conn.recv(128)
conn.send(data.upper())

conn.close()
