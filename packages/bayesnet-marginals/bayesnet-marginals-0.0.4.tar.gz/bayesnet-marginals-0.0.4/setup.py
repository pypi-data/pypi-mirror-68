from setuptools import setup

setup(
    name='bayesnet-marginals',
    version='0.0.4',
    packages=['bayesnet'],
    url='https://gitlab.inria.fr/cobcom/cimem/bayesnet',
    license='',
    author='Samuel Deslauriers-Gauthier',
    author_email='sam.deslauriers@gmail.com',
    description='A Python package to repeatedly obtain the marginal '
                'distributions of a Bayesian network using exact inference.',
    install_requires=[
        'numpy',
        'recursive-abc',
    ],
    extras_require={
        'gpu-acceleration': ['pyopencl'],
        'scripts': ['matplotlib']
    },
    data_files=[
        ('config', ['config/bayesnet.json']),
    ],
)
