import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class SegueLinha(Node):

    def __init__(self):
        super().__init__('segue_linha')

        # Publisher para mandar velocidade ao robô
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Subscriber da câmera
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Conversor de imagem ROS -> OpenCV
        self.bridge = CvBridge()

        # Guarda erro da linha
        self.erro = 0

        # Diz se achou ou não a linha
        self.achou_linha = False

        # Timer de controle
        self.timer = self.create_timer(0.1, self.control)

    def image_callback(self, msg):
        # Converte imagem ROS para OpenCV
        img_bgr = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # Pega altura e largura da imagem
        altura, largura, _ = img_bgr.shape

        # Usa só a parte de baixo da imagem
        # porque é onde a linha do chão aparece mais próxima do robô
        recorte = img_bgr[int(altura * 0.6):altura, 0:largura]

        # Converte para HSV
        img_hsv = cv2.cvtColor(recorte, cv2.COLOR_BGR2HSV)

        # Máscara para detectar preto
        # ajuste se a linha for outra cor
        preto_baixo = np.array([0, 0, 0])
        preto_alto = np.array([180, 255, 80])

        mask = cv2.inRange(img_hsv, preto_baixo, preto_alto)

        # Calcula momentos da máscara
        M = cv2.moments(mask)

        if M["m00"] > 0:
            # Centro da linha no eixo x
            cx = int(M["m10"] / M["m00"])

            # Centro da imagem
            centro_imagem = largura // 2

            # Erro:
            # negativo = linha à esquerda
            # positivo = linha à direita
            self.erro = cx - centro_imagem
            self.achou_linha = True

        else:
            # Não achou linha
            self.achou_linha = False

    def control(self):
        vel = Twist()

        if self.achou_linha:
            # Anda para frente
            vel.linear.x = 0.2

            # Corrige direção com base no erro
            # Se erro positivo, gira para direita
            # Se erro negativo, gira para esquerda
            vel.angular.z = -float(self.erro) / 300.0

        else:
            # Se perdeu a linha, gira devagar procurando
            vel.linear.x = 0.0
            vel.angular.z = 0.2

        self.cmd_vel_pub.publish(vel)


def main(args=None):
    rclpy.init(args=args)

    node = SegueLinha()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()