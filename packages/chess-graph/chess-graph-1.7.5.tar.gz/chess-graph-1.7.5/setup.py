from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="chess-graph",
    version="1.7.5",
    license ="'MIT'",
    author="Simon Ilincev",
    author_email="trilogicworlds@gmail.com",
    description="A package that can create an interactive multi-level, shaded, piechart visualization of chess games.",
    packages = find_packages(),
    package_data={'chess_graph': ['elo_reading/*']},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Destaq/chess_graph",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
