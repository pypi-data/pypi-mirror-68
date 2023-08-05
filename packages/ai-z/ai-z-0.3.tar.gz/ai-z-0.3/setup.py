import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai-z",
    version="0.3",
    license='MIT',
    author="Mathieu Poliquin",
    author_email="mathieu.poliquin@gmail.com",
    description="GPU usage graph in the terminal for AMD and NVIDIA GPUs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ai-z.org",
    install_requires=['py3nvml','numpy','psutil','py-cpuinfo','sparklines'],
    packages=setuptools.find_packages(),
    scripts=['bin/ai-z'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)