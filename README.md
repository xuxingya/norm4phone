# Phone-Normalizer
## What is Phone Normalizer?

Phone Normalizer is a python implement of [AfterShip](https://github.com/AfterShip)/**[phone](https://github.com/AfterShip/phone)**

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

## Usage

```python
import PhoneNormalizer
pn = PhoneNormalizer(default_country='China')
pn.normalize_phone_num('+8613314672720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('+86 13314672720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('13314672720') //return['+8613314672720', 'CHN']
pn.normalize_phone_num('86 13314672720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('(86) 13314672720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('(+86) 13314672720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('+(86) 13314672720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('+86 133-146-72720') //return ['+8613314672720', 'CHN']
pn.normalize_phone_num('1 6479392750') //return ['+16479392750', 'CAN']
```

If you want to validate landline phone numbers, set `allowLandline` to true:

```
pn.normalize_phone_num('+(852) 2356-4902', '', true)
```


