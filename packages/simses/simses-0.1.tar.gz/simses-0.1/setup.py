from setuptools import setup

setup(
    name='simses',
    version='0.1',
    description='Simulation for Stationary Storage Systems (SimSES)',
    url='https://gitlab.lrz.de/open-ees-ses/simses',
    author='Daniel Kucevic, Marc Möller',
    author_email='simses.ees@ei.tum.de',
    license='BSD 3-Clause "New" or "Revised" License',
    install_requires=['scipy',
                      'numpy',
                      'pandas',
                      'plotly',
                      'matplotlib',
                      'pytest',
                      'pytz'
                      ],


    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
)