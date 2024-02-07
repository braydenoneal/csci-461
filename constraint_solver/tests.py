from tester import make_test, get_tests

#from mat_vec_ops import *
#from classify import *

import operator
import math

# CSP tests

import csp
from moose_csp import moose_csp_problem

EXPECTED_FC_MOOSE_TREE = """ROOT
	1=Mc(c,1)
		2=Y(c,2)
			3=M(c,3)
				4=O(c,4)
					5=B(f,5)
				4=B(c,6)
					5=O(f,7)
			3=O(c,8)
				4=M(f,9)
				4=B(c,10)
					5=M(f,11)
			3=B(c,12)
				4=M(f,13)
				4=O(c,14)
					5=M(f,15)
		2=M(c,16)
			3=Y(c,17)
				4=O(c,18)
					5=B(f,19)
				4=B(c,20)
					5=O(f,21)
			3=O(c,22)
				4=Y(f,23)
				4=B(c,24)
					5=Y(c,25)
						6=P(*,26)
			3=B(u,-)
		2=P(u,-)
"""

EXPECTED_FCPS_MOOSE_TREE = """ROOT
	1=Mc(c,1)
		2=Y(c,2)
			3=M(f,3)
			3=O(f,4)
			3=B(f,5)
		2=M(c,6)
			3=Y(f,7)
			3=O(c,8)
				4=B(c,9)
					5=Y(c,10)
						6=P(*,11)
			3=B(u,-)
		2=P(u,-)
"""

def csp_test_1_getargs():
    return [ "moose_csp_problem", "forward_checking" ]

def csp_test_1_testanswer(val, original_val = None):
    return ( val == EXPECTED_FC_MOOSE_TREE )

make_test(type = 'FUNCTION',
          getargs = csp_test_1_getargs,
          testanswer = csp_test_1_testanswer,
          expected_val = EXPECTED_FC_MOOSE_TREE,
          name = 'csp_solver_tree'
          )

def csp_test_2_getargs():
    return [ "moose_csp_problem", "forward_checking_prop_singleton" ]

def csp_test_2_testanswer(val, original_val = None):
    return ( val == EXPECTED_FCPS_MOOSE_TREE )

make_test(type = 'FUNCTION',
          getargs = csp_test_2_getargs,
          testanswer = csp_test_2_testanswer,
          expected_val = EXPECTED_FCPS_MOOSE_TREE,
          name = 'csp_solver_tree'
          )

