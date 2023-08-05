from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="my-annalisa-lambdata", # the name that you will install via pip
    version="1.0",
    author="Your Full Name",
    author_email="your@email.com",
    description="A short description",
    long_description=long_description,
    long_description_content_type="text/markdown", # required if using a md file for long desc
    #license="MIT",
    url="https://github.com/AnnalisaGibbs/lambdata-annalisagibbs",
    #keywords="",
    packages=find_packages() # ["my_lamdata"]
)