"""
Phone Number Normalizer
"""
import os
import json
import re
from typing import List, Union, Any

dirname = os.path.dirname(__file__)

class PhoneNormalizer:

    def __init__(self, default_country='China'):
        # default phone country is set to China(38)
        self.iso3166_data = json.load(open(os.path.join(dirname,'iso3166Data.json'), 'rb'))
        self.default = next(i for i, v in enumerate(self.iso3166_data) if v['country_name']==default_country)

    def get_iso3166(self, country: str) -> dict:
        if len(country) == 0:
            return self.iso3166_data[self.default]

        elif len(country) == 2:
            for _ in self.iso3166_data:
                if _['alpha2'] == country.upper():
                    return _

        elif len(country) == 3:
            for _ in self.iso3166_data:
                if _['alpha3'] == country.upper():
                    return _

        for _ in self.iso3166_data:
            if _['country_name'].upper() == country.upper():
                return _
        return {}

    def get_iso3166_by_phone(self, phone: str, allow_landline=False) -> Union[dict, Any]:
        exact_result, possible_result = {}, {}
        filtered_by_country_code = filter(lambda x: phone.startswith(x['country_code']), self.iso3166_data)
        tmp = filter(
            lambda x: any((length + len(x['country_code'])) == len(phone) for length in x['phone_number_lengths']),
            filtered_by_country_code)

        def begin_filter(x):
            # some country doesn't have mobile_begin_with
            if x['mobile_begin_with'] and not allow_landline:
                return any(phone.startswith(x['country_code'] + beginWith) for beginWith in x['mobile_begin_with'])
            return True

        for item in tmp:
            if begin_filter(item):
                exact_result = item
                break

        tmp = filter(
            lambda x: any((len(x['country_code']) + length + 1) == len(phone) for length in x['phone_number_lengths']),
            filtered_by_country_code)

        def begin_filter_2(x):
            # some country doesn't have mobile_begin_with
            if x['mobile_begin_with'] and not allow_landline:
                # delete trunk prefix
                return any(
                    re.match('^' + x['country_code'] + '\\d' + beginWith) for beginWith in x['mobile_begin_with'])
            return True

        for item in tmp:
            if begin_filter_2(item):
                possible_result = item
                break

        return exact_result, possible_result

    @staticmethod
    def validate_phone_iso3166(phone: str, iso3166: dict, allow_landline=False) -> bool:
        if not iso3166:
            return False
        phone_without_country = re.sub('^' + iso3166['country_code'], '', phone)
        is_length_valid = any(len(phone_without_country) == length for length in iso3166['phone_number_lengths'])
        if iso3166.get('mobile_begin_with'):
            is_begin_with_valid = any(
                phone_without_country.startswith(begin_with) for begin_with in iso3166['mobile_begin_with'])
        else:
            is_begin_with_valid = True

        return is_length_valid and (allow_landline or is_begin_with_valid)

    def parse(self, phone: str, country='', allow_landline=False) -> List[str]:
        result = []
        format_phone = phone.strip()
        format_country = country.strip()
        # like 86 13312341234 add +
        if len(format_phone.split()) == 2:
            format_phone = '+' + format_phone
        plus_sign = False
        if format_phone.startswith('+'):
            plus_sign = True
        format_phone = re.sub('[^0-9]', '', format_phone)
        iso3166 = self.get_iso3166(format_country)

        if len(iso3166) == 0:
            return result

        if format_country:
            # remove leading 0s for all countries except 'GAB', 'CIV', 'COG'
            if iso3166['alpha3'] in ['GAB', 'CIV', 'COG']:
                format_phone = format_phone.replace('0', '')

            # if input 89234567890, RUS, remove the 8
            if iso3166['alpha3'] == 'RUS' and len(format_phone) == 11 and format_phone.startswith('89'):
                format_phone = re.sub('^8+', '', format_phone)

            if not plus_sign and len(format_phone) in iso3166['phone_number_lengths']:
                format_phone = iso3166['country_code'] + format_phone

        elif plus_sign:
            # A: no country, have plus sign --> lookup country_code, length, and get the iso3166 directly.
            # also validation is done here. so, the iso3166 is the matched result.
            iso3166, possible_iso_3166 = self.get_iso3166_by_phone(format_phone)
            if not iso3166:
                # for some countries, the phone number usually includes one trunk prefix for local use
                # The UK mobile phone number ‘07911 123456’ in international format is ‘+44 7911 123456’, so without the first zero.
                # 8 (AAA) BBB-BB-BB, 0AA-BBBBBBB
                # the numbers should be omitted in international calls
                if possible_iso_3166:
                    iso3166 = possible_iso_3166
                    format_phone = iso3166['country_code'] + re.sub('^{}\\d'.format(iso3166['country_code']), '', format_phone)
                else:
                    iso3166 = {}

        elif len(format_phone) in iso3166['phone_number_lengths']:
            country_code = self.iso3166_data[self.default]['country_code']
            format_phone = country_code + format_phone

        validate_result = self.validate_phone_iso3166(format_phone, iso3166, allow_landline)

        if validate_result:
            return ['+' + format_phone, iso3166['alpha3']]

        return result


if __name__ == '__main__':
    pn = PhoneNormalizer(default_country='China')
    assert pn.parse('+8613314672720')==['+8613314672720', 'CHN']
    assert pn.parse('+86 13314672720') == ['+8613314672720', 'CHN']
    assert pn.parse('13314672720')==['+8613314672720', 'CHN']
    assert pn.parse('86 13314672720') == ['+8613314672720', 'CHN']
    assert pn.parse('(86) 13314672720') == ['+8613314672720', 'CHN']
    assert pn.parse('(+86) 13314672720') == ['+8613314672720', 'CHN']
    assert pn.parse('+(86) 13314672720') == ['+8613314672720', 'CHN']
    assert pn.parse('+86 133-146-72720') == ['+8613314672720', 'CHN']
    assert pn.parse('1 6479392750') == ['+16479392750', 'CAN']