# STools

#### 介绍

基于 Python 的数学工具箱，致力于复现 matlab 的一些好用的函数。

#### 安装教程

```bash
python setup.py build
python setup.py sdist
pip install .\dist\stools-0.x.x.tar.gz ( 根据实际情况修改文件名 )
pip install --upgrade .\dist\stools-0.x.x.tar.gz ( 更新 根据实际情况修改文件名 )
```

#### 使用说明

例子：

```python

from stools import Ssound, Swave

s = Ssound.Sound()
s.play_ndarray(Swave.sine(440, 2, 44100), level=5)

```
