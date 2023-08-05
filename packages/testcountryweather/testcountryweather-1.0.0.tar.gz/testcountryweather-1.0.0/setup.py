from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="testcountryweather",
    version="1.0.0",
    description="A Python package to get weather reports for cities in any Country.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Raghu960/weather-reporter",
    author="Raghavendra Deshmukh",
    author_email="raghu.deshmukh55@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["weather_reporter"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "weather-reporter=weather_reporter.cli:main",
        ]
    },
)
