# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

parameters_validate_sieve_size = [(None, None),
                                  (0, None),
                                  (1, 1),
                                  (10, 10)]

parameters_validate_sieve_size_exception = [-1, 11]

parameters_validate_simplify = [(None, False),
                                (True, True),
                                (False, False)]

parameters_Postprocessing = [([None, None], [None, False]),
                             ([0, True], [None, True]),
                             ([1, False], [1, False]),
                             ([10, None], [10, False])]
