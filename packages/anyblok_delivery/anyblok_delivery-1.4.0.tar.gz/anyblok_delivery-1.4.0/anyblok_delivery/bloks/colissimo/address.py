# This file is a part of the AnyBlok / Delivery project
#
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from logging import getLogger
from anyblok import Declarations
from sqlalchemy_utils.types.phone_number import PhoneNumberType


logger = getLogger(__name__)


def convert_phone(phone, region):
    if not phone:
        return ''

    if isinstance(phone, str):
        PhoneNumber = PhoneNumberType(region=region, max_length=20).python_type
        phone = PhoneNumber(phone, region)

    return phone.international.replace(' ', '')


def fr_adater(address, region):
    return {
        "companyName": address.company_name or '',
        "firstName": address.first_name or '',
        "lastName": address.last_name or '',
        "line0": "",
        "line1": "",
        "line2": "%s" % address.street1,
        "line3": "%s" % address.street2,
        "countryCode": "%s" % address.country.alpha_2,
        "city": "%s" % address.city.strip(),
        "zipCode": "%s" % address.zip_code.strip(),
        "mobileNumber": convert_phone(address.phone1, region),
        "phoneNumber": convert_phone(address.phone2, region),
    }


def be_adater(address, region):
    return {
        "companyName": address.company_name or '',
        "firstName": address.first_name or '',
        "lastName": address.last_name or '',
        "line0": "",
        "line1": "",
        "line2": "%s - %s" % (address.street1, address.street2),
        "line3": "%s" % address.street2,
        "countryCode": "%s" % address.country.alpha_2,
        "city": "%s" % address.city.strip(),
        "zipCode": "%s" % address.zip_code.strip(),
        "mobileNumber": convert_phone(address.phone1, region),
        "phoneNumber": convert_phone(address.phone2, region),
    }


@Declarations.register(Declarations.Model)
class Address:

    @classmethod
    def get_colissimo_adapter(cls):
        return {
            'FRA': fr_adater,
            'BEL': be_adater,
            'CHE': be_adater,
        }

    def get_colissimo_adapter_for_country(self):
        return self.registry.Address.get_colissimo_adapter().get(
            self.country.alpha_3, fr_adater)

    def get_colissimo(self):
        adapter = self.get_colissimo_adapter_for_country()
        return adapter(self, self.country.alpha_2)
