from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='evovrp',
    version='1.0',
    description='Solving vehicle routing problem using evolutionary algorithms.',
    author='Matic Pintarič',
    author_email='matic.pintaric@outlook.com',
    url='https://github.com/karakatic/evovrp',
    license='MIT',
    packages=['evovrp'],
    install_requires=[
        'numpy',
        'imageio',
        'matplotlib',
        'NiaPy==2.0.0rc4'
    ]
)
