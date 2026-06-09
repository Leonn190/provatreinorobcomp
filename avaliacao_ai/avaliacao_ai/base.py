import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


# Classe principal do node
class MeuNode(Node):

    def __init__(self):
        # Nome do node no ROS
        super().__init__('meu_node')

        # Publisher:
        # cria um publicador que envia mensagens do tipo Twist no tópico /cmd_vel
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Timer:
        # chama a função control() a cada 0.1 segundos
        self.timer = self.create_timer(0.1, self.control)

    def control(self):
        # Cria uma mensagem de velocidade
        vel = Twist()

        # Velocidade linear para frente
        vel.linear.x = 0.2

        # Velocidade angular
        # 0.0 significa não girar
        vel.angular.z = 0.0

        # Publica a velocidade no robô
        self.cmd_vel_pub.publish(vel)


def main(args=None):
    # Inicializa o ROS
    rclpy.init(args=args)

    # Cria o node
    node = MeuNode()

    # Mantém o node rodando
    rclpy.spin(node)

    # Finaliza o node
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()