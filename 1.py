import socket, ssl

HOST = 'its.ac.id'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = context.wrap_socket(client_socket, server_hostname=HOST)
server_address = (HOST, 443)
client_socket.connect(server_address)

request_header = f'GET https://www.its.ac.id/ HTTP/1.0\r\nHost: {HOST}\r\n\r\n'.encode('utf-8')
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')

response_header = response.split('\r\n\r\n')[0]
header_status = response_header.splitlines()[0].split(' ')
print(f'{header_status[1]} {header_status[2]}')
