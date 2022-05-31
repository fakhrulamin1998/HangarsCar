from socket import * 
import time

serverName = gethostname() 
serverPort = 12000 
serverSocket = socket(AF_INET, SOCK_DGRAM) 
serverSocket.bind((serverName, serverPort)) 
print ("\nThe server is ready to receive\n")  
    
def order_send(o):
    try:
        message, clientAddress = serverSocket.recvfrom(64000) 
        print("Message From Client:" +str(clientAddress)) 
        #print("Processing...") 
        serverSocket.sendto(o, clientAddress) 
        print("Sending a Message to the Client:" +str(clientAddress))
        
    except:
        print("ord err")
        pass
     