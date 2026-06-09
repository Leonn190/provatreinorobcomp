import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class DetectorCores(Node):

    def __init__(self):
        super().__init__('detector_cores')

        # Subscriber da câmera
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Converte imagem ROS para OpenCV
        self.bridge = CvBridge()

        # Quantidade mínima de pixels para considerar que viu a cor
        self.min_pixels = 500

    def image_callback(self, msg):
        # Converte a imagem do ROS para formato OpenCV
        img_bgr = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # Converte BGR para HSV
        # HSV é melhor para detectar cor
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        # Dicionário com limites das cores em HSV
        cores = {
            "vermelho_1": ((0, 80, 80), (10, 255, 255)),
            "vermelho_2": ((170, 80, 80), (180, 255, 255)),

            "azul": ((100, 80, 80), (130, 255, 255)),
            "verde": ((40, 80, 80), (80, 255, 255)),
            "amarelo": ((20, 80, 80), (35, 255, 255)),
            "laranja": ((10, 80, 80), (20, 255, 255)),
            "roxo": ((130, 80, 80), (160, 255, 255)),

            "preto": ((0, 0, 0), (180, 255, 50)),
            "branco": ((0, 0, 200), (180, 40, 255)),
        }

        cores_detectadas = []

        for nome, (baixo, alto) in cores.items():
            baixo = np.array(baixo)
            alto = np.array(alto)

            # Cria máscara da cor
            mask = cv2.inRange(img_hsv, baixo, alto)

            # Conta quantos pixels dessa cor existem
            pixels = cv2.countNonZero(mask)

            if pixels > self.min_pixels:
                cores_detectadas.append(nome)

        # Junta os dois vermelhos em um nome só
        if "vermelho_1" in cores_detectadas or "vermelho_2" in cores_detectadas:
            cores_detectadas = [
                cor for cor in cores_detectadas
                if cor not in ["vermelho_1", "vermelho_2"]
            ]
            cores_detectadas.append("vermelho")

        print("========== CÂMERA ==========")

        if len(cores_detectadas) == 0:
            print("Nenhuma cor relevante detectada")
        else:
            print("Cores detectadas:", cores_detectadas)


def main(args=None):
    rclpy.init(args=args)

    node = DetectorCores()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()