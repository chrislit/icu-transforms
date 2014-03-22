# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re, codecs

E = codecs.open('Unicode-MdC-Mapping-v1.utf8', 'r', 'utf-8').readlines()
E.reverse()

M = codecs.open('Egyptian_Latin_MdC.txt', 'w', 'utf-8')
G = codecs.open('Egyptian_Latin_Gardiner.txt', 'w', 'utf-8')
S = codecs.open('Egyptian_Latin_GSL.txt', 'w', 'utf-8')

header1 = '# **************************************************************************\n# *\n# *  Copyright (C) 2014, CrossWire Bible Society\n# *  All Rights Reserved.\n# *\n# ***************************************************************************\n'
header2 = '# Generated from CLDR\n\n'
header3 = '# Based on UTN32\n\n'
header4 = ':: [:Egyptian_Hieroglyphs:];\n\n([:Egyptian_Hieroglyphs:])([:Egyptian_Hieroglyphs:])>|$1\-$2;\n\n'


M.write(header1)
M.write('# File: Egyptian_Latin_MdC.txt\n')
M.write(header2)
M.write('# Transliteration between Egyptian Hieroglyphs and their Manual de Codage\n# transliteration, with fallback to the Gardiner sign list number\n\n')
M.write(header3)
M.write('# Egyptian-Latin/MdC\n\n')
M.write(header4)

G.write(header1)
G.write('# File: Egyptian_Latin_Gardiner.txt\n')
G.write(header2)
G.write('# Transliteration between Egyptian Hieroglyphs and their Gardiner\n# transliteration, with fallback to the Gardiner sign list number\n\n')
G.write(header3)
G.write('# Egyptian-Latin/Gardiner\n\n')
G.write(header4)

S.write(header1)
S.write('# File: Egyptian_Latin_GSL.txt\n')
S.write(header2)
S.write('# Transliteration between Egyptian Hieroglyphs and their Gardiner sign list\n# number\n\n')
S.write(header3)
S.write('# Egyptian-Latin/GSL\n\n')
S.write(header4)


def demdc(ns):
    for i in range(5):
        ns = re.sub(r'A([^0-9]|$)', u'ꜣ'+r'\1', ns)
        ns = re.sub(r'H([^0-9]|$)', u'ḥ'+r'\1', ns)
        ns = re.sub(r'X([^0-9]|$)', u'ẖ'+r'\1', ns)
        ns = re.sub(r'S([^0-9]|$)', u'š'+r'\1', ns)
        ns = re.sub(r'T([^0-9]|$)', u'ṯ'+r'\1', ns)
        ns = re.sub(r'D([^0-9]|$)', u'ḏ'+r'\1', ns)
        ns = re.sub(r'(^|[^0-9])i', r'\1'+u'ı͗', ns)
        ns = re.sub(r'(^|[^0-9])a', r'\1'+u'ꜥ', ns)
        ns = re.sub(r'(^|[^0-9])x', r'\1'+u'ḫ', ns)
        ns = re.sub(r'(^|[^0-9])q', r'\1'+u'ḳ', ns)
    return ns


for l in E:
    l = l.strip('\n ').split('\t');
    
    ch = l[0]
    cp = l[1]
    xl = l[2]

    comm = l[3]

    if ' ' in xl:
        xl = xl.split()
        mdc = ' '.join(xl[0:-1])
        gar = demdc(mdc)
        gsl = xl[-1].replace('J', 'Aa')
    else:
        mdc = xl.replace('J', 'Aa')
        gar = xl.replace('J', 'Aa')
        gsl = xl.replace('J', 'Aa')


    gsl = re.sub(r'\\[rt]?[123]?', '', gsl)
    gsl = re.sub(r'([\\\-])', r'\\\1', gsl)
    gsl = re.sub(r'<h?[0123]', '\\-', gsl)
    gsl = re.sub(r'h?[0123]>', '\\-', gsl)
    gsl = re.sub(r'[\&:\(\)\*]', '\\-', gsl)
    gsl = re.sub(r'(\\\-)+', r'\1', gsl)
    gsl = re.sub(r'\\\-$', '', gsl)
    gsl = re.sub(r'^\\\-', '', gsl)
    gsl = re.sub(r'([0-9]+)([a-z])', lambda m: (m.group(1) + ('\\*' * (ord(m.group(2))-ord('a')+1))), gsl)
    gsl = re.sub(r'([A-Z]+)([0-9]+)', r'\1\\ \2', gsl)
    gsl = re.sub(r'(Aa)([0-9]+)', r'\1\\ \2', gsl)

    gar = re.sub(r'\\[rt]?[123]?', '', gar)
    gar = re.sub(r'([\\\-])', r'\\\1', gar)
    gar = re.sub(r'<h?[0123]', '\\-', gar)
    gar = re.sub(r'h?[0123]>', '\\-', gar)
    gar = re.sub(r'[\&\(\):\*]', '\\-', gar)
    gar = re.sub(r'(\\\-)+', r'\1', gar)
    gar = re.sub(r'\\\-$', '', gar)
    gar = re.sub(r'^\\\-', '', gar)
    gar = re.sub(r'\\\- ', ' ', gar)

    mdc = re.sub(r'([\*\\\-:\)\(\&<>])', r'\\\1', mdc)
    
    
    if gsl:
        S.write(ch+'<>'+gsl+';\n')
    else:
        S.write(ch+'>;\n')

    if ' ' in mdc:
        mdc = mdc.split()
        M.write(ch+'<>'+mdc[0]+';\n')            
        M.write(ch+'<'+mdc[1]+';\n')
    else:
        M.write(ch+'<>'+mdc+';\n')

    if not gar:
        G.write(ch+'>;\n')
    elif ' ' in gar:
        gar = gar.split()
        #print gar
        G.write(ch+'<>'+gar[0]+';\n')
        G.write(ch+'<'+gar[1]+';\n')
    else:
        G.write(ch+'<>'+gar+';\n')

M.write(u'\n:: Null;\n\nAa<J;\nD<j;\nk<c;\n<[eou];\nr<l;\nw<v;\ns<z;\n\n')
M.write(':: ([A-Za-z0-9\ \\\-\:\*<>\&\(\)]);\n')

G.write(u'\n:: Null;\n\nAa<J;\nı͗<i;\nḏ<j;\nr<l;\n<[ou];\nk<q;\nw<v;\nks<x;\n\n')
G.write(u':: ([A-Za-z0-9\ \-ꜣꜥı̣̱̮͗̌]);\n')

S.write('\n:: Null;\n\nAa<J;\n\n')
S.write(':: ([A-Z0-9\ \-\*]);\n')
