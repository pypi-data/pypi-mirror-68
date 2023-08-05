<!-- # utils4ymc [![Version][version-badge]][version-link] ![MIT License][license-badge] -->


Making our programing more efficient.


`utils4ymc` 是一个Yummy Chen为自己提高效率，复用代码的库。


### 示例

#### Decos装饰器工具
* 记录函数运行时间工具 logger
```python
@logger(log_path)
def func(*args):
    pass
```
* 检查参数的输入类型
* 记录函数运行时间工具 logger
```python
@@type_assert(*types)
def func(*args):
    pass
```

#### Tools 计算工具
* One-hot

* dist
计算两个高阶向量的距离，支持L1、L2距离。


### 使用方式

``` python
from utils4ymc import *
```

### 安装

```
$ pip install utils4ymc
```


### License

[MIT](https://github.com/Interesting6/utils4ymc/blob/master/LICENSE)


<!-- [version-badge]:   https://img.shields.io/badge/version-0.1-brightgreen.svg
[version-link]:    https://pypi.python.org/pypi/douyin_image/
[license-badge]:   https://img.shields.io/github/license/pythonml/douyin_image.svg -->
