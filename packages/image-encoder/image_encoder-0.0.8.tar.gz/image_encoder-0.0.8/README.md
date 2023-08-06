# Image encoder for http

## Functions

Encode: Takes in a filepath to a jpg, returns a string representation of base64 encoded bytes

Decdode: Takes a string representation of base64 encoded bytes and returns PIL image


## Usage

**Python**

```python
from image_encoder.image_encoder import *
to_send = encode('filepath.jpg')
image = decode(to_send)
```


## Author  


Jagath Jai Kumar
