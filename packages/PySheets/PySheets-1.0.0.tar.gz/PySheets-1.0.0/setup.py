from setuptools import *

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='PySheets',
    version='1.0.0',
    packages=find_packages(include=['pysheets']),
    url='https://github.com/GrandMoff100/SheetsHandler',
    license='MIT License',
    author='Quantum_Wizard',
    author_email='minecraftcrusher100@gmail.com',
    description='A module full of many tools and extensions incorporated into the SheetsPy01 spreadsheet module.',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
