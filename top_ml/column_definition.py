# define a dctionary for keeping track of what is where
global column_no_to_name

# get_column_name = {0:   'label',
#                    1:   'jet mass',
#                    2:   'jet pt',
#                    3:   'jet eta',
#                    4:   'jet phi',
#                    5:   'Tau32_wta',
#                    6:   'Split23',
#                    7:   'Dip12',
#                    8:   'Qw',
#                    9:   'D2',
#                    10:  'b pt',
#                    11:  'b eta',
#                    12:  'b phi',
#                    13:  'W_1 pt',
#                    14:  'W_1 eta',
#                    15:  'W_1 phi',
#                    16:  'W_2 pt',
#                    17:  'W_2 eta',
#                    18:  'W_2 phi',
#                    19:  'constit start pt'}


get_column_name = {0: 'weight',
                   1: 'label',
                   2:  'jet mass',
                   3:  'jet pt',
                   4:  'jet eta',
                   5:  'jet phi',
                   6:  'Tau32_wta',
                   7:  'Split23',
                   8:  'Dip12',
                   9:  'Qw',
                   10: 'D2',
                   11:  'b pt',
                   12:  'b eta',
                   13:  'b phi',
                   14:  'W_1 pt',
                   15:  'W_1 eta',
                   16:  'W_1 phi',
                   17:  'W_2 pt',
                   18:  'W_2 eta',
                   19:  'W_2 phi',
                   20:  'constit start pt'}

get_column_no = dict((reversed(item) for item in get_column_name.items()))
