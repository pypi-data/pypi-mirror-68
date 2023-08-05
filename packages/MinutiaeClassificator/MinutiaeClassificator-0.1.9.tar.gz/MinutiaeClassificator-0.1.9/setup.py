from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='MinutiaeClassificator',
    version='0.1.9',
    license='MIT',
    description='Minutiae extraction and classification tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jakub Arendac',
    author_email='jakub.arendac105@gmail.com',
    url='https://github.com/jakubarendac/MinutiaeClassificator',
    download_url='https://github.com/jakubarendac/MinutiaeClassificator/archive/0.1.7.tar.gz',
    keywords=['minutiae', 'extraction', 'classification', 'biometrics'],
    # TODO : add needed packages
    install_requires=['opencv-python', 'keras==2.2.4','tensorflow==1.13.1','tensorflow-gpu==1.13.1', 'matplotlib', 'pillow', 'scikit-image'],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages()
)