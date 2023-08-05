
import setuptools

with open("README.md") as rdm:
    longDiscr = rdm.read()
    
setuptools.setup(
    name="dkh_pixel",
    version="1.0.1",
    author="Дмитрий Холостов",
    author_email="dkh@ro.ru",
    description="Библиотека для создания пиксельной графики в Python. Использует Tkinter.",
    long_description=longDiscr,
    long_description_content_type="text/markdown",
    url="https://github.com/dkh-gh/pixel_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
