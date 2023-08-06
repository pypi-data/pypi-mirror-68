# fastutils

Collection of simple utils.

## Install

```shell
pip install fastutils
```

## *NOTE:* Extra requirements for python 2.7

- funcsigs

## Installed Utils

- aesutils
- cacheutils
- dictutils
- funcutils
- hashutils
- imageutils
- jsonutils
- listutils
- rsautils
- sixutils
- strutils
- threadutils
- typingutils


## Usage Example

```python
from fastutils import strutils
assert strutils.split("a,b.c", [",", "."]) == ["a", "b", "c"]
```



## Releases

### v0.11.1 2020-05-19

- Add bizerror dependency.

### v0.10.0 2020-04-23

- Add strutils.is_chinese_character to test if the character is a chinese character.
- Add cacheutils.get_cached_value to get or set cached value.

### v0.9.0 2020-03-05

- Add listutils.append_new to append new value and only new value to the list.

### v0.8.0 2020-01-15

- Add strutils.smart_get_binary_data.
- Add rsautils.

### v0.7.0 2020-01-14

- Add hashutils.get_file_hash.
- Add extra install requires for python 2.x.
- Add imageutils.parse_base64image and imageutils.get_image_bytes.
- Fix jsonutils.make_simple_json_encoder ignore bases problem.

### v0.6.0 2020-01-07

- Add imageutils, add imageutils.get_base64image to make base64 image that can be rendered by web browser.
- Add imageutils.resize to scale image size.
- Add Image-Object-Encode support in jsonutils.
- Add threadutils, add threadutils.Service to simplify long-run-service programming.
- Raise bizerror.MissingParameter error in funcutils.get_inject_params while missing required parameter.

### v0.5.4 2019-12-10

- Fix hashutils.get_hash_hexdigest and hashutils.get_hash_base64 problem.

### v0.5.3 2019-12-08

- Using typingutils.smart_cast in funcutils.get_inject_params.

### v0.5.2 2019-12-08

- Add unit test cases for typingutils.
- Fix cast_list, do strip for every element in comma-separated-list.
- Fix base64 import missing in typingutils.

### v0.5.1 2019-12-08

- Add typingutils.cast_str.

### v0.5.0 2019-12-08

- Set library property in get_encoder in jsonutils.
- Add typingutils.

### v0.4.0 2019.12.07

- Add jsonutils, provides simple json encoder register system.

### v0.3.2 2019.10.29

- Fix problems for python 2.7.
- Fix name error of funcutils.

### v0.3.1 2019.10.28

- Fix problem casued by str.isascii() which is new from python 3.7.

### v0.3.0 2019.09.24

- Add listutils.unique to remove duplicated elements from the list.
- Add listutils.replace to replace element value in thelist with new_value in collection of map.

### v0.2.0 2019.09.10

- Add functuils.get_inject_params to smartly choose parameters from candidates by determine with the function's signature.
- Add functuils.call_with_inject to smartly call the function by smartly choose parameters.

### v0.1.1 2019.08.27

- Add strutils.wholestrip function, use to remove all white spaces in text.
- Fix strutils.is_urlsafeb64_decodable, strutils.is_base64_decodable and strutils.is_unhexlifiable functions, that have problem to test text contains whitespaces.

### v0.1.0 2019.08.23

- Add simple utils about operations of aes, dict, hash, list and str.
