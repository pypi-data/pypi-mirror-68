# KlondBar \m/_(>_<)_\m/
*coded by dAriush* 

## what is klondbar?
klondbar is a simple progress bar package with lots of customizations!
here are some of this customizable features:

* adding header to progress bar
* changing bar width
* changing the color of progress bar

## how to install klondbar?
use pip like any other package:

    pip install klondbar
    
    or: python3 -m pip install klondbar

## How to use:

at this version of klondbar there is two different types of progress bar available:

1. Mega Bar
2. Micro Bar

### Fast Usage Guide

*Just wrap for loop sequence with **micro_bar()** or **mega_bar()***

**mega_bar Fast Usage Sample Code:**

```python
from klondbar.megabar import mega_bar
import time
for i in mega_bar(range(10)):
    # place your calculations here
    time.sleep(0.1)  # just an exapmle of calculations
```

Here's example of mega_bar output:

![megabar_output](https://gitlab.com/dariush-bahrami/klondbar_project/-/raw/master/megabar_output%20example.png?inline=false)



**micro_bar Fast Usage Sample Code:**

```python
from klondbar.microbar import micro_bar
import time
for i in micro_bar(range(10)):
    # place your calculations here
    time.sleep(0.1)  # just an exapmle of calculations
```

Here's example of micro_bar output:

![micro_bar output](https://gitlab.com/dariush-bahrami/klondbar_project/-/raw/master/microbar_output%20example.png?inline=false)

**for more usage guide use following jupyter notebook:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dariush-bahrami/klondbar_project/blob/master/klondbar_guide.ipynb)

## More information

* code repository: https://gitlab.com/dariush-bahrami/klondbar_project.git
* PyPI page: https://pypi.org/project/klondbar/
* dAriush email address: dariush.bahrami@ut.ac.ir