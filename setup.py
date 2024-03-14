from setuptools import find_packages,setup

setup (
    name="mcqgenrator",
    version="0.0.1",
    author="aditya varpe",
    author_email="adi.varpe117@gmail.com",
    install_requires = ["openai","langchain","pyPDF2","python-dotenv"],
    packages=find_packages()
)
