import setuptools

# adding README data as a long description
with open('README.md', 'r') as fp:
    long_description = fp.read()

# getting all requirements from package
requirements_path = 'helpers/requirements.txt'
requirements = []

with open(requirements_path, 'r') as fp:
    for line in fp:
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        requirements.append(line.strip())

setuptools.setup(
    name="helpers",
    version="0.0.1",
    author="Intellimind",
    author_email="hello@intellimind.io",
	license="MIT",
    description="general-utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IntelliMindTeam/helpers.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
	install_requires=requirements,
    dependency_links=[
        # link of pip installation from github without git+
    ],
    include_package_data=True,
)

