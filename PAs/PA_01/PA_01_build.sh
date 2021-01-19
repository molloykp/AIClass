## Build PA01

# 
# copy over decision_tree_tests.py and strip decorators
# from code
grep -v @points_decor instructor/autolab/mldt/officialtests/decision_tree_tests.py | grep -v 'from unittest_utils' > www/decision_tree_tests.py
