# import unittest

# from myutils_ethank5149.math import linspace

# # FIXME
# # TODO: Create tests
# class MyTestCase(unittest.TestCase):
#     # Bisection Method
#     ###########################################################################
#     def test_bisection_sqrt9(self):                                           #
#         ans = linspace(lambda x: x ** 2 - 9, 1.0, 5.0)                        #
#         self.assertEqual(round(ans, 8), 3.00000000)                           #

#     def test_bisection_sin(self):                                             #
#         ans = bisection(lambda x: sin(x), 2.0, 4.0)                           #
#         self.assertEqual(round(ans, 8), 3.14159265)                           #

#     def test_bisection_erf_x_squared_minus_1(self):                           #
#         ans = bisection(lambda x: erf(x**2-1), 0.0001, 5.0)                   #
#         self.assertEqual(round(ans, 8), 1.00000000)                           #
#     ###########################################################################

#     # Secant Method
#     ###########################################################################
#     def test_secant_sqrt9(self):                                              #
#         ans = secant(lambda x: x ** 2 - 9, 1.0, 5.0)                          #
#         self.assertEqual(round(ans, 8), 3.00000000)                           #

#     def test_secant_sin(self):                                                #
#         ans = secant(lambda x: sin(x), 2.0, 4.0)                              #
#         self.assertEqual(round(ans, 8), 3.14159265)                           #

#     def test_secant_erf_x_squared_minus_1(self):                              #
#         ans = secant(lambda x: erf(x**2-1), 0.0001, 5.0)                      #
#         self.assertEqual(round(ans, 8), 1.00000000)                           #
#     ###########################################################################

#     # Ridder's Method
#     ###########################################################################
#     def test_ridder_sqrt9(self):                                              #
#         ans = ridder(lambda x: x ** 2 - 9, 1.0, 5.0)                          #
#         self.assertEqual(round(ans, 8), 3.00000000)                           #

#     def test_ridder_sin(self):                                                #
#         ans = ridder(lambda x: sin(x), 2.0, 4.0)                              #
#         self.assertEqual(round(ans, 8), 3.14159265)                           #

#     def test_ridder_erf_x_squared_minus_1(self):                              #
#         ans = ridder(lambda x: erf(x**2-1), 0.0001, 5.0)                      #
#         self.assertEqual(round(ans, 8), 1.00000000)                           #
#     ###########################################################################

#     # False Position Method
#     ###########################################################################
#     def test_falsepos_sqrt9(self):                                            #
#         ans = falsepos(lambda x: x ** 2 - 9, 1.0, 5.0)                        #
#         self.assertEqual(round(ans, 8), 3.00000000)                           #

#     def test_falsepos_sin(self):                                              #
#         ans = falsepos(lambda x: sin(x), 2.0, 4.0)                            #
#         self.assertEqual(round(ans, 8), 3.14159265)                           #

#     def test_falsepos_erf_x_squared_minus_1(self):                            #
#         ans = falsepos(lambda x: erf(x**2-1), 0.0001, 5.0)                    #
#         self.assertEqual(round(ans, 8), 1.00000000)                           #
#     ###########################################################################

#     # Brent's Method
#     ###########################################################################
#     def test_brent_sqrt9(self):                                               #
#         ans = brent(lambda x: x ** 2 - 9, 1.0, 5.0)                           #
#         self.assertEqual(round(ans, 8), 3.00000000)                           #

#     def test_brent_sin(self):                                                 #
#         ans = brent(lambda x: sin(x), 2.0, 4.0)                               #
#         self.assertEqual(round(ans, 8), 3.14159265)                           #

#     def test_brent_erf_x_squared_minus_1(self):                               #
#         ans = brent(lambda x: erf(x**2-1), 0.0001, 5.0)                       #
#         self.assertEqual(round(ans, 8), 1.00000000)                           #
#     ###########################################################################

# if __name__ == '__main__':
#     unittest.main()

# import unittest
# from math import sin, erf, log


# class MyTestCase(unittest.TestCase):


# if __name__ == '__main__':
#     unittest.main()

