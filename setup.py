from setuptools import find_packages, setup

HYPEN_E_DOT = '-e .'

def get_requirements(file_path) :
    requirements = [] 
    with open(file_path) as f:
        requirements = [lines.replace("\n","" ) for lines in f.readlines()]
    
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
name = 'kubeflow_project',
version = '0.0.1',
author = 'praneeth_bhandary',
author_email = 'praneethbhandary@gmail.com',
packages = find_packages(),
install_requires = get_requirements('requirements.txt')
)
