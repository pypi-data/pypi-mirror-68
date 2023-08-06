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

class DameMinMax(object):
    def __init__(self, l):
        self.l = l

    def minmax(self):
        n = len(self.l)
        counter = 0
        if n == 0:
            return

        elif n == 1:
            min = max = self.l[0]

        elif n == 2:
            # 1 compare for 2 elements
            counter +=1
            if self.l[0] < self.l[n-1]:
                min = self.l[0]
                max = self.l[n-1]
            else:
                min = self.l[n-1]
                max = self.l[0]

        else:
                # 1 compare between 1st and last element
                counter +=1
                if self.l[0] < self.l[n-1]:
                    min = self.l[0]
                    max = self.l[n-1]
                else:
                    min = self.l[n-1]
                    max = self.l[0]

                mid = int((n-2)/2) + ((n-2) % 2 > 0)

                for i in range (1,mid+1):
                    # maximum 3 compares for any 2 elements
                    counter += 1
                    if (self.l[i] < self.l[n-i-1]):
                        counter += 1
                        if (self.l[i] < min):
                            min = self.l[i]
                        counter += 1
                        if (self.l[n-i-1] > max):
                            max = self.l[n-i-1]
                    else:
                        counter += 1
                        if self.l[n-i-1] < min:
                            min = self.l[n-i-1]
                        counter += 1
                        if self.l[i] > max:
                            max = self.l[i]
        l = [min, max, n, counter]
        return(l)
        # print("\noriginal list: " , str(L)[1:-1])
        # print("min: " , min)
        # print("max: " , max)
        # print("Length of list: " , n)
        # print("total comparisons: ", counter , "\n")


def main():

        self.minmax([9, 3, 5, 10, 1, 7, 12])
        #minmax([5,78,99,4,890,76543,8])
        #minmax([9, 3, 5, 10, 1, 7])
        #minmax([1, 3, 5, 8, 4, 10])
        #minmax([10, 3, 5, 8, 7, 1])
        #minmax([4, 3, 5, 1, 7, 10])
        self.minmax([9, 3, 5, 10, 1, 7 , 5,78,99,4,890,76543,8,67,89,34,2,1,6,7,0,56,58])
        self.minmax([])
        self.minmax([3])
        self.minmax([5,4])
        self.minmax([5,4,3])


if __name__ == "__main__":
        main()
