# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2019 Henrik tom Wörden
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
"""Tests for the Record class."""
# pylint: disable=missing-docstring
import unittest

from caosdb import Entity, Record


def test_is_entity():
    record = Record()
    assert isinstance(record, Entity)


def test_role():
    record = Record()
    assert record.role == "Record"


class TestRecord(unittest.TestCase):
    def test_property_access(self):
        rec = Record()
        rec.add_property("Prop")
        assert rec.get_property("Pop") is None
        assert rec.get_property("Prop") is not None
        assert rec.get_property("prop") is not None
        assert rec.get_property("prOp") is not None
