from setuptools import setup

setup(
    name='tracker-master',
    version='1.0.25',
    packages=['tracker_master', 'tracker_master.model', 'tracker_master.app_master', 'tracker_master.app_server'],
    url='',
    license='',
    author='Mikhail Astafurov',
    author_email='',
    package_data={
        '': ['logging.json'],
        'tracker_master': ['conf/*.yaml']
    },
    description='',
    install_requires=['pyserial', 'pyzabbix', 'PyYAML']
)
