import git
import setuptools

repository = git.Repo(".")

# Ensure that the Repo is clean
if repository.is_dirty():
    raise Exception("You have uncommitted local changes.")

# Find the current Commit (e.g., what we are building)
commit = repository.commit()

tags = list(filter(lambda t: t.commit == commit, repository.tags))
# Find a Tag corresponding to the current Commit, it one exists
if len(tags) == 1:
    tag = tags[0]
elif len(tags) > 1:
    raise NotImplementedError('many tags')
else:
    tag = None

# The Version is derived either from the Tag or the current Commit
if tag is not None:
    version = tag.name
else:
    version = commit.hexsha[0:7]

# Read the README
with open("README.rst", "r") as f:
    long_description = f.read()

# Read the Requirements
with open("requirements.txt") as f:
    required = f.read().splitlines()

# Build the Distribution
setuptools.setup(
    name="limecore-util",
    version=version,
    # Description
    description="limecore: Utilities",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # GitHub Link
    url="https://github.com/limecore/util",
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Owner Information
    author="Daniel Bradberry",
    author_email="daniel@danielbradberry.com",
    # License
    license="MIT",
    # Packages
    package_dir={"": "src"},
    packages=["limecore.util"],
    # Requirements
    install_requires=required,
    python_requires=">=3.6",
)
