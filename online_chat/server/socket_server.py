# 文件名：server.py
import socket
import threading
import hashlib
import base64
import struct
import json
# import sys
# from os.path import abspath, join, dirname
from backend.views import url_map

# sys.path.insert(0, join(abspath(dirname(__file__))))
PRINT_LOG = False
GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


# 将由js提交的bytes类型的消息转为str
def bytes2str(msg):
    local_code_length = msg[1] & 127
    if local_code_length == 126:
        masks = msg[4:8]
        data = msg[8:]
    elif local_code_length == 127:
        masks = msg[10:14]
        data = msg[14:]
    else:
        masks = msg[2:6]
        data = msg[6:]
    en_bytes = b""
    cn_bytes = []
    for i, d in enumerate(data):
        nv = chr(d ^ masks[i % 4])
        nv_bytes = nv.encode()
        nv_len = len(nv_bytes)
        if nv_len == 1:
            en_bytes += nv_bytes
        else:
            en_bytes += b'%s'
            cn_bytes.append(ord(nv_bytes.decode()))
    if len(cn_bytes) > 2:
        cn_str = ""
        cn_len = len(cn_bytes)
        count = int(cn_len / 3)
        for x in range(count):
            i = x * 3
            b = bytes([cn_bytes[i], cn_bytes[i + 1], cn_bytes[i + 2]])
            cn_str += b.decode()  # 输入快了这个地方会报错，应该是buffer的原因
        new = en_bytes.replace(b'%s%s%s', b'%s')
        new = new.decode()
        rst = (new % tuple(list(cn_str)))
    else:
        rst = en_bytes.decode()
    return rst


# 根据js发送的报文计算code_length和header_length并返回
def calculate_data_length(msg):
    local_code_length = msg[1] & 127
    if local_code_length == 126:
        local_code_length = struct.unpack('>H', msg[2:4])[0]
        local_header_length = 8
    elif local_code_length == 127:
        local_code_length = struct.unpack('>Q', msg[2:10])[0]
        local_header_length = 14
    else:
        local_header_length = 6
    local_code_length = int(local_code_length)

    return local_code_length, local_header_length


# 握手请求中发送的Sec-WebSocket-Key的值，追加258EAFA5-E914-47DA-95CA-C5AB0DC85B11(固定值) ，采用新值的SHA-1，然后进行base64编码.
def generate_token(web_socket_key, guid):
    web_socket_key = web_socket_key + guid
    ser_socket_key = hashlib.sha1(web_socket_key.encode(encoding='utf-8')).digest()
    web_socket_token = base64.b64encode(ser_socket_key)  # 返回的是一个bytes对象
    return web_socket_token.decode('utf-8')


# 将消息加上标识信息，组合成报文
def generate_message(msg):
    send_msg = b"\x81"
    data_length = len(msg.encode('utf-8'))  # 可能有中文内容传入，因此计算长度的时候需要转为bytes信息
    # 数据长度的三种情况
    if data_length <= 125:  # 当消息内容长度小于等于125时，数据帧的第二个字节0xxxxxxx 低7位直接标示消息内容的长度
        send_msg += str.encode(chr(data_length))
    elif data_length <= 65535:  # 当消息内容长度需要两个字节来表示时,此字节低7位取值为126,由后两个字节标示信息内容的长度
        send_msg += struct.pack('b', 126)
        send_msg += struct.pack('>h', data_length)
    elif data_length <= (2 ^ 64 - 1):  # 当消息内容长度需要把个字节来表示时,此字节低7位取值为127,由后8个字节标示信息内容的长度
        send_msg += struct.pack('b', 127)
        send_msg += struct.pack('>q', data_length)
    else:
        print(u'太长了')
    if PRINT_LOG:
        print("INFO: send message: [%s]; len: %d(bytes)" % (msg, data_length))
    return send_msg + msg.encode('utf-8')


def web_socket_conn(sock, address):
    thread_name = threading.current_thread().name
    code_length = 0
    header_length = 0
    buffer_utf8 = b""
    length_buffer = 0
    print('INFO: Socket %s Started' % thread_name)
    print('INFO: Try shaking hands with the (%s, %s)... ' % address, end='')
    try:
        buffer = sock.recv(1024).decode('utf-8')  # sock.recv(1024)返回的是bytes，需要转换为str来解析
        buffer.index('\r\n\r\n')  # 握手请求报文，应该是以\r\n\r\n来分隔header和data（一般没有data），如果没有此分隔，则index()会抛出异常
        headers = {}
        header = buffer.split('\r\n\r\n', 1)[0]  # 按\r\n\r\n split一次,返回[header,data]
        meta_list = header.split("\r\n")
        request_path = meta_list[0].split(' ')[1]
        meta_list = meta_list[1:]  # header第一行是'GET / HTTP/1.1'，接下来不需要它
        for meta in meta_list:
            key, value = meta.split(": ", 1)  # 逐行的解析Request Header信息(Key,Value)
            headers[key] = value
        web_socket_key = headers["Sec-WebSocket-Key"]
        web_socket_token = generate_token(web_socket_key, GUID)
        headers["Location"] = "ws://%s%s" % (headers["Host"], request_path)
        handshake = "HTTP/1.1 101 Switching Protocols\r\n" \
                    "Connection: Upgrade\r\n" \
                    "Sec-WebSocket-Accept: " + web_socket_token + "\r\n" \
                    "Upgrade: websocket\r\n\r\n"
        sock.send(handshake.encode(encoding='utf-8'))
        print('success!')
    except Exception as e:
        print('failed! meet %s: %s' % (str(type(e)).split("'")[1], e.args[-1]))
        sock.close()

    else:
        while 1:
            msg = sock.recv(128)
            if code_length == 0:
                code_length, header_length = calculate_data_length(msg)
            length_buffer += len(msg)
            buffer_utf8 += msg
            if length_buffer - header_length < code_length:
                if PRINT_LOG:
                    print("INFO: The data is not fully received, continue")
                continue
            else:

                # if not buffer_utf8:
                #     continue
                receive_message = bytes2str(buffer_utf8)
                if PRINT_LOG:
                    print("INFO: Receive message: [%s]; len: %d(str)" % (receive_message, len(receive_message)))
                    print("INFO: code length: %d(bytes), header length: %d(bytes)" % (code_length, header_length))
                if receive_message == "EOT":  # 与前端约定好的终止信号，具体见js代码
                    # now_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
                    # sock.send(generate_message("[%s] %s,goodbye" % (now_time, address[0])))
                    print("INFO: Socket %s closed with signal: %s" % (thread_name, 'EOT'))
                    sock.close()
                    break
                else:
                    target_api = url_map(request_path)
                    backend_resp = target_api({'address': address, 'params': receive_message})
                    if backend_resp.get('status_code') == 5000:
                        print("INFO: Socket %s closed with signal: %s" % (thread_name, backend_resp.get('message')))
                        sock.close()
                        break
                    else:
                        sock.send(generate_message(json.dumps(backend_resp)))
                code_length = 0
                length_buffer = 0
                buffer_utf8 = b""


# WebSocket服务器对象
class WebSocketServer():
    def __init__(self, ip='127.0.0.1', port=9000, thread_num=50):
        self.socket = None
        self.ip = ip
        self.port = port
        self.thread_num = thread_num

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(self.thread_num)
        print('INFO: WebSocketServer Started')
        print('INFO: Server is listening at %s:%d, Maximum number of available connections:%d' %
              (self.ip, self.port, self.thread_num)
        )

        while 1:
            connection, address = self.socket.accept()
            t = threading.Thread(target=web_socket_conn, args=(connection, address))
            t.start()


if __name__ == '__main__':
    my_server = WebSocketServer()
    my_server.start()