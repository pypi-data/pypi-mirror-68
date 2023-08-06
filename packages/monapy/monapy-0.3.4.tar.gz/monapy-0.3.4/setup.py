import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='monapy',
    version='0.3.4',
    author='Andriy Stremeluk',
    author_email='astremeluk@gmail.com',
    description='Declarative programming tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(exclude=['test*', 'devif*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.0'
)
