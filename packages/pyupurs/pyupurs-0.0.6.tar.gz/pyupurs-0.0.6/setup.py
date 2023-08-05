import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='pyupurs',
    version='0.0.6',
    author='Imad Youbi Idrissi',
    author_email='imad.youbi.idrissi@gmail.com',
    description="PYthon Utilitary Processing, Useful and Reliable Stuff",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ImadYIdrissi/pyupurs",
    packages=setuptools.find_packages(),
    license='LICENSE.txt',
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ),
    install_requires=requirements,
    python_requires='>=3.6'
    # scripts=['some_script.py', 'bin/some_other_script.py'],
)
