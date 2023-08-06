import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setuptools.setup(
    name="git-issue-tracker",
    version=version,
    author="Aleksandr Belyaev",
    author_email="lexbel89@gmail.com",
    description="Git issue tracker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lexbel/git_issue_tracker",
    packages=setuptools.find_packages(),
    install_requires=[
        "injector==0.18.3",
        "Flask==1.1.1",
        "Flask-Injector==0.12.3",
        "GitPython==3.1.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
