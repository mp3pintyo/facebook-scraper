from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="facebook_page_scraper",
    version="1.0.0",
    author="Pintér Zsolt",
    description="Facebook oldal bejegyzés gyűjtő script Selenium WebDriver használatával",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mp3pintyo/facebook-scraper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "facebook-scraper=app:main",
        ],
    },
)
