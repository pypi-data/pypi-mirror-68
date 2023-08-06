"""Python drivers for various chips used with Raspberry Pis."""
from setuptools import setup


with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name='numat-chips',
    version='0.1.1',
    description="Drivers for ADCs, sensors, and other electronic chips.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/numat/chips/',
    author='Patrick Fuller',
    author_email='pat@numat-tech.com',
    packages=['chips'],
    entry_points={
        'console_scripts': [('chips = chips:command_line')]
    },
    install_requires=['smbus', 'spidev'],
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
    ]
)
