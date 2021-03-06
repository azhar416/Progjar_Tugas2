import socket, ssl
import re

HOST = 'google.com'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = context.wrap_socket(client_socket, server_hostname=HOST)
server_address = (HOST, 443)
client_socket.connect(server_address)

request_header = f'GET / HTTP/1.0\r\nHost: {HOST}\r\n\Accept-Encoding: gzip, deflate, br\r\n\r\n'.encode('utf-8')
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')

response_header = response.split('\r\n\r\n')[0]
number_2 = re.match(r"([\s\S]* Content-Encoding=)(.*)", response_header)
if number_2:
    number_2 = number_2.group(2).strip()
    print("Content-Encoding : ", number_2)
else:
    print('Content-Encoding tidak ditemukan.')
