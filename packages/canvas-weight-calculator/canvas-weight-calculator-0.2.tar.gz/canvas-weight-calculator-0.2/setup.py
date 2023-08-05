from setuptools import setup, find_packages

setup(
    name='canvas-weight-calculator',
    version='0.2',
    license='MIT',
    py_modules=['gamification'],
    packages=find_packages(),
    author='Keyvan Khademi',
    author_email="keyvankhademi@gmail.com",
    url='https://github.com/keyvankhademi/canvas-weight-calculator',
    download_url='https://github.com/keyvankhademi/canvas-weight-calculator/archive/v0.2.tar.gz',
    keywords=['Canvas', 'Gamification'],
    include_package_data=True,
    install_requires=[
        'Click',
        'canvasapi',
    ],
    entry_points='''
    [console_scripts]
    gamification=gamification:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
