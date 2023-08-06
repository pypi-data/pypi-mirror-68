from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    reqs = f.read()

pkgs = [p for p in find_packages() if p.startswith('fastrouge')]
print(pkgs)

setup(
    name='fastrouge',
    version='0.0.1',
    url='https://github.com/fastnlp/fastSum',
    description='A rouge tool written in Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='Apache License',
    author='FudanNLP',
    python_requires='>=3.6',
    packages=pkgs,
    install_requires=reqs.strip().split('\n'),
)