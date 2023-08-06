import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='chatbot-common-aiqingyuyan', # Replace with your own username
    version='0.0.3',
    author='Unknown',
    description='common package for chatbot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=['bot_common', 'bot_common.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)
