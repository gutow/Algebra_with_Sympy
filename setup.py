import setuptools

with open("ReadMe.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="Algebra_with_SymPy",
    url = "https://github.com/gutow/Algebra_with_Sympy",
    version="0.9.0.rc1",
    description="Equations that can be algebraicly manipulated.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jonathan Gutow",
    author_email="gutow@uwosh.edu",
    license="GPL-3.0+",
    packages=setuptools.find_packages(),
    install_requires=[
        # 'python>=3.6',
        #RPi.GPIO is required by pi-plates, not sure why not included in the
        # pi-plates setup.py.
        'jupyter>=1.0.0',
        'sympy>=1.6'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
