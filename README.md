# 命令执行-文件落地

## 项目介绍

​	这是一个简易的命令行运用工具，仅通过配置配置文件(settings)就能够运行脚本，不需用额外的参数添加。项目的最终目标是方便渗透过程中各类文件落地。因为在渗透过程中可能会存在无法将大文件直接拉取到远程主机的可能性，所以这里采用分块封装的方法将大文件划分成为小模块，通过将多种上传模板，以命令行的形式生成对应的shell脚本，仅仅需要执行命令/脚本便能够使得文件落地。



## 项目架构

```cmd
Project
│
├─ settings.py					# 项目配置文件
│
├─ start.py						# 项目测试文件
│
├─ task.py						# 项目类文件（构造初始化项目）
│	
├─ utils.py						# 项目工厂文件（所有核心类的注册中心）
│
├─core							# 项目核心文件
│  ├─ __init__.py
│  │
│  ├─ FileDataIter.py			# 文件内容块存储
│  │
│  ├─ FileSystem.py				# 文件处理
│  │
│  ├─ FolderSystem.py			# 文件夹处理
│  │
│  ├─ ParseConfig.py			# 基础配置文件解析
│  │
│  ├─ ParseConfigPy.py			# Py类型配置文件解析
│  │
│  ├─ RandomSystem.py			# 随机数生成
│  │
│  ├─ ReadDataBlock.py			# 加工数据库链表
│  │
│  ├─ ReadDataIter.py			# 数据迭代器
│  │
│  └─ ReadFileSystem.py			# 文件读取系统
│
├─dst							# 脚本输出文件存储文件夹
│  └─ out.bat					
│
├─logs							# 日志存储文件夹
│
├─module						# 脚本生成文件存储文件夹
│  ├─ __init__.py
│  │
│  └─ echo_certuil.py			# echo + certuil + base64.decode 
│  │
│  └─ echo_certuil_hex.py	 	# echo + certuil + unhex
│  │
│  └─ echo_openssl_base64.py	# echo + Openssl + base64.decode 
│
├─read							# 文件读取方法存储文件夹
│  ├─ __init__.py
│  │
│  └─ whole_file2bytes.py		# 读取整个文件
│
├─src							# 源文件存储文件夹
│  └─ payload.xml				# 测试过程中所使用的源文件
│
└─tamper						# 数据加密/编码文件存储文件夹
   ├─ __init__.py
   │
   └─ tamper2base64.py			# base64编码数据
   │	
   └─ tamper2hex.py				# hex编码数据
```



## 项目模块

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/3.png)



## 执行流程

1. 通过选定的”文件读取方法存储文件夹“中的脚本文件，执行其read() ，获得一个DataGenerate(数据生成器)。DataGenerate(数据生成器)中，一个ReadDataIter(数据迭代对象)对象存储的数据来自于read方法返回的一个数据块，每个ReadDataIter对象存储的数据大小由read方法决定，而不是由配置文件决定。
2. DataGenerate每个ReadDataIter(数据迭代对象)对象通过选定的”数据加密/编码文件存储文件夹“中的脚本文件encode()获取编码/加密后数据。经过一次处理的数据会根据配置文件中预定的模块处理方式生成一个ProcessBlockList链表用于存储数据。ProcessBlockList链表中的每个ProcessBlockItem节点分别存储一定量的加密/编码数据片段。
3. 数据二次处理阶段，会遍历每个ReadDataIter，获取其中ReadDataIter对象存储的ProcessBlockList链表，通过选定的”脚本生成文件存储文件夹“中的脚本文本，执行run()方法渲染模板。



## 配置文件解析

```python
SETTINGS = {
    # 系统相关配置
    "SYSTEM": {
        # 默认脚本文件后缀
        "DEFAULT_FUNC_SUFFIX": "py",
		# 随机生成相关参数
        "RANDOM_SYSTEM": {
            # 随机数最小边界
            "MINIMUM_NUMBER_START": 1,
            # 随机数边界最大偏移值
            "MAX_NUMBER_OFFSET": 9,
            "ASCII_LOWERCASE": 'abcdefghijklmnopqrstuvwxyz',
            "ASCII_UPPERCASE": 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            "DIGITS": '0123456789',
            "UNDERLINE": "_",
        },
		# 文件系统相关参数
        "FILE_SYSTEM": {
            # 随机处理模块大小是否开启
            'RANDOM_PROCESS_BLOCK_ENABLE': False,
            # 是否需要划分处理模块
            'EDIT_PROCESS_BLOCK_ENABLE': True,
            # 一个处理模块固定大小
            'MAX_PROCESS_BLOCK_SIZE': 1024,
            # 是否需要随机数据填充
            'DEFAULT_CONTENT_ENABLE': False,
            # 随机填充内容大小
            'DEFAULT_CONTENT_SIZE': 0,
        },
		# 文件夹相关参数
        'FOLDER': {
            # 脚本输出文件存储文件夹
            'OUTPUT_FILE_FOLDER': "dst",
            # 源文件存储文件夹
            'INPUT_FILE_FOLDER': "src",
            'LOG_FILE_FOLDER': "logs",
            # 文件读取方法存储文件夹
            'READ_FILE_FOLDER': "read",
            # 核心代码文件夹
            'CORE_CODE_FILE_FOLDER': "core",
            # 数据加密/编码文件存储文件夹
            'TAMPER_FILE_FOLDER': "tamper",
            # 脚本生成文件存储文件夹
            'MODULE_FILE_FOLDER': "module",
        },
		# 日志相关参数
        "LOGGER": {
            "DEFAULT_LOG_SUFFIX": "log",
            "LOG_NAME_FORMAT": "%Y-%m-%d",
            "MES_FORMAT": '%(asctime)s - %(levelname)s - %(message)s',
            "LOG_LEVEL": "DEBUG",
        }
    },
	
    # 运行时相关配置
    'RUNNING': {
        # 待处理文件
        'INPUT_FILENAME': "payload.xml",
        # 脚本输出文件
        'OUTPUT_FILENAME': "out.bat",
		# 各类自定义方法入口点
        "ENTER_FUNCTION": {
            # 文件读取方法函数入口点
            'READ_ENTER_FUNCTION': 'read',
            # 数据加密/编码函数入口点
            'TAMPER_ENTER_FUNCTION': "encode",
            # 脚本生成文件函数入口点
            'MODULE_ENTER_FUNCTION': "run",
        },
		# 类方法标识符
        "START_SIGNAL": {
            # 文件读取方法函数标识符(用于区分文件读取方法函数和其他方法)
            'READ_ENTER_FUNCTION_START': 'read_data',
        },
		# 运行过程中使用的数据加密/编码函数列表
        'TAMPER_LIST': [
            'tamper2base64',
        ],
        # 运行过程中使用的脚本生成函数列表
        "MODULE_LIST": [
            'echo_openssl_base64',

        ],
        # 运行过程中使用的文件读取方法
        "READ_FUNCTION": "whole_file2bytes",
    }
}
```



## 自定义方法

​	读取方法、加密/编码方法、模板方法是可以自定义的，只需要按照特定的格式编写即可。

### 1.读取方法(read)

​	函数入口必须是read方法(在settings中定义)，在函数方法执行的末尾通过 `yield` 返回文件内容。

​	函数的参数由path(文件路径)和其他参数组成。

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



### 2.加密/编码方法

​	函数入口必须是encode方法(在settings中定义)，在函数方法执行的末尾通过 `return` 返回编码/加密后数据内容。

​	函数的参数由data(经过一次处理的数据内容)和其他参数组成。

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

**注意：encode函数输入的data参数的类型和read方法的返回值是一致的，这里建议都是用bytes类型**



### 3.模板方法

​	函数入口必须是run方法(在settings中定义)，在函数方法执行的末尾通过 `return` 返回模板内容。

​	函数的参数由data(经过一次处理的数据内容)、utils(工具类)、end(是否到达ProcessBlockList链表结尾，数据读取完结)和其他参数组成。

```python
# -*- coding: utf-8 -*-

# 源文件
src_filename = ""
# 目的文件
dst_filename = ""


def run(data, utils, end: bool, *args, **kwargs):
    /* *
    * 模板构造方法
    */
    ... 
    
    return 模板内容

```



**注意：run函数输入的data参数的类型和encode方法的返回值是一致的，这里建议都是用str类型**

**注意：run函数输入的utils参数是项目脚手架文件中Utils类的实例化，可以通过它调用其他Utils注册类**



## Utils 类

```
class Utils(object):
    MAX_STRING_LENGTH = 10

    def __init__(
            self,
            factory,
            config_filename: str = "settings.py"
    ):
        # 配置信息解析类
        self.__setting_system = ParseConfig(config_filename)

        # 文件夹处理
        self.__folder_system = FolderSystem(self)

        # 元类
        self.__factory = factory

        # 随机内容工具初始化
        self.__random_system = RandomSystem(self)

        # file_system.run 只需要提供read的脚本和文件的路径作为做基础的参数就可以运行读取文件
        self.__file_system = ReadSystem(self)

        # 日志系统
        self.__logger_system = LogSystem(self)
        self.__logger_system.info("test")

        # 文件内容分区工具
        self._file_data_iter = FileDataIter(self)
```

​	通过Utils 类能够访问所有的其他核心类对象。

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/4.png)

​	Utils类也将每个类的配置查询方法集成起来，不再需要通过复杂的链式调用获取属性值。



##  演示

​	将 src 目录下的 test.txt 转换成 bat脚本 用于文件落地。

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/1.png)

​	这里将采用的利用链：read/whole_file2bytes.py(全文读取，并将文件内容以字节的形式传输) -> tamper/tamper2base64.py(将数据转换成base64编码形式进行传输) -> module/echo_certuil.py(通过echo-certuil的形式落地文件)

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/2.png)