from setuptools import find_packages, setup

package_name = 'lidar_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lidar_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mscrobotics2425laptop37',
    maintainer_email='judebarakat@yahoo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lidar_publisher = lidar_pkg.lidar_publisher:main',
            'lidar_subscriber = lidar_pkg.lidar_subscriber:main',
        ],
    },
)
