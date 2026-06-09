import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class MeuNode(Node):

    def __init__(self):
        super().__init__('meu_node_girando')

        # Publisher que envia velocidade para o robô
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Chama control() a cada 0.1 segundos
        self.timer = self.create_timer(0.1, self.control)

    def control(self):
        # Cria a mensagem de velocidade
        vel = Twist()

        # Não anda para frente
        vel.linear.x = 0.0

        # Gira parado
        # positivo = gira para um lado
        # negativo = gira para o outro
        vel.angular.z = 0.3

        # Envia o comando para o robô
        self.cmd_vel_pub.publish(vel)


def main(args=None):
    rclpy.init(args=args)

    node = MeuNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()