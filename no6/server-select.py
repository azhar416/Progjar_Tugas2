from urllib.parse import unquote
import socket
import configparser
import select
import sys
import os

config = configparser.RawConfigParser()
cfg_path = 'no6/httpserver.conf'
config.read(cfg_path)

server_address = (config.get('server-config', 'server'), int(config.get('server-config', 'port')))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

DATASET = 'no6/dataset'
def listFiles():
    files = next(os.walk(DATASET), (None, None, []))[2]
    message = ""
    for idx, f in enumerate(files):
        message += f"<li><h5><a href='/{f}'>{f}</a></h3></li>\n"
    return message

def getContentType(extension):
  with open('no6/ext2mime.txt') as topo_file:
    for line in topo_file:
        ext = line.split(' ')[0]
        if extension == ext:
            return line.split(' ')[1]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)                       
            
            else:                
                # receive data from client, break when null received          
                data = sock.recv(4096)
                # print(data)
                
                data = data.decode('utf-8')
                # print("data: ", data)
                request_header = data.split('\r\n')
                # print("request header: ", request_header)
                request_file = request_header[0].split()[1]
                print("request file: ", request_file)
                response_header = b''
                response_data = b''
                
                if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
                    f = open('no6/index.html', 'r')
                    response_data = f.read()
                    f.close()
                    
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_length) + '\r\n\r\n'

                    sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                elif (request_file == '/dataset' or request_file == 'dataset'):
                    print('WOKE!')
                    response_data = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    </head>
                    <body>
                    <h1>
                    DATASET
                    <h1>
                    <ul>
                    """
                    response_data += listFiles()
                    response_data += """<ul>
                    </body>
                    </html>"""
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_length) + '\r\n\r\n'
                    sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                else:
                    request_file = unquote(request_file)
                    if (os.path.isfile(DATASET+request_file)):
                        # print('WOKEE!')
                        f = open(DATASET+request_file, 'rb')
                        response_data = f.read()
                        f.close()

                        # f = open("/ext2mime.txt")
                        filename = request_file.split('.')[0].strip('/')
                        print("filename : ", filename)
                        extension = request_file.split('.')[1]
                        extension = '.' + extension
                        print("extension : ", extension)
                        content_type = getContentType(extension)
                                # print(line)  # The comma to suppress the extra new line char

                        content_length = len(response_data)
                        response_header = f'HTTP/1.1 200 OK\r\nContent-Disposition: attachment; filename="{filename}{extension}"\r\nContent-Type: {content_type}; charset=UTF-8\r\nContent-Length:' \
                                            + str(content_length) + '\r\n\r\n'
                        sock.sendall(response_header.encode('utf-8') + response_data)
                        
                    else:
                        f = open('no6/404.html', 'r')
                        response_data = f.read()
                        f.close()
                        
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                        + str(content_length) + '\r\n\r\n'
                                        
except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)
