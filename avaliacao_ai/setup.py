from setuptools import find_packages, setup

package_name = 'avaliacao_ai'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='borg',
    maintainer_email='euleonsoto@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'base = exemplos.base:main',
        'girador = exemplos.girador:main',
        'estados = exemplos.estados:main',
        'odom = exemplos.odom:main',
        'pardes = exemplos.pardes:main',
        'detector = exemplos.detector:main',
        'detectacores = exemplos.detectacores:main',
        'seguelinha = exemplos.seguelinha:main',
        'comandos = exemplos.comandos:main',
        'q1 = avaliacao_ai.q1:main',
        'q2 = avaliacao_ai.q2:main',
    ],
},
)
