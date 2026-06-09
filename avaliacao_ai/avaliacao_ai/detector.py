import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan

import math


class DetectorParedes(Node):

    def __init__(self):
        super().__init__('detector_paredes')

        # Subscriber do laser
        # Recebe mensagens do tópico /scan
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Distância mínima para considerar que "tem parede"
        self.limite = 0.7

    def scan_callback(self, msg):
        ranges = msg.ranges

        # Em muitos robôs:
        # frente  ≈ índice 0
        # esquerda ≈ índice 90
        # atrás ≈ índice 180
        # direita ≈ índice 270
        #
        # Em vez de usar um índice só, usamos pequenas faixas.

        frente = self.menor_distancia(
            list(ranges[0:10]) + list(ranges[-10:])
        )

        esquerda = self.menor_distancia(
            list(ranges[80:100])
        )

        atras = self.menor_distancia(
            list(ranges[170:190])
        )

        direita = self.menor_distancia(
            list(ranges[260:280])
        )

        # Detecta se tem parede ou obstáculo perto
        tem_frente = frente < self.limite
        tem_esquerda = esquerda < self.limite
        tem_direita = direita < self.limite
        tem_atras = atras < self.limite

        # Print no terminal
        print("========== LASER ==========")
        print(f"Frente:   {frente:.2f} m | Tem parede? {tem_frente}")
        print(f"Esquerda: {esquerda:.2f} m | Tem parede? {tem_esquerda}")
        print(f"Direita:  {direita:.2f} m | Tem parede? {tem_direita}")
        print(f"Atrás:    {atras:.2f} m | Tem parede? {tem_atras}")

    def menor_distancia(self, lista):
        """
        Recebe uma lista de leituras do laser
        e retorna a menor distância válida.
        """

        valores_validos = []

        for valor in lista:
            # Remove infinito, nan e valores inválidos
            if math.isfinite(valor) and valor > 0.0:
                valores_validos.append(valor)

        # Se não tiver nenhum valor válido, assume que está longe
        if len(valores_validos) == 0:
            return 999.0

        return min(valores_validos)


def main(args=None):
    rclpy.init(args=args)

    node = DetectorParedes()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()