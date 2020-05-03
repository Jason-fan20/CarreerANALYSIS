# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 20:09:35 2020

@author: ASUS
"""
import del_bracket
import generate_frequence_file
import parse_newversion
import parse

# =============================================================================
# generate frequence_file by ins.txt
# =============================================================================
#generate_frequence_file.main()

# =============================================================================
# Delete the bracket in out_ori.txt, output is out_del_brackets.txt
#Excpet for this, out_ori.txt will be divided into 200 different files in ./file
# =============================================================================
del_bracket.main()
#parse_newversion.

# =============================================================================
# Parse the OC(occupation) in out_del_brackets.txt,output is total.txt
# =============================================================================
#parse_newversion.main()


# =============================================================================
# Parse the OC(occupation) in out_del_brackets.txt,output is total.txt
# The difference between new_version and this is, new_version won't delete any information
# in original txt, but this will delete some position information, even by wrong way
# =============================================================================
parse.main()

# =============================================================================
# OCtree build&&Compress
# =============================================================================
#import OCtree
#tree=OCtree.build_tree()
#tree=OCtree.compress_tree(tree)
#OCtree.visualization(tree)
import OCtree
OCtree.build_tree()
OCtree.compress_tree()
#OCtree.visualization()
OCtree.print_all_node()

#tree.

