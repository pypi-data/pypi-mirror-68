from setuptools import setup, find_packages
#packages = ["cnex_dfx"]
#python setup.py sdist upload  

setup(
    name = 'cnex_dfx',
    version = '2.2.6',
    keywords = ['cnexlabs', 'dfx', 'dump'],
    description = 'cnexlabs tool for dump dfx files',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
    license = 'MIT License',
	url = 'https://pypi.org/project/cnex_dfx',
    #install_requires = [],
    packages = find_packages(),
    include_package_data=True, 
    author = 'yuwen123441',
    author_email = 'yuwen123441@qq.com',
    platforms = 'any',
    entry_points = {
        'console_scripts': [
        'cnex_dfx = cnex_dfx.run:main'
        ]}
)