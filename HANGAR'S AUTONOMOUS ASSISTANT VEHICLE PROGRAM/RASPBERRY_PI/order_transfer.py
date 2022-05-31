from socket import * 
import time
import motor_control
import threading

print("--------")
serverName = '169.254.9.118'   #Change this for your PC IP
serverPort = 12000 

clientSocket = socket(AF_INET, SOCK_DGRAM)


def order_recv():
    try:
        message = "cnn"
        clientSocket.sendto(message.encode(), (serverName, serverPort)) 
      
        modifiedMessage, serverAddress = clientSocket.recvfrom(64000)
        ###
        #print("\nMessage Sent to Server :" +str(serverAddress))
        #print("Receiving Message From the Server...")
        
        orders=modifiedMessage.decode()
        sign=orders.split('-')[0]
        pedestrian_exist=orders.split('-')[1]
        ####
        print("Sign:",sign + "\t Pedestrian:", pedestrian_exist)
        
        #message = input("\nInput lowercase sentence:")
        #clientSocket.close()
        
        thread1=threading.Thread(target=motor_control.operate_order(sign[0]))
        thread1.start()
        thread2=threading.Thread(target=motor_control.operate_buzz(pedestrian_exist[0]))
        thread2.start()
        
        #print('Distance3')
        #print(current_distance)
        #print("Distance4")
        #print(T1_start)
        
        
            
        
        #print('Distance:' +str(current_distance)+' cm')
        
        #thread3=threading.Thread(target=motor_control.object_detect(5))
        #thread3.start()
    except:
        ###
        #print("ord rec err")
        pass
