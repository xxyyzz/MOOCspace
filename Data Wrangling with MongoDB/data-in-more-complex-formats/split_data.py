#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    data = list()
    results = list()
    n = 0
    with open(filename,'rb') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if line.startswith("<?xml") and len(data) > 0:
                results.append(data)
                data = list()
            else:
                data.append(line)

            if i == (len(lines)-1):
                results.append(data)

    for result in results:
        t = ET.ElementTree(ET.fromstringlist(result))
        new_filename = "{}-{}".format(filename, n)
        n += 1
        t.write(new_filename, xml_declaration = True, method = "xml", encoding="UTF-8")


    pass


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()