# Command Execution-File Landing

## Project Introduce

​	This is a simple command-line application project aimed at facilitating file landing during the penetration process. By rendering the file content into various upload templates and running the corresponding script files in command-line format, the target file is landed.



## Project Architecture

```cmd
Project
├─ run.py						# Project master file
│
├─ settings.py					# Project configuration file
│	
├─ utils.py						# Project scaffolding files
│
├─core							# Core project documents
│  ├─ __init__.py
│  │
│  ├─ file_system.py			# File processing
│  │
│  ├─ random_system.py			# Random content generation
│  │
│  └─ read_object.py			# File reading
│
├─dst							# Output content
│  └─ out.bat					
│
├─logs							# Journal
│
├─module						# Template method
│  ├─ __init__.py
│  │
│  └─ echo_certuil.py
│
├─read							# Reading method
│  ├─ __init__.py
│  │
│  └─ whole_file2bytes.py
│
├─src							# source file
│  └─ payload.xml
│
└─tamper						# Encryption/Encoding method
   ├─ __init__.py
   │
   └─ tamper2base64.py
```



## Execution process

1. Read method, which reads the contents of the src file and generates an iterator through the read method specified in the configuration file or the read folder during initialization
2. Encryption/Encoding Method (tamper), which encrypts/encodes the generated content of the iterator sequentially by specifying the encryption/encoding method in the tamper folder specified in the configuration file or initialization process
3. Template method (module), which reconstructs the content by specifying the template method in the module folder specified in the configuration file or initialization process, and generates the corresponding script content in the dst directory



## Custom Method
### 1. Reading method (read)

```python
# -*- coding: utf-8 -*-
def read(path: str, *args, **kwargs):
    /* *
    *Method of reading files
    */
    ... 
    
	yield file content
```
​	The read method in the read folder can be custom designed, and the function entry must be the read method (defined in settings). At the end of the function method execution, the file content can be returned through 'yield'.



### 2. Encryption/Encoding Methods

```python
# -*- coding: utf-8 -*-
def encode(data, *args, **kwargs):
    /* *
    *Methods of data encoding/encryption
    */
    ... 

    return encoded/encrypted data
```
​	The encryption/encoding methods in the tamper folder can be custom designed, and the function entry must be the encode method (defined in settings). At the end of the function method execution, the file content can be returned through 'return'.

**Note: The type of the data parameter input to the encode function is consistent with the return value of the read method**

### 3. Template method

```python
# -*- coding: utf-8 -*-
def run(data,  utils, *args, **kwargs):
    /* *
    *Data templating
    */
    ... 

    return templated data
```
​	The template methods in the module folder can be custom designed, and the function entry must be the run method (defined in settings). At the end of the function method execution, the file content can be returned through 'return'.

**Note: The type of the data parameter input to the run function is consistent with the return value of the encode method**

**Note: The 'tils' parameter input to the' run 'function is an instantiation of the' Utils' class in the project scaffold file, which can be used to call other 'Utils' registration classes**



## Demo
​	Convert the test. txt file in the src directory to a bat script for file landing.

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/1.png)

​	The utilization chain that will be used here is: read/hole_file2bytes. py (read the entire text and transfer the file content in bytes) ->tamper/tamper2base64.py (convert the data to base64 encoding for transmission) ->module/echo_certuil. py (landing the file in the form of echo celltuil)

![](https://github.com/thedarknessdied/Command-Execution-File-Landing/blob/main/pic/2.png)
