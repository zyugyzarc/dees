import setuptools

setuptools.setup(
    name='deez',
    version='1.0',
    scripts=['./deez/deez'],
    author='Me',
    description='This runs my script which is great.',
    packages=['deez.deez']
    install_requires=[
        'setuptools',
        'regex >= 2021.8.3',
    ],
    python_requires='>=3.6'
)
