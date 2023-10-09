from setuptools import setup

setup(
    name='llm_test_helpers',
    version='0.1.0',    
    description='LLM test suite runner helpers',
    url='https://github.com/shuds13/pyexample',
    author='Nisala Kalupahana',
    author_email='nisala.a.kalupahana@vanderbilt.edu',
    license='AGPL-3.0',
    packages=['llm_test_helpers'],
    install_requires=['langchain', 'openai', 'pyyaml'],

    classifiers=[]
)