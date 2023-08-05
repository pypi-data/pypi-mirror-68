import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='web-downloader', # Replace with your own username
    version='0.0.7',
    author='Gabriel Chung',
    author_email='gabrielchung1128@gmail.com',
    description='A Python package using Selenium to download web content',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://github.com/gabrielchung/WebDownloader',
    packages=setuptools.find_packages(),
    install_requires=[
        'selenium',
        'pyautogui',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    python_requires='>=3.6',
)