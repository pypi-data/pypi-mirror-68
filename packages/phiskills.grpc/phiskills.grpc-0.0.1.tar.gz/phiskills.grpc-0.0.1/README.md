# Phi Skills Generic gRPC API Server for Python

| **Homepage** | [https://phiskills.com][0]        |
| ------------ | --------------------------------- | 
| **GitHub**   | [https://github.com/phiskills][1] |

## Overview

This project contains the Python module to create a generic **gRPC API Server**.

## Installation

```bash
pip install phiskills.grpc
```

## Creating the server

```python
from phiskills.grpc import Api

api = Api('My API')
xxx.add_XxxServicer_to_server(XxxServicer(), api.server)
api.start()
```
For more details, see [gRPC Basics - Python: Creating the server][10].

[0]: https://phiskills.com
[1]: https://github.com/phiskills
[10]: https://www.grpc.io/docs/tutorials/basic/python/#server
