from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'gui_controller_leo'


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),

    data_files=[

        ('share/ament_index/resource_index/packages', ['resource/gui_controller_leo']),
        ('share/gui_controller_leo', ['package.xml']),
        ('share/gui_controller_leo/launch', ['launch/gui_controller_launch.py']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
            
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
        # Include rviz (.rviz) files
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
        # Include world (.sdf, .dae, and .stl) files
        (os.path.join('share', package_name, 'worlds'), 
        glob(os.path.join('worlds', '**', '*.sdf'), recursive=True) +
        glob(os.path.join('worlds', '**', '*.dae'), recursive=True) +
        glob(os.path.join('worlds', '**', '*.stl'), recursive=True)),
        # Include config (.yaml) files
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.*yaml*'))),
	    # Include map (.yaml and .pgm) files
        (os.path.join('share', package_name, 'maps'), glob(os.path.join('maps', '*.[yp][ag][m]*'))),


    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mscrobotics2425laptop35',
    maintainer_email='islam.elbagiraminsalih@student.manchester.ac.uk',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gui_controller = gui_controller_leo.gui_controller:main',
        ],
    },
)
