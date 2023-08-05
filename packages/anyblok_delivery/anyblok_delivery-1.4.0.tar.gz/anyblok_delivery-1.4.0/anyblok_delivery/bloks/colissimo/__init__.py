# This file is a part of the AnyBlok / Delivery project
#
#    Copyright (C) 2018 Franck Bret <franckbret@gmail.com>
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from anyblok_delivery.release import version
from logging import getLogger
logger = getLogger(__name__)


def import_declaration_module(reload=None):
    from . import colissimo
    from . import address
    if reload is not None:
        reload(colissimo)
        reload(address)


SERVICES = [
    ('France: Colissimo Domicile - sans signature', 'COLD'),
    ('France: Colissimo Domicile - avec signature', 'COL'),
    ('France: Colissimo - Point Retrait – en Bureau de Poste',  'BPR'),
    ('France: Colissimo - Point Retrait – en relais Pickup ou en '
     'consigne Pickup Station', 'A2P'),
    ('France: Colissimo Retour France', 'CORE'),
    ('France: Colissimo Flash - sans signature', 'COLR'),
    ('France: Colissimo Flash – avec signature', 'J+1'),
    ('International / Outre-Mer: Colissimo Retour International', 'CORI'),
    ('Outre-Mer: Colissimo Domicile - sans signature', 'COM'),
    ('Outre-Mer: Colissimo Domicile - avec signature', 'CDS'),
    ('Outre-Mer: Colissimo Eco OM', 'ECO'),
    ('International: Colissimo Expert International', 'COLI'),
    ('International: Offre Economique Grand Export (offre en '
     'test pour la Chine pour un client Pilote)', 'ACCI'),
    ('International (Europe): Colissimo - Point Retrait – en relais', 'CMT'),
    ('International (Europe): Colissimo - Point Retrait – Consigne '
     'Pickup Station – Sauf France et Belgique', 'PCS'),
    ('International (Europe) / France: Colissimo Domicile - sans signature',
     'DOM'),
    ('International (Europe) / France: Colissimo Domicile - avec signature',
     'DOS'),
    ('International (Europe): Colissimo Point Retrait – en bureau de poste',
     'BDP'),
]


class DeliveryColissimoBlok(Blok):
    """Delivery blok
    """
    version = version
    author = "Franck BRET"

    required = ['delivery']

    @classmethod
    def import_declaration_module(cls):
        import_declaration_module()

    @classmethod
    def reload_declaration_module(cls, reload):
        import_declaration_module(reload=reload)

    def update_colissimo(self):
        ca = self.registry.Delivery.Carrier.insert(
            name="Colissimo", code="COLISSIMO")
        ca_cred = self.registry.Delivery.Carrier.Credential.insert()
        for (name, product_code) in SERVICES:
            self.registry.Delivery.Carrier.Service.Colissimo.insert(
                name=name, product_code=product_code,
                carrier=ca, credential=ca_cred)

    def update(self, latest):
        if latest is None:
            self.update_colissimo()
