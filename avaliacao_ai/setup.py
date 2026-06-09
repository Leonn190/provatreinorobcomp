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
        'base = avaliacao_ai.base:main',
        'girador = avaliacao_ai.girador:main',
        'estados = avaliacao_ai.estados:main',
        'odom = avaliacao_ai.odom:main',
        'pardes = avaliacao_ai.pardes:main',
        'detector = avaliacao_ai.detector:main',
        'detectacores = avaliacao_ai.detectacores:main',
        'seguelinha = avaliacao_ai.seguelinha:main',
        'q1 = avaliacao_ai.q1:main',
        'q2 = avaliacao_ai.q2:main',
    ],
},
)
