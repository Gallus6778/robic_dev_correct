#!/usr/bin/env python
# coding: utf-8

# In[1]:

import socket, threading
from chatbot_module import Pas_internet as pi
# In[ ]:


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        
    def run(self):
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode("utf8")
            if msg=='bye':
                self.csocket.send(message_emis)
                break
            # ===========================================================
            print ("from client", msg)
            reponse = list(msg.split(","))

            message_ack = ''
            if reponse[1] == 'pi':
                pas_internet = pi(reponse[0])
                print(reponse)
                print(reponse[0])
                print(type(reponse[0]))
                transcription = pas_internet.main()

                # for keys, values in transcription.items():
                #     message_ack = message_ack + keys + ":" + values +";"
            elif reponse[1] == 'li':
                message_ack = 'lenteur internet a resoudre tres bientot'
                # pas_internet = pi(reponse[0])
                # transcription = pas_internet.main()
                #
                # for keys, values in transcription:
                #     message_ack = message_ack + keys + ":" +values +";"
            elif reponse[1] == 'ae':
                message_ack = 'appel entrant a resoudre tres bientot'
            elif reponse[1] == 'as':
                message_ack = 'appel sortant a resoudre tres bientot'
            elif reponse[1] == 'sms':
                message_ack = 'pb sms a resoudre tres bientot'
            else:
                message_ack = 'probleme non specifie'
            # ===========================================================

            # message_emis = message_ack.encode("utf8")
            message_emis = transcription.encode("utf8")

            self.csocket.send(message_emis)
        print ("Client at ", clientAddress , " disconnected...")

# ==================changer l'adresse ip de la machine dans le reseau=========================================
LOCALHOST = "192.168.1.3"
PORT = 12101
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(10)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()

