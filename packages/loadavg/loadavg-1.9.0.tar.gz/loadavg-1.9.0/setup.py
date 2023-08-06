from setuptools import setup, find_packages


long_description = 'Simple package for check and monitoring server'

setup(
    name='loadavg',
    version='1.9.0',
    description='loadaverage.net',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'loadavg = src.main:loadavg'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='python',
    install_requires=["psutil", "flask"],
    zip_safe=False
)
