import setuptools
import json

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("package_metadata.json", "r") as fh:
    appVersion=json.loads( fh.read() )['version']

setuptools.setup(
    name="stock-price-alerts", # Replace with your own username
    version=appVersion,
    author="Alex Schittko",
    author_email="alex4108@live.com",
    description="Realtime alerts when your stocks cross thresholds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex4108/stock_price_alert_system",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
    entry_points ={ 
        'console_scripts': [ 
            'stock-price-alerts = src.tracker_v2:main'
        ] 
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)