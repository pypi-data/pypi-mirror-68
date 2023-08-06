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
# along with Damenumpy; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from unittest import TestCase
import cv2 
import os 

import numpy as np

class TestBasics(TestCase):

    def test_write(self):
        # Image path 
        image_path = 'files/img/woman1.jpg'
  
        # Image directory 
        directory = 'files/img'
  
        # Using cv2.imread() method 
        # to read the image 
        img = cv2.imread(image_path)   
  
        # Filename 
        filename = 'files/img/savedImage.jpg'
  
        # Using cv2.imwrite() method 
        # Saving the image 
        cv2.imwrite(filename, img) 
        
        self.assertEqual(len(os.listdir(directory)), 14)
        
        try:
            os.remove(filename)
            self.assertEqual(len(os.listdir(directory)), 13)
        except OSError as e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename, e.strerror))

