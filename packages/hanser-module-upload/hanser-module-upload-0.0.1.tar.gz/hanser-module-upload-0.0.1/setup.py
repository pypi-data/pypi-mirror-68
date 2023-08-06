# setup.py 是一个 setuptools 的构建脚本，其中包含了项目和代码文件的信息
# 如果没有需要先安装，pip install setuptools
import setuptools

setuptools.setup(
    # 项目的名称
    name="hanser-module-upload",
    # 项目的版本
    version="0.0.1",
    # 项目的作者
    author="布诺妮亚",
    # 作者的邮箱
    author_email="hanser@baka.com",
    # 项目描述
    description="简单的加减运算上传测试",
    # 项目的长描述
    long_description="简单的加减运算上传测试",
    # 以哪种文本格式显示长描述
    long_description_content_type="text/markdown",
    # 项目主页
    url="https://www.baidu.com",

    packages=setuptools.find_packages(),
    # 其他信息，这里写了使用 Python3，MIT License许可证，不依赖操作系统。
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)