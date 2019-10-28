import socket
import base64
import time
import hashlib

HOST = '127.0.0.1'
PORT = 23455

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT))
server.listen(5)

sendOUT = 0

while True:
    conn, addr = server.accept() #accept
    print("Connected by", addr)
    now = time.localtime()
    encodedData = ''
    while True:
        start = time.time() #เริ่มจับเวลา
        indata = conn.recv(1024) #รับมาทีละ1024
        if indata is None : 
            # print(indata is None)
            break
        if len(indata) == 0:
            # print(len(indata) == 0)
            break
        data = repr(indata.decode()) #แปลง object -> string
        data = data[1:len(data)-1] #ตัด ' ' หัวท้ายออก
        print('{{ {}'.format(data[0]))
        print(data[1:len(data)-32])
        print('{} }}'.format(data[-32:]))
        check = hashlib.md5(bytes(data[:len(data)-32], 'utf-8')).hexdigest() == data[-32:] #ตรวจสอบความถูกต้องของข้อมูล
        color = '\033[92m' if check else '\033[91m'
        print('Verification = {} {} '.format(color, check)+'\033[0m')
        if check:
            processedText = data[1:len(data)-32].lower() #แปลงเป็นตัวเล็ก
            conn.sendall(bytes(data[0]+processedText+hashlib.md5(bytes(data[0]+processedText, 'utf-8')).hexdigest(), 'utf-8')) #ส่งข้อมูลกลับไป
            end = time.time() #หยุดการจับเวลา
            print('Total Time = {} seconds'.format(end-start)) #แสดงเวลา
        else:
            conn.sendall(bytes('NACK()', 'utf-8')) #ส่ง NACK เพื่อขอข้อมูลใหม่
            print('Send NACK({}) signal to secondary'.format(data[0]))
        
        
