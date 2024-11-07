# STools

#### Description

Python based math toolbox, dedicated to replicate some of the useful functions of matlab.

#### Installation

```bash
python setup.py build
python setup.py sdist
pip install.\dist\stools-0.x.x.tar.gz (Modify the file name as required)
pip install -- upgrade. \dist\stools-0.x.x.tar.gz (Update the file name based on the actual situation)
```

#### Instructions

Example:

```python
from stools import Ssound, Swave
s = Ssound.Sound()
s.play_ndarray(Swave.sine(440, 2, 44100), level=5)
```
