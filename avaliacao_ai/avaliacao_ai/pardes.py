import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

import math


class MeuNode(Node):

    def __init__(self):
        super().__init__('meu_node_odom_laser')

        # Publisher para mandar velocidade para o robô
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Subscriber da odometria: posição do robô
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Subscriber do laser: distância até paredes/obstáculos
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Estado inicial
        self.estado = "ANDANDO"

        # Posição atual
        self.x = 0.0
        self.y = 0.0

        # Distâncias do laser
        self.frente = 999.0
        self.esquerda = 999.0
        self.direita = 999.0

        # Timer chama control() a cada 0.1 segundos
        self.timer = self.create_timer(0.1, self.control)

    # =========================
    # CALLBACK DA ODOMETRIA
    # =========================

    def odom_callback(self, msg):
        # Posição atual do robô
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

    # =========================
    # CALLBACK DO LASER
    # =========================

    def scan_callback(self, msg):
        # O laser vem como uma lista de distâncias
        ranges = msg.ranges

        # Normalmente:
        # índice 0 = frente
        # índice 90 = esquerda
        # índice 270 = direita
        #
        # Para ficar mais seguro, usamos uma faixa de valores
        # em vez de um único ponto.

        frente_lista = list(ranges[0:10]) + list(ranges[-10:])
        esquerda_lista = list(ranges[80:100])
        direita_lista = list(ranges[260:280])

        # Remove leituras inválidas: inf, nan ou valores muito pequenos
        frente_lista = self.filtra_laser(frente_lista)
        esquerda_lista = self.filtra_laser(esquerda_lista)
        direita_lista = self.filtra_laser(direita_lista)

        # Pega a menor distância em cada direção
        self.frente = min(frente_lista)
        self.esquerda = min(esquerda_lista)
        self.direita = min(direita_lista)

    def filtra_laser(self, lista):
        nova_lista = []

        for valor in lista:
            if math.isfinite(valor) and valor > 0.0:
                nova_lista.append(valor)

        # Se não sobrou nenhum valor bom, assume longe
        if len(nova_lista) == 0:
            nova_lista.append(999.0)

        return nova_lista

    # =========================
    # CONTROLE PRINCIPAL
    # =========================

    def control(self):
        vel = Twist()

        # Mostra no terminal para debug
        self.get_logger().info(
            f"estado={self.estado} | x={self.x:.2f}, y={self.y:.2f} | "
            f"frente={self.frente:.2f}, esq={self.esquerda:.2f}, dir={self.direita:.2f}"
        )

        # =========================
        # LÓGICA DE DETECÇÃO DE PAREDE
        # =========================

        if self.frente < 0.5:
            # Parede muito perto na frente
            self.estado = "GIRANDO"

        else:
            # Caminho livre
            self.estado = "ANDANDO"

        # =========================
        # SELETOR DE ESTADOS
        # =========================

        if self.estado == "PARADO":
            vel.linear.x = 0.0
            vel.angular.z = 0.0

        elif self.estado == "ANDANDO":
            vel.linear.x = 0.2
            vel.angular.z = 0.0

        elif self.estado == "GIRANDO":
            vel.linear.x = 0.0
            vel.angular.z = 0.3

        elif self.estado == "CURVA_DIREITA":
            vel.linear.x = 0.2
            vel.angular.z = -0.3

        elif self.estado == "CURVA_ESQUERDA":
            vel.linear.x = 0.2
            vel.angular.z = 0.3

        self.cmd_vel_pub.publish(vel)


def main(args=None):
    rclpy.init(args=args)

    node = MeuNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()