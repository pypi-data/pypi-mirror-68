#! python

#  test_cli.py: Test the command line interface.
#  Copyright (C) 2020  Delvian Valentine <delvian.valentine@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""usage: test_cli.py"""

__author__ = 'Delvian Valentine <delvian.valentine@gmail.com>'
__version__ = '2.0'

import os
import sys
import unittest

sys.path.insert(0, '..')

import contacts
from contacts import cli


class Delete(unittest.TestCase):
    """Delete contacts."""

    def setUp(self):
        """Delete contacts."""
        contacts.FILE = '.contacts'
        cli.main(['new', 'name', 'email'])
        cli.main(['delete', 'name'])

    def test_delete(self):
        """Test deleting contacts."""
        self.assertEqual({}, cli.load())

    def tearDown(self):
        """Remove the file."""
        os.remove(contacts.FILE)


class New(unittest.TestCase):
    """Store a new contact."""

    def setUp(self):
        """Store a new contact."""
        contacts.FILE = '.contacts'
        cli.main(['new', 'name', 'email'])

    def test_new(self):
        """Test storing a new contact."""
        self.assertEqual({'name': 'email'}, cli.load())

    def tearDown(self):
        """Remove the file."""
        os.remove(contacts.FILE)


class Update(unittest.TestCase):
    """Update a contact."""

    def setUp(self):
        """Edit a contact."""
        contacts.FILE = '.contacts'
        cli.main(['new', 'name', 'email'])
        cli.main(['update', 'name', '@'])

    def test_edit(self):
        """Test editing a contact."""
        self.assertEqual({'name': '@'}, cli.load())

    def tearDown(self):
        """Remove the file."""
        os.remove(contacts.FILE)


if __name__ == '__main__':
    unittest.main()
