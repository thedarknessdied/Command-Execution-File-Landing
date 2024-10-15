# 命令执行-文件落地

## 项目介绍

​	这是一个简易的命令行运用项目，目的是方便渗透过程中文件落地。通过将文件内容渲染成多种上传模板，以命令行的形式运行相应的脚本文件使得目标文件落地。



## 项目架构

```cmd
Project
├─ run.py						# 项目主文件
│
├─ settings.py					# 项目配置文件
│	
├─ utils.py						# 项目脚手架文件
│
├─core							# 项目核心文件
│  ├─ __init__.py
│  │
│  ├─ file_system.py			# 文件处理
│  │
│  ├─ random_system.py			# 随机内容生成
│  │
│  └─ read_object.py			# 文件读取
│
├─dst							# 输出内容
│  └─ out.bat					
│
├─logs							# 日志
│
├─module						# 模板方法
│  ├─ __init__.py
│  │
│  └─ echo_certuil.py
│
├─read							# 读取方法
│  ├─ __init__.py
│  │
│  └─ whole_file2bytes.py
│
├─src							# 源文件
│  └─ payload.xml
│
└─tamper						# 加密/编码方法
   ├─ __init__.py
   │
   └─ tamper2base64.py
```



## 执行流程

1. 读取方法(read)，通过配置文件或者初始化过程中指定的read文件夹下的读取方法，读取src文件内容并生成迭代器

2. 加密/编码方法(tamper)，通过配置文件指定或者初始化过程中指定的tamper文件夹下的加密/编码方法，对迭代器的生成内容依次进行加密/编码方法

3. 模板方法(module)，通过配置文件指定或者初始化过程中指定的module文件夹下的模板方法，对内容进行重构，在dst目录下生成对应的脚本内容



## 自定义方法

### 1.读取方法(read)

```python
# -*- coding: utf-8 -*-


def read(
        path: str,
        *args, **kwargs
):
    /* *
    * 读取文件的方法
    */
    ... 
    
    yield 文件内容
```

​	read文件夹下的读取方法是可以自定义设计的，函数入口必须是read方法(在settings中定义)，在函数方法执行的末尾通过 `yield` 返回文件内容即可。



### 2.加密/编码方法

```python
# -*- coding: utf-8 -*-
import base64


def encode(data, *args, **kwargs):
    /* *
    * 数据编码/加密的方法
    */
    ... 
    
    return 编码/加密后数据
```

​	tamper文件夹下的加密/编码方法是可以自定义设计的，函数入口必须是encode方法(在settings中定义)，在函数方法执行的末尾通过 `return` 返回文件内容即可。



**注意：encode函数输入的data参数的类型和read方法的返回值是一致的**

### 3.模板方法

```python
# -*- coding: utf-8 -*-


def run(data, utils, *args, **kwargs):
    /* *
    * 数据模板化
    */
    ... 
    
    return 模板化数据
```

​	module文件夹下的模板方法是可以自定义设计的，函数入口必须是run方法(在settings中定义)，在函数方法执行的末尾通过 `return` 返回文件内容即可。



**注意：run函数输入的data参数的类型和encode方法的返回值是一致的**

**注意：run函数输入的utils参数是项目脚手架文件中Utils类的实例化，可以通过它调用其他Utils注册类**



##  演示

​	将 src 目录下的 test.txt 转换成 bat脚本 用于文件落地。

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/1.png)

​	这里将采用的利用链：read/whole_file2bytes.py(全文读取，并将文件内容以字节的形式传输) -> tamper/tamper2base64.py(将数据转换成base64编码形式进行传输) -> module/echo_certuil.py(通过echo-certuil的形式落地文件)

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/2.png)