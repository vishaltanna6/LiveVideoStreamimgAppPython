import cv2, socket, pickle, os,threading
def send():
    s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
    serverip="192.168.0.109" #Server IP
    serverport=3000          #Server Port
    cap = cv2.VideoCapture(1)
    while True:
        ret,photo = cap.read()            
        ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY),30])
        img_bytes = pickle.dumps(buffer)
        s.sendto(img_bytes,(serverip , serverport))
        cv2.namedWindow('2_send', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('2_send', 180,180)
        cv2.imshow('2_send', photo)
        if cv2.waitKey(10) == 13:
            cap.release()
            break    
            
    cv2.destroyAllWindows()

def recv():
    sr=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    ip="192.168.0.109"      #Host IP
    port=3050               #Host Port
    sr.bind((ip,port))
    
    while True:
        x=sr.recvfrom(100000000)
        if x == 0:
            pass
        else:
            # print(x)
            clientip = x[1][0]
            data=x[0]
            # print(data)
            data=pickle.loads(data)
            # print(type(data))
            data = cv2.imdecode(data, cv2.IMREAD_COLOR)
            cv2.imshow('2_recv', data) 
            if cv2.waitKey(10) == 13:
                break
    cv2.destroyAllWindows()



t1 = threading.Thread(target=send)
t2 = threading.Thread(target=recv)
t1.start()
t2.start()
