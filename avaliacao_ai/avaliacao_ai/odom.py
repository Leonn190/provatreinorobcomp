import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class MeuNode(Node):

    def __init__(self):
        super().__init__('meu_node_com_odom')

        # Publisher para mandar velocidade para o robô
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Subscriber para receber a posição do robô
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Estado atual
        # Teste trocando entre:
        # "PARADO", "ANDANDO", "GIRANDO", "CURVA_DIREITA", "CURVA_ESQUERDA"
        self.estado = "ANDANDO"

        # Posição atual do robô
        self.x = 0.0
        self.y = 0.0

        # Guarda a posição inicial
        self.x_inicial = None
        self.y_inicial = None

        # Timer chama control() a cada 0.1 segundos
        self.timer = self.create_timer(0.1, self.control)

    def odom_callback(self, msg):
        # Pega a posição atual vinda da odometria
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # Guarda a posição inicial apenas uma vez
        if self.x_inicial is None:
            self.x_inicial = self.x
            self.y_inicial = self.y

    def control(self):
        vel = Twist()

        # Só para visualizar no terminal
        self.get_logger().info(f"Posição atual: x={self.x:.2f}, y={self.y:.2f}")

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

        # Publica o movimento escolhido
        self.cmd_vel_pub.publish(vel)


def main(args=None):
    rclpy.init(args=args)

    node = MeuNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()