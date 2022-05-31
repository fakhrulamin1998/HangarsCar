import cv2, imutils, socket
import numpy as np
import time
import base64
import threading
import order_transfer
import motor_control

BUFF_SIZE = 75000
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '169.254.55.222'#  change this for your Raspberry Pi IP
print(host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)




#####



message=b'Hello'
def vid_send():
    vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
    fps,st,frames_to_count,cnt = (0,0,20,0)
    current_distance = 350
    T1_start = 0
    T1_check = False

    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        #print(msg.decode())
        WIDTH=400
        while(vid.isOpened()):
            try:
                _,frame = vid.read()
                frame = imutils.resize(frame,width=WIDTH)
                encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                message = base64.b64encode(buffer)
                server_socket.sendto(message,client_addr)
                #frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                #cv2.imshow('TRANSMITTING VIDEO',frame)
            except:
                print("err vid tr")
                continue
            try:
                t=threading.Thread(target=order_transfer.order_recv)
                t.start()
                
            
                #order_transfer.order_recv()
            except:
                continue
            
            try:
                #To RUN OBJECT DETECT SENSOR
                #print('Test Test Test')
                print("Distance: "+str(current_distance)+" cm")
                
                if T1_check == False:
                    T1_start = time.time()
                    T1_check = True
            
                if time.time() - T1_start >= 0.5 and T1_check == True:
                    #print('Check Check Check Check')
                    T1_check = False
                    current_distance = motor_control.object_detect2()
                    
            except:
                continue
            
            
            #key = cv2.waitKey(1) & 0xFF
            
            
            #if key == ord('q'):
                #server_socket.close()
                #break
            #if cnt == frames_to_count:
                #try:
                    #fps = round(frames_to_count/(time.time()-st))
                    #st=time.time()
                    #cnt=0
                #except:
                    #pass
            #cnt+=1
            
                
"""            
def order():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,1024)
    host_name2=socket.gethostname()
    host_ip2 = '192.168.1.36'#  socket.gethostbyname(host_name)
    print(host_ip2)
    port2 = 9999+1
    socket_address2 = (host_ip2,port2)
    while True:
        try:
            print("tt")
            msg2,_i = client_socket.recvfrom(1024)
            print(msg2.decode('utf-8'))
            print("112323433432")
        except:
            print(777)
"""            
"""
t1=threading.Thread(target=vid_send)
#t2=threading.Thread(target=order)
#t2=threading.Thread(target=order_transfer.order_recv)
t1.start()

#t2.start()
"""
vid_send()