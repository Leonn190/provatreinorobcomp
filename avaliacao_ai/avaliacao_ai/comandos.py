# # 1) Ir para a pasta onde ficam os pacotes/projetos ROS 2
# cd ~/colcon_ws/src

# # 2) Baixar o repositório da prova
# git clone LINK_DO_REPOSITORIO_DA_PROVA

# # 3) Entrar na pasta do repositório baixado
# cd NOME_DO_REPOSITORIO

# # 4) Abrir o projeto no VS Code
# code .

# # 5) Criar um pacote ROS 2 em Python, se a prova pedir para criar pacote
# # Troque avaliacao_sub pelo nome exigido no enunciado
# ros2 pkg create --build-type ament_python avaliacao_sub --dependencies rclpy std_msgs geometry_msgs sensor_msgs nav_msgs cv_bridge robcomp_interfaces robcomp_util

# # 6) Voltar para a raiz do workspace antes de compilar
# cd ~/colcon_ws

# # 7) Compilar o pacote da prova
# # Troque avaliacao_sub pelo nome real do pacote
# colcon build --packages-select avaliacao_sub --symlink-install

# # 8) Atualizar o terminal para ele reconhecer o pacote compilado
# source install/setup.bash

# # 9) Rodar a questão 1
# # Funciona se o setup.py tiver algo como: 'q1 = avaliacao_sub.q1:main'
# ros2 run avaliacao_sub q1

# # 10) Rodar a questão 2
# # Funciona se o setup.py tiver algo como: 'q2 = avaliacao_sub.q2:main'
# ros2 run avaliacao_sub q2

# # 11) Listar os tópicos ROS ativos
# # Serve para descobrir nomes como /cmd_vel, /scan, /odom, /camera/image_raw, /controle
# ros2 topic list

# # 12) Ver o tipo de mensagem de um tópico
# # Exemplo: mostra se /cmd_vel usa Twist, se /scan usa LaserScan etc.
# ros2 topic info /cmd_vel
# ros2 topic info /scan
# ros2 topic info /odom

# # 13) Ver os dados chegando em um tópico
# # Use para conferir se o robô está recebendo laser, odometria ou comandos
# ros2 topic echo /scan
# ros2 topic echo /odom
# ros2 topic echo /cmd_vel

# # 14) Procurar arquivos de launch do simulador
# # Use se você não souber o nome exato do comando para abrir o mundo
# cd ~/colcon_ws/src
# find . -name "*.launch.py"

# # 15) Rodar o simulador
# # O nome exato depende da prova; copie do enunciado ou do arquivo encontrado
# ros2 launch NOME_DO_PACOTE NOME_DO_ARQUIVO.launch.py

# # 16) Ver o estado do Git antes de entregar
# git status

# # 17) Adicionar todos os arquivos modificados
# git add .

# # 18) Criar o commit da entrega
# git commit -m "Entrega avaliacao"

# # 19) Enviar para o GitHub
# git push

# # 20) Conferir se o commit existe
# git log --oneline

# # 21) Se o push der erro de branch, tente este comando
# git push -u origin HEAD

# # 22) Se o terminal travar rodando nó ou simulador, pare com:
# CTRL + C