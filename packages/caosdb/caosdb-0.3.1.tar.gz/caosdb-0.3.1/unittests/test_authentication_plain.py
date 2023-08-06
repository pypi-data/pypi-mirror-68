# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
"""test_authentication_plain.

Unit tests for the modul caosdb.connection.authentication.plain.
"""

from __future__ import unicode_literals
from pytest import raises
from caosdb.connection.authentication.plain import PlainTextCredentialsProvider


def test_subclass_configure():
    """Test the correct passing of the password argument."""
    class SubClassOf(PlainTextCredentialsProvider):
        """A simple subclass of PlainTextCredentialsProvider."""

        def configure(self, **config):
            super(SubClassOf, self).configure(password="added in subclass", **config)

    instance = SubClassOf()
    instance.configure()
    assert instance.password == "added in subclass"

    instance.configure(**{"somearg": "BLA"})
    assert instance.password == "added in subclass"

    instance.configure(somearg="BLA")
    assert instance.password == "added in subclass"

    with raises(TypeError) as exc_info:
        instance.configure(password="OH NO!")
    assert exc_info.value.args[0] == ("configure() got multiple values for "
                                      "keyword argument 'password'")


def test_plain_has_logger():
    p = PlainTextCredentialsProvider()
    assert hasattr(p, "logger")
    assert p.logger.name == "authentication"
