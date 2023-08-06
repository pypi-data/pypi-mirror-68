#! python

#  test_contacts.py: Test contacts.
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
"""usage: test_contacts.py"""

import os
import sys
import unittest

sys.path.insert(0, '..')

import contacts


class Load(unittest.TestCase):
    """Load the contacts."""

    def test_load(self):
        """Test loading the contacts."""
        self.assertEqual({}, contacts.load())


class Save(unittest.TestCase):
    """Save the contacts."""

    def setUp(self):
        """Save the contacts."""
        contacts.FILE = '.contacts'
        contacts.save({'name': 'email'})

    def test_save(self):
        """Test saving the contacts."""
        self.assertEqual({'name': 'email'}, contacts.load())

    def tearDown(self):
        """Remove the file."""
        os.remove(contacts.FILE)


class Search(unittest.TestCase):
    """Search the contacts."""

    def test_search(self):
        """Test searching the contacts."""
        self.assertEqual(['name'], contacts.search(['name'], {'name': 'email'}))


if __name__ == '__main__':
    unittest.main()
