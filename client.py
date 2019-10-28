import socket
import base64
import hashlib

class Frame:
    seq = b''
    data = b''
    checksum = b''

    def __init__(self, sequen, dataFrame):
        print(dataFrame)
        self.seq = bytes(str(sequen), 'utf-8')
        self.data = bytes(dataFrame, 'utf-8')
        self.checksum = bytes(hashlib.md5(self.seq+self.data).hexdigest(), 'utf-8')

HOST = '127.0.0.1'
PORT = 23455
byteStr = open('./client data/text.txt', "r").read()

# print(allbyte)
# print(str(allbyte))

# byteStr = str(allbyte)[1:]
# byteStr = byteStr[:-1]

Time = 0.002
print(byteStr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

totalSend = 0
success = 0
sumData = ''
seq = 1 #รอบการส่ง
while(len(byteStr) != 0): #เช็คว่าข้อมูลยังเหลือไหม
    data = Frame(seq, byteStr[:7]) #data สร้าง object ใส่ลำดับ และ ข้อมูล0-8byte
    # print(byteStr[:7])
    # sumData += data.data
    try:
        # print(type(data.seq))
        print(data.seq+data.data+data.checksum) #printดูข้อมูลใน data
        if totalSend % 2 == 1: #%2ทำให้เกิดerror โดยการกำหนดค่า checksum มั่ว
            data.checksum = b'12345678901234567890123456789012'
        server.send(data.seq+data.data+data.checksum) #ส่งข้อมูล

        # print("Receiving return data")
        server.settimeout(Time) #กำหนด Timeout ในการส่งข้อมูล
        send = 0
        getData = server.recv(1024)
        send = 1
        success = success + 1
        totalSend = totalSend + 1
    except socket.timeout as e:
        print('\033[92mTimeout\033[0m, Send previous Frame again!!!!!!!!!!!!!!!!!!')
        if send != 1:
            server.settimeout(1)
            trash = server.recv(1024)
            server.settimeout(Time)
            totalSend = totalSend + 1
        continue
    getDataStr = repr(getData.decode()).replace('\'','')
    if getDataStr == 'NACK()':
        print('>>>>>>>>>>>>> \033[91m Send again \033[0m')
        # seq = seq-1
        continue
    print("Return >>>")
    print(getDataStr)
    check = hashlib.md5(bytes(getDataStr[:len(getDataStr)-32], 'utf-8')).hexdigest() == getDataStr[-32:]
    if check:
        sumData = sumData + getDataStr[1:len(getDataStr)-32]
        seq = seq+1
        byteStr = byteStr[7:]
    else:
        continue
server.close()   
print('Exit, success \033[92m{}\033[91m / \033[93m{}\033[0m'.format(success, totalSend))
print(sumData)
