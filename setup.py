from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="e2e-password-generator",
    version="1.0.0",
    author="Anton B",
    description="Test fixture for AgentKit workflow engine - generates strong random passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anton-b/e2e-password-generator",
    py_modules=["passgen"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "passgen=passgen:main",
        ],
    },
)
