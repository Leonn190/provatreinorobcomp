import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class MeuNode(Node):

    def __init__(self):
        super().__init__('meu_node_estados_basico')

        # Publisher para controlar o robô
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Estado atual do robô
        # Troque aqui para testar:
        # "PARADO", "ANDANDO", "GIRANDO", "CURVA"
        self.estado = "PARADO"

        # Timer chama control() várias vezes por segundo
        self.timer = self.create_timer(0.1, self.control)

    def control(self):
        vel = Twist()

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

        elif self.estado == "CURVA":
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