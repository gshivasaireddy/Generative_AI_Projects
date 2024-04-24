from setuptools import find_packages,setup

setup(
  name='mcq_generator',
  version='0.0.1',
  author ='author name',
  author_email='author email'
  install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
  packages=find_packages()  # responsible to find the local packages where it has __init__.py file, it identifies that folder as package
)