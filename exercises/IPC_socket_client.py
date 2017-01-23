import socket

sock = socket.socket()
sock.connect(('localhost', 9999))
sock.send(b'abde')
data = sock.recv(128)
sock.close()

print(data)
