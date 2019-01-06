#!/usr/bin/env python
# coding=utf-8
import csv
import re
import os
import urllib.request
from datetime import datetime
import time
import rospy
from geometry_msgs.msg import Twist

log = open('Data/driver_log.csv', 'w')
#url = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/m1UI4XnQF7NZHBXdfRBDhVQheIz.jpg"
url = "http://192.168.0.65/jpg/image.jpg" #LINK DA IMAGEM

linearX = 0.0
angularZ = 0.0

def salvarArquivos(x, z):
    log = open('Data/driver_log.csv', 'a')
    escrever = csv.writer(log)
    j = 0 
    i = 0
    while os.path.exists("Data/IMG/imagem%s.jpg" % i): #VERIFICA A ULTIMA IMAGEM SALVA
        i += 1
    try:
        urllib.request.urlretrieve(url, "Data/IMG/imagem%s.jpg" % i) #SALVA A IMAGEM BAIXADA
        nomeimagem = "IMG/imagem%s.jpg" % i #os.getcwd()+"/Data/ EDIÇÕES
        print("imagem %s baixada com sucesso!" % i)
    except:
        print('ocorreu um erro no download da imagem %s' % i) #MENSAGEM CASO ENCONTRE UM ERRO
    try:
        escrever.writerow((nomeimagem, x, z)) #SALVA A IMAGEM NO ARQUIVO DE LOG, JUNTAMENTE COM O VALOR DE X e Y
        print("imagem %s salva no arquivo de Log com sucesso!" % i)
	#print("imagem: %s, X: %s, Y: %s" %nomeimagem, %x, %z)
    except:
        print('ocorreu um erro para salvar a imagem %s' % i)
    i += 1
    j += 1 
    print(os.getcwd())
    log.close()
    listener()

#não está precisando por enquanto
def callback(data): # COLOCA O VALOR ENVIADO DO NO NAS VARIÁVIES X e Y
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    linear_x = data.linear.x
    print('X: ', linear_x)
    angular_z = data.angular.z
    print('z: ', angular_z)
    salvarArquivos(linear_x,angular_z)
    
    
def listener(): #ESCULTA O NÓ DE COMUNICAÇÃO DE CONTROLE COM O ROS

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('NodeDeTeste', anonymous=True)
    #procura  um node com o nome definido atrás da mensagem Twist declada
    #para executar a função callback
    #valores = rospy.Subscriber("drrobot_cmd_vel", Twist, callback)
    data = rospy.wait_for_message("drrobot_cmd_vel", Twist)
    #callback(data)
    linear_x = data.linear.x
    print('X: ', linear_x)
    angular_z = data.angular.z
    print('z: ', angular_z)
    
    salvarArquivos(linear_x,angular_z)
    print("ele chegou até aqui 3")
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    



print("Iniciando...")
listener()
	

