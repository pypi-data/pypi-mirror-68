# <h2 id="title"> Thư viên Monitor trên ngôn ngữ Python để chạy monitor các function,... trong các project của Mobio.</h2>

# Copyright: MobioVN

# <h2 id="version">Version</h2>
Phiên bản hiện tại `0.6`

# <h2 id="ChangeLog">What news version 0.6</h2>
- Fix bugs

# <h2 id="ChangeLog">What news version 0.4</h2>
- Fix bugs

# <h2 id="ChangeLog">What news version 0.3</h2>
- Fix issue build Cython
- Option log args (Ex: monitor_func(self, threshold=-1, args_log_enable=False))

# <h2 id="ChangeLog">What news version 0.2</h2>
- Fix issue read config file
- Fix issue using with @staticmethod

# Cài đặt:
`pip3 install m-monitor`
hoặc add vào file requirements.txt

# Sử dụng:
1. Trước khi sử dụng cần tạo folder chứa file log. Ví dụ _monitor_logs_.
2. Khởi tạo và cấu hình cho object monitor.
```
monitor = Monitor()
# cấu hình trong code
monitor.config()
"""
:param file_max_bytes: Dung lượng tối đa của file log.
:param file_backup_count: Số lượng file log tối đa. Khi đạt số lượng file tối đa. Hệ thống sẽ quay vòng.
:param log_file_name: Đường dẫn đến file log.
:param func_threshold: Mức cảnh báo mặc định dùng chung. Nếu trên mức này --> ghi log. Có thể cấu hình riêng tuỳ biến khi sử dụng với từng function.
"""
# Hoặc cấu hình trong file config
config_from_file(self, config_file):
"""
:param config_file: duong dan file cau hinh cho module monitor.
"""
```
[Mẫu file config](https://gitbucket.mobio.vn/mobio/monitor/blob/master/monitor.conf)

3. Đặt decorate vào func cần monitor.

```
Example:
@monitor.monitor_func()
def executes1(x=1):
  time.sleep(1)


class Sample(object):
  def __init__(self):
    pass

  @staticmethod
  @monitor.monitor_func(2)
  def test():
    time.sleep(2)


executes1(x=2)
Sample.test()

# log file:
===============================================
# Time: 2019-02-16 12:37:18
# Duration: [1.00s]
Function: executes1
Kwargs:
  x: 2

===============================================
# Time: 2019-02-16 12:37:19
# Duration: [2.00s]
Function: test

```

# Build & distribute new version
## <h2 id="prepare">Prepare</h2>
1. Tạo tài khoản tại site: [https://test.pypi.org](https://test.pypi.org)
2. Tạo tài khoản tại site: [https://pypi.org/](https://pypi.org)

## <h2 id="build">Build</h2>
Make sure you have the latest versions of setuptools and wheel installed:

`python3 -m pip install --user --upgrade setuptools wheel`

Now run this command from the same directory where setup.py is located:

`python3 setup.py sdist`

## <h2 id="upload">Uploading the distribution archives</h2>
Now that you are registered, you can use [twine](https://packaging.python.org/key_projects/#twine) to upload the distribution packages. You’ll need to install Twine:

`python3 -m pip install --user --upgrade twine`

Once installed, run Twine to upload all of the archives under dist:

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

Upload to PyPI

`twine upload dist/*`