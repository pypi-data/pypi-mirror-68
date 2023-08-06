from setuptools import setup

setup(
    name="pencilcase",
    author="Chelsea Voss",
    author_email="csvoss@csvoss.com",
    description=("A little box of Python tools."),
    version="0.0.1",
    scripts=["pencilcase.py"],
    install_requires=["prompt_toolkit"],
)
