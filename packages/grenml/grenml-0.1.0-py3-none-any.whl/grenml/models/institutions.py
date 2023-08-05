"""
Copyright 2020 CANARIE Inc.

SPDX-License-Identifier: Apache License 2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------------------------------------------------------------------

Synopsis: The representation of an institution in the GRENML topology
"""
from .meta import GRENMLObject, Location
from grenml.exceptions import AttributeTypeError

INSTITUTION_TYPES = [
    'rren', 'nren', 'ran', 'university', 'global', 'other',
]


class Institution(Location, GRENMLObject):
    """
    Represents a connected institution or a REN
    (Research and Education Network)
    or any other organisation entity. Frequently used to represent "ownership"
    of NetworkObjects, as in "Link A belongs to NREN X and RREN Y".
    """

    def __init__(
            self, id=None, name=None, short_name=None, institution_type=None,
            longitude=None, latitude=None, altitude=None, unlocode=None, address=None,
            version=None, **kwargs
    ):
        super().__init__(
            id=id, name=name, short_name=short_name, longitude=longitude, latitude=latitude,
            altitude=altitude, unlocode=unlocode, address=address, version=version,
            **kwargs
        )
        if not institution_type:
            institution_type = 'other'
        self.type = institution_type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if str(type).lower() not in INSTITUTION_TYPES:
            raise AttributeTypeError
        self._type = str(type).lower()
