from setuptools import setup, find_packages

setup(
    name='McqGenerator',
    version='0.0.1',
    author='Harsh',
    author_email='pharshin29@gmail.com',
    packages=find_packages(),
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_community","langchain_openai"]
)