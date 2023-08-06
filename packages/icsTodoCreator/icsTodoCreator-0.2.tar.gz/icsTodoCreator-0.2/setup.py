from setuptools import setup, find_packages

setup(
    name='icsTodoCreator',
    version='0.2',
    description='A tool to create multiple vcalendar tasks at once to speed up decentralized specialized manufacturing.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ics tasks todo scale MakerVsVirus',
    author='Fabian Becker',
    author_email='fab.becker@outlook.de',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
)
