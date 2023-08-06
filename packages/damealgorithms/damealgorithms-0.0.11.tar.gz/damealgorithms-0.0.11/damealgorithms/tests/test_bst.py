#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damealgorithms; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from unittest import TestCase
from src.bst import BinarySearchTree

class TestBst(TestCase):

    def test_bst_create(self):
        btree = BinarySearchTree()
        vals = [5, 3, 9, 4, 1, 7, 30]
        for val in vals:
            btree.insert(val)
        self.assertEqual(int(btree.size()), 7)

    def test_bst_find(self):
        btree = BinarySearchTree()
        vals = [5, 3, 9, 4, 1, 7, 30]
        for val in vals:
            btree.insert(val)
        self.assertFalse(btree.find(8))
        self.assertTrue(btree.find(7))
        self.assertTrue(btree.find(1))
