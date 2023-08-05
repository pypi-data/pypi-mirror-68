#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez

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
# along with Damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import csv
import json

femalescsv = "femalesbyyear.csv"
malescsv = "malesbyyear.csv"
dicc = {}

with open(femalescsv) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(reader, None)
    l = []
    dicc = {}
    for row1 in reader:
        # this for is only to set the dicc
        dicc[row1[1]] = {}
print(dicc)
csvfile.close()                

with open(femalescsv) as csvfile2:
    reader2 = csv.reader(csvfile2, delimiter=',', quotechar='|')
    next(reader2, None)        
    for row2 in reader2:
        dicc[row2[1]][row2[2]] = {}
        dicc[row2[1]][row2[2]]["male"] = {}
        dicc[row2[1]][row2[2]]["female"] = {}                
csvfile2.close()        
print(dicc)

with open(femalescsv) as csvfile3:
    reader3 = csv.reader(csvfile3, delimiter=',', quotechar='|')
    next(reader3, None)        
    for row3 in reader3:
        dicc[row3[1]][row3[2]]["female"] = row3[0]             
csvfile3.close()        
print(dicc)

for i in dicc.keys():
    males = 0
    females = 0
    for j in dicc[i].keys():
        if (('""".."""' == dicc[i][j]["female"]) or (dicc[i][j]["female"].isspace())):
            num = 0
        else:
            num = dicc[i][j]["female"]
        print(num)
        print(int(num))
        females = females + int(num)
        
    dicc[i]["females"] = females

for i in dicc.keys():
    males = 0
    females = 0
    for j in dicc[i].keys():
        if (('""".."""' == dicc[i][j]["male"]) or (dicc[i][j]["male"].isspace())):
            num = 0
        else:
            num = dicc[i][j]["male"]
        print(num)
        print(int(num))
        males = males + int(num)
        
    dicc[i]["males"] = males
    
print(dicc)


# with open(nzpathyears) as csvfile4:
#     reader4 = csv.reader(csvfile4, delimiter=',', quotechar='|')
#     next(reader4, None)
#     for row4 in reader4:
#         if (row4[1] == 'Girls'):
#             dicc[row4[3]][row4[0]]["female"] = row4[4]
#         elif (row4[1] == 'Boys'):
#             dicc[row4[3]][row4[0]]["male"] = row4[4]
# print(dicc)
            
# print(dicc.keys())
# for i in dicc.keys():
#     males = 0
#     females = 0
#     for j in dicc[i].keys():
#         if (dicc[i][j]["female"] == {}):
#             num = 0
#         else:
#             num = dicc[i][j]["female"]
#         females = females + int(num)
#         if (dicc[i][j]["male"] == {}):
#             num = 0
#         else:
#             num = dicc[i][j]["male"]
#         males = males + int(num)
        
#     dicc[i]["females"] = females
#     dicc[i]["males"] = males            

# print(dicc["Paula"]["females"])
# jsonvar = json.dumps(dicc)
# fo = open("nznames.json", "w")
# fo.write(jsonvar)
# fo.close()


