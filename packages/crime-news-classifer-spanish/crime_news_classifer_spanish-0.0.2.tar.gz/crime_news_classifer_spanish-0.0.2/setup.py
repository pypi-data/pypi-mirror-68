import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crime_news_classifer_spanish",
    version="0.0.2",
    author="Hugo J. Bello",
    author_email="hjbello.wk@gmail.com",
    description="A classifier for crime and violence newspaper news in spanish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/news-scrapers/crime-in-news-classifier",
    packages=setuptools.find_packages(),
    package_data={'crime_news_classifer_spanish': ['saved_models/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)