#!/usr/bin/env python
import csv
import re
import os
import urllib.request
from datetime import datetime
from time import sleep
import rospy
#from geometry_msgs import Twist

#url = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/m1UI4XnQF7NZHBXdfRBDhVQheIz.jpg"
url = "http://192.168.0.65/jpg/image.jpg"
def salvarArquivos(x, z):
    log = open('Data/driver_log.csv', 'w')
    escrever = csv.writer(log)
    j = 0
    i = 0
    b = 1
    while os.path.exists("imagem%s.jpg" % i):
        i += 1
    while b == 1:
        try:
            urllib.request.urlretrieve(url, "Data/IMG/imagem%s.jpg" % i)
            nomeimagem = os.getcwd()+"/Data/IMG/imagem%s.jpg" % i
            print("imagem %s baixada com sucesso!" % i)
        except:
            print('ocorreu um erro no download da imagem %s' % i)
        #delay em segundos
        sleep(0.1)
        try:
            escrever.writerow((nomeimagem, x,z))
            print("imagem %s salva no arquivo de Log com sucesso!" % i)
        except:
            print('ocorreu um erro para salvar a imagem %s' % i)
        i += 1
        j += 1
        if j >= 3:
            b = 0
        
    print(os.getcwd())
    log.close()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    x = data.linear.x
    print('X: ', x)
    z = data.linear.z
    print('z: ', z)
    salvarArquivos(x,z)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('NodeDeTeste', anonymous=True)

    #procura  um node com o nome definido atrás da mensagem Twist declada
    #para executar a função callback
    rospy.Subscriber("drrobot_cmd_vel", Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
