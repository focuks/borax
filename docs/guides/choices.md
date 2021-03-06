# choices 模块

> 模块： `borax.choices`



## 背景

`borax.choices` 的出现是为了解决 `django.db.models.Field` 中 choices 的一些缺点。下面是一个典型的使用示例：

```python
from django.db import models

class Student(models.Model):
    MALE = 'male' # 1
    FEMALE = 'female'
    UNKOWN = 'unkown'
    
    GENDER_CHOICES = (
        (MALE, 'male'), # 2
        (FEMALE, 'famale'),
        (UNKOWN, 'unkown')
    )
    gender = models.IntergerFIeld(
        choices=GENDER_CHOICES,
        default=UNKOWN
    )
```

从上面的例子可以看出：

- choices 的定义冗长，每一个选项的内容通常会出现两次
- 每个选项都是挂在 model 下的，即使用 `Student.MALE` 形式访问，当同一个model出现多个choices时，无法很好的区分

使用 Borax.Choices 可解决上述两个问题，并且代码更为简洁：

```python
from django.db import models
from borax import choices

class GenderChoices(choices.ConstChoices):
    MALE = choices.Item(1, 'male')
    FEMALE = choices.Item(2, 'female')
    UNKOWN = choices.Item(3, 'unkown')
    
class Student(models.Model):        
    gender = models.IntergerFIeld(
        choices=GenderChoices,
        default=GenderChoices.UNKOWN
    )
```

## 使用示例

每个可选选项集合都继承自 `choices.ConstChoices`, 并使用 `choices.Item` 列出所有的可选项。

```python
from borax import choices

class YearInSchoolChoices(choices.ConstChoices):
    FRESHMAN = choices.Item('FR', 'Freshman')
    SOPHOMORE = choices.Item('SO', 'Sophomore')
    JUNIOR = choices.Item('JR', 'Junior')
    SENIOR = choices.Item('SR', 'Senior')
```

可以直接使用 `YearInShoolChoices.FRESHMAN` 访问该选项具体的值。

 ```bash
 >>> YearInShoolChoices.FRESHMAN
'FR'
>>> YearInShoolChoices.is_valid('SR')
True
>>> YearInShoolChoices.is_valid('Et')
False
 ```

 ## 简单选项

在某些选项稀少、意义明确的情况下，可以只使用简单的数据类型定义选项，这些形式包括：

- 含有2个元素的列表或元组
- 一个单值对象，仅限 `int`，`float`，`str`，`bytes` 四种类型

`ConstChoices` 将自动生成一个新的 `Item` 对象。以下四个语句是等效的（忽略order的值）：

```
NS = choices.Item('A', 'A')
NS = choices.Item('A')
NS = 'A', 'A'
NS = 'A'
```


例如上述 `YearInSchoolChoices` 也可以简写为

```python
class YearInSchoolChoices(choices.ConstChoices):
    FRESHMAN = 'FR', 'Freshman'
    SOPHOMORE = 'SO', 'Sophomore'
    JUNIOR = 'JR', 'Junior'
    SENIOR = 'SR', 'Senior'
```

## 选项(Item)定义

在类定义体使用 `<name> = <value>` 的格式定义选项。

名称 name 遵循 Python 变量命名规范，需要注意的是：

- 以下划线（"_"）开始的变量不视为一个有效的选项
- 变量名并不是必须使用大写形式

值 value 通常为一个 `Item` 对象，定义如下：

```python
def __init__(value, display=None, *, order=None):pass
```

参数说明如下：

- value ： 保存的值，在一个 Choices 中该值是唯一的
- display ： 可读的文本信息
- order ：用于排序的数字

## 选项复用和继承

可以使用类继承的方式实现选项的复用和重新定制某些选项的属性。

```python
from borax import choices

class VerticalChoices(choices.ConstChoices):
    S = choices.Item('S', 'south')
    N = choices.Item('N', 'north')


class DirectionChoices(VerticalChoices):
    E = choices.Item('E', 'east')
    W = choices.Item('W', 'west')
```
默认情况下，子类的选项在父类选项之后，但可以使用 `order` 属性以调整顺序。

## API

以下所有的方法均为 `ConstChoices` 类的属性和方法。

- **`ConstChoices.choices`**

所有选项列表。可直接用于 django.models.Field.choices 。

类似于 `[(value1, display1), (value2, display2), ...]` 。

- **`ConstChoices.is_valid(value)`**

检查 `value` 是否是有效的选项。

- **`ConstChoices.get_value_display(value)`**

获取某个选项的文本。

- **`ConstChoices.__iter__()`**

遍历 `ConstChoices.choices`

## 关于Django.Choices

### 概述

自 Django 3.0 起，Django 新增了使用枚举方式定义choices属性（[点击了解]( https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types )）。

和 `borax.Choices` 相比 Django.Choices具有以下特点：

| 主题           | 内容                                                         |
| -------------- | ------------------------------------------------------------ |
| 类层次         | 类层次是一样的，都是 “Choices - 选项实例 - 选项值”，只是每个层次的实现方式不同。 |
| 类型扩展       | 更为经常使用的类是 `models.TextChoices` 、 `models.IntegerChoices`  或其他自定义的类。这就要求所有的选项值总是同一类型的。 |
| 选项的创建方式 | 选项即 Borax.Choices 的 `Item` ， 在Django.Choices中即为`<Enum XxxMyChoices>` ，具有枚举类型的特性。在字面定义中，总是定义为 tuple 。 |
| 访问方式       | 在 Django.Choices 中， `<XxxChoices>.<XxxChoices>` 返回的 选项实例，而不是选项值。 |
| 扩展           | 在一个choices之上添加若干个选项形成新的choices。Borax.Choices 可以使用类继承解决。Django.Choices 不可以直接使用类继承 ，可参考 [《How to extend Python Enum? - Stack Overflow》](https://stackoverflow.com/questions/33679930/how-to-extend-python-enum) 这篇问答。 |

### API对照表

下表描述了 Borax.Choices 和 Django.Choices 之间的API差异。

```python
from django.db import models

from borax import choices

class MyChoices(models.TextChoices):
    GREEN = 'g', 'green'
    RED = 'r', 'red'
    YELLOW = 'y', 'yellow'

class MyChoices(choices.Choices):
    GREEN = 'g', 'green'
    RED = 'r', 'red'
    YELLOW = 'y', 'yellow'
```

表 Borax.Choices *VS* Django.Choices


|                             | Borax.Choices | Django.Choices     | 备注 |
| --------------------------- | ------------- | ------------------ | ---- |
| MyChoices.choices           | `(...)`       | `(...)`            |      |
| MyChoices.GREEN             | `'g'`         | `<Enum MyChoices>` |      |
| MyChoices['GREEN']          | -             | `<Enum MyChoices>` |      |
| MyChoices.is_valid('g')     | True          | -                  |      |
| MyChoices.GREEN.name        | -             | `'g'`              |      |
| MyChoices.GREEN.label       | -             | `'green'`          |      |
| MyChoices.GREEN.value       | -             | -                  |      |
| MyChoices.GREEN.display     | -             | -                  |      |
| MyChoices.get_value_display | `<label>`     | -                  |      |
| MyChoices._ _ iter _ _      | Y             | -                  |      |
| MyChoices.names             | -             | Y                  |      |
| MyChoices.values            | -             | Y                  |      |
| MyChoices.labels            | -             | Y                  |      |
| member in (check values)    | Y             | Y                  |      |
