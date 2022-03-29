import socket, ssl
from bs4 import BeautifulSoup

HOST = 'classroom.its.ac.id'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = context.wrap_socket(client_socket, server_hostname=HOST)
server_address = (HOST, 443)
client_socket.connect(server_address)

request_header = f'GET https://classroom.its.ac.id/ HTTP/1.0\r\nHost: {HOST}\r\n\r\n'.encode('utf-8')
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')


body = response.split('\r\n\r\n')[1]
soup = BeautifulSoup(body)
dropdown = soup.find_all("li", class_="dropdown")
for item in dropdown:
  a_block = item.find_all('a')
  for a in a_block:
    text = a.get_text().strip()
    print(text)
    

    
