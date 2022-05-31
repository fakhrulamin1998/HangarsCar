import cv2, imutils, socket
import numpy as np
import time
import base64
import threading

import utils
from pedestrian import detect_person

import del_serv
import GLOBAL_VAR
global order
order=bytes("6"+"-"+"0",encoding='utf8')

min_size_components = 500
similarity_contour_with_circle = 0.8

class vid_receiver:
    def __init__(self,ip:str):
        self.ip = ip
        self.port=9999
        self.BUFF_SIZE=75000
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,self.BUFF_SIZE)
        self.host_name=socket.gethostname()
        print(ip)
        self.message=b'Hello'

    def run(self):
        self.client_socket.sendto(self.message,(self.ip,self.port))
        fps,st,frames_to_count,cnt = (0,0,20,0)
        global order
        while True:
            try:
                packet,_ = self.client_socket.recvfrom(self.BUFF_SIZE)
                data = base64.b64decode(packet,' /')
                npdata = np.fromstring(data,dtype=np.uint8)
                frame = cv2.imdecode(npdata,1)
                #frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            except:
                continue
            
            """
            pre_fra = utils.preprocess_image(frame)
            bin_fra = utils.removeSmallComponents(pre_fra, min_size_components)
            contours = utils.findContour(bin_fra)
            sav_img, coordinate = utils.findLargestSign(frame, contours, similarity_contour_with_circle, 15)
    
            box_fra = frame.copy()
            if coordinate:
                cv2.rectangle(box_fra, coordinate[0], coordinate[1], (0, 255, 0), 2)
                #print(coordinate)
                
                sign=utils.predict(sav_img)
                print(sign)
                order=bytearray(str(sign),encoding='utf8')
                
            frame,person_exist=detect_person(frame)
            print(person_exist)
            """
            
            
            if frame is None:
                pass
            else:
                try:
                    sign, GLOBAL_VAR.sign_type, coordinate = utils.get_localization_label(frame)
                    frame, GLOBAL_VAR.person_exist = detect_person(frame)
                    order=bytes(GLOBAL_VAR.sign_type+"-"+GLOBAL_VAR.person_exist,encoding='utf8')
                    box_fra = frame.copy()
                    if coordinate:
                        cv2.rectangle(box_fra, coordinate[0], coordinate[1], (0, 255, 0), 2)
                          
                   
                    #cv2.imshow('Remote', box_fra)
                    print("Label:", GLOBAL_VAR.sign_type)
                    print("person?:", GLOBAL_VAR.person_exist)
                    #if cv2.waitKey(1) & 0xFF == 27:  # ESC for end
                       # break
                except:
                    print("err")
                    continue
                
            

            try:
                del_serv.order_send(order) 
            except:
                continue
            
            cv2.imshow("RECEIVING VIDEO",box_fra)
            #time.sleep(0.1)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.client_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1
            
      
class order_sender:
    def __init__(self,ip):
        self.ip = ip
        self.port=10000
        self.BUFF_SIZE=1024
        self.sender_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sender_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,1024)
        self.socket_address = (self.ip,self.port)
        self.sender_socket.bind(self.socket_address)
        self.host_name=socket.gethostname()
        print(ip)
        self.m="kkk"
        
        
    def run(self):
        
        global order
        while True:
            data,addr=self.sender_socket.recvfrom(64)
            self.sender_socket.sendto(b'hello client',addr)
            #self.sender_socket.sendto(self.m.encoding('utf-8'),(self.ip,self.port))
            time.sleep(0.1)
        

r=vid_receiver('169.254.55.222')
th1=threading.Thread(target=r.run)
th1.start()
