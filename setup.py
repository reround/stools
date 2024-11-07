from setuptools import setup, find_packages

setup(
    # 包的名称
    name="stools",
    # 包的版本
    version="0.1.3",
    # 包的描述
    description="A short description of your package",
    # 长描述可以是从另一个文件中读取的
    # long_description=open("README.md").read() + open("CHANGELOG.txt").read(),
    # 包的URL
    # url="https://github.com/yourusername/your_package_name",
    # 作者
    author="Shun",
    # 作者的联系邮箱
    author_email="2716753570@qq.com",
    # 许可证类型
    license="MIT",
    # 包的分类器，可以从 https://pypi.org/classifiers/ 查找合适的分类器
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # 包的关键字
    keywords="tools signal processing",
    # 包的依赖
    install_requires=[
        # 依赖包
    ],
    packages=["stools"],
)
