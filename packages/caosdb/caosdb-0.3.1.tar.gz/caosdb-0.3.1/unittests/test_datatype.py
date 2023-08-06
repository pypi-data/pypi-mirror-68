# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (c) 2020 IndiScale GmbH
# Copyright (c) 2020 Daniel Hornung (d.hornung@indiscale.com)
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

import caosdb as db
from caosdb.common import datatype


def test_list():
    assert db.LIST("RT") == "LIST<RT>"
    assert db.LIST(db.RecordType("bla")) == "LIST<bla>"


def test_list_utilites():
    """Test for example if get_list_datatype works."""
    dtype = db.LIST(db.INTEGER)
    assert datatype.get_list_datatype(dtype) == db.INTEGER
