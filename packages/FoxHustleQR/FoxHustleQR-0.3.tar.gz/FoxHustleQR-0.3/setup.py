from setuptools import setup

setup(name='FoxHustleQR',
    version='0.3',
    description='QR-code Generator',
    packages=['FoxHustleQR'],
    author='welcome32',
    author_email='welcome32@foxhustle.ru',
    zip_safe=False,
    install_requires=[
        'Pillow==7.1.2', 
        'PyQRCode==1.2.1',
        'requests==2.23.0',
    ], 
    python_requires='>=3.6',
    )