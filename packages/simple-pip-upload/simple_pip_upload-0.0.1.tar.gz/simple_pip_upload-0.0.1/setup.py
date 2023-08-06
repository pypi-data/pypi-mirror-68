import setuptools

setuptools.setup(
    name="simple_pip_upload",
    version="0.0.1",
    author="moumoubaimifan",
    author_email="example@example.com",
    description="一个简单的四则运算 PIP 上传例子",
    long_description="一个简单的 PIP 上传测试",
    long_description_content_type="text/markdown",
    url="https://simple_pip_upload.xx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)