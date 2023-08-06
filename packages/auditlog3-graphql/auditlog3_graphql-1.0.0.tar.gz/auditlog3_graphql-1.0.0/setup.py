import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auditlog3_graphql",  # Replace with your own username
    version="1.0.0",
    author="Adekunle",
    author_email="olayinkakunle24@gmail.com",
    description="django-auditlog for Django 3.0 and Graphql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjkester/django-auditlog/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
