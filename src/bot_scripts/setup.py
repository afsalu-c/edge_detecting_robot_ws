from setuptools import find_packages, setup

package_name = 'bot_scripts'

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
    maintainer='afsalu-rahman-c',
    maintainer_email='afsalu2002@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "edge_detection = bot_scripts.edge_detection:main",
            "cli = bot_scripts.cli:main"
        ],
    },
)
