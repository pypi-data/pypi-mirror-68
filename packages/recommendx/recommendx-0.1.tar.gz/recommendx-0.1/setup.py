from distutils.core import setup

setup(
    name='recommendx', 
    packages = ['recommendx'],
    version='0.1',
    license = 'bsd-3-clause',
    description = 'Recommendation system with observed attributes and time-varying coefficients',
    author = 'Adam Rennhoff',
    author_email = 'Adam.Rennhoff@mtsu.edu',
    url = 'https://github.com/adrennhoff/recommendx',
    keywords = ['machine learning','recommendation system','SVD'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
)