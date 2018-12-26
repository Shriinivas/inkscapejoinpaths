#!/usr/bin/env python

'''
Inkscape extension to join the selected paths

Copyright (C) 2018  Shrinivas Kulkarni

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import inkex, cubicsuperpath
import copy

def floatCmpWithMargin(float1, float2, margin):
    return abs(float1 - float2) < margin 
    
def vectCmpWithMargin(vect1, vect2, margin):
    return all(floatCmpWithMargin(vect2[i], vect1[i], margin) for i in range(0, len(vect1)))

def getPartsFromCubicSuper(cspath):
    parts = []
    for subpath in cspath:
        part = []
        prevBezPt = None            
        for i, bezierPt in enumerate(subpath):
            if(prevBezPt != None):
                seg = [prevBezPt[1], prevBezPt[2], bezierPt[0], bezierPt[1]]
                part.append(seg)
            prevBezPt = bezierPt
        parts.append(part)
    return parts
        
def getCubicSuperFromParts(parts):
    cbsuper = []
    for part in parts:
        subpath = []
        lastPt = None
        pt = None
        for seg in part:
            if(pt == None):
                ptLeft = seg[0]
                pt = seg[0]
            ptRight = seg[1]
            subpath.append([ptLeft, pt, ptRight])
            ptLeft = seg[2]
            pt = seg[3]
        subpath.append([ptLeft, pt, pt])
        cbsuper.append(subpath)
    return cbsuper

class JoinPathsEffect(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        selections = self.selected        
        pathNodes = self.document.xpath('//svg:path',namespaces=inkex.NSS)

        paths = [(pathNode.get('id'), cubicsuperpath.parsePath(pathNode.get('d'))) \
            for pathNode in  pathNodes if (pathNode.get('id') in selections.keys() \
            and pathNode.get('d') != "")]

        if(len(paths) > 1):
            newParts = []
            firstElem = None
            for key, cspath in paths:
                parts = getPartsFromCubicSuper(cspath)
                start = parts[0][0][0]
                elem = selections[key]
                
                if(len(newParts) == 0):
                    newParts += parts[:]
                    firstElem = elem
                else:
                    if(vectCmpWithMargin(start, newParts[-1][-1][-1], margin = .01)):
                        newParts[-1] += parts[0]
                    else:
                        newSeg = [newParts[-1][-1][-1], newParts[-1][-1][-1], start, start]
                        newParts[-1].append(newSeg)                    
                        newParts[-1] += parts[0]
                    
                    if(len(parts) > 1):
                        newParts += parts[1:]
                
                parent = self.getParentNode(elem)
                idx = parent.index(elem)
                parent.remove(elem)

            newElem = copy.copy(firstElem)
            oldId = firstElem.get('id')
            newElem.set('d', cubicsuperpath.formatPath(getCubicSuperFromParts(newParts)))
            newElem.set('id', oldId + '_joined')
            parent.insert(idx, newElem)

effect = JoinPathsEffect()
effect.affect()
