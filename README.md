# norm4phone
## What is norm4phone?

norm4phone is a python implement of [AfterShip](https://github.com/AfterShip)/**[phone](https://github.com/AfterShip/phone)**

A common problem is that users normally input phone numbers in this way:

```
`(817) 569-8900` or
`817569-8900` or
`1(817) 569-8900` or
`+1(817) 569-8900` or ...
```

We always want:

```
+18175698900
```
## Install
```python
$ pip install norm4phone
```
## Usage

```python
from norm4phone import PhoneNormalizer
pn = PhoneNormalizer(default_country='China')
pn.parse('+8613314672720') //return ['+8613314672720', 'CHN']
pn.parse('+86 13314672720') //return ['+8613314672720', 'CHN']
pn.parse('13314672720') //return['+8613314672720', 'CHN']
pn.parse('86 13314672720') //return ['+8613314672720', 'CHN']
pn.parse('(86) 13314672720') //return ['+8613314672720', 'CHN']
pn.parse('(+86) 13314672720') //return ['+8613314672720', 'CHN']
pn.parse('+(86) 13314672720') //return ['+8613314672720', 'CHN']
pn.parse('+86 133-146-72720') //return ['+8613314672720', 'CHN']
pn.parse('1 6479392750') //return ['+16479392750', 'CAN']
```

If you want to validate landline phone numbers, set `allowLandline` to true:

```
pn.parse('+(852) 2356-4902', '', true)
```


