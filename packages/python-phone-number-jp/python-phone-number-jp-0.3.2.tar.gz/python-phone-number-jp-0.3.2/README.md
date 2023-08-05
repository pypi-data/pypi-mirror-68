[![Build Status](https://travis-ci.org/torico-tokyo/python-phone-number-jp.svg?branch=master)](https://travis-ci.org/torico-tokyo/python-phone-number-jp)
[![Latest PyPI version](https://img.shields.io/pypi/v/python-phone-number-jp.svg)](https://pypi.python.org/pypi/python-phone-number-jp/)

# 日本の電話番号分割

日本の電話番号を簡易的に分割する

市外局番以下の分割はけっこう適当

(3セグメント目の方が長くなるように半分に分ける)

## requirements
* python3.6 or higher

## インストール

```
pip install python-phone-number-jp
```

## 使う

```
>>> from phone_number_jp import split_phone_number

>>> split_phone_number('09011112222')
('090', '1111', '2222')

>>> split_phone_number('0250111222')
('0250', '111', '222')

>>> split_phone_number('0251112222')
('025', '111', '2222')
```

## テスト
```
python setup.py test
```
