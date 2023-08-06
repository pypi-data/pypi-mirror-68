## Desciption

Python utility to get the partial content of the web file or to unarchive a single file from a huge remote web zip.


## Installation

```shell
$ python3 -m pip install partial_web_file
```

## Usage

To get a part of the file from the Web:

```python
import partial_web_file

test_url = 'https://alexapps.net/files/mobile_app_boxingitimer_icon.png'
partial_content = partial_web_file.get_partial_web_file(test_url, start_position=1, length=3)
print(partial_content)  # prints "b'PNG'"
```

Imagine there is a huge zip file on the Web server. Downloading it takes time and network traffic. But you need only small file from that zip. Here is how to get that small file without full download:

```python
import partial_web_file

url_to_huge_zip = 'https://alexapps.net/files/huge.zip'
file_to_unzip = 'a/1.txt'
local_destination = '1.txt'

content = partial_web_file.get_file_content_from_web_zip(url_to_huge_zip, file_to_unzip)
with open(local_destination, 'w') as fout:
  fout.write(content)
```

If there are several files that need to be exctracted from the same remote zip file, do this:

```python
from partial_web_file import get_file_contents_from_web_zip


def on_content(path, content):
    if content is None:
        print('Fail for', path)
        return

    local_destination = os.path.basename(path)
    with open(local_destination, 'w') as fout:
        fout.write(content)


url_to_huge_zip = 'https://alexapps.net/files/huge.zip'
files_to_unzip = ['a/1.txt', 'b/2.txt']
get_file_contents_from_web_zip(url_to_huge_zip, files_to_unzip, on_content)
```
