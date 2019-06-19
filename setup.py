from setuptools import setup

setup(
    name='evovrp',
    version='1.0',
    description='Solving MDVRP using evolutionary algorithms.',
    author='Matic Pintarič, Sašo Karakatič',
    author_email='matic.pintaric@outlook.com',
    url='https://github.com/mpinta/evovrp',
    license='MIT',
    packages=['evovrp'],
    install_requires=[
        'numpy',
        'imageio',
        'matplotlib',
        'NiaPy==2.0.0rc4'
    ]
)
