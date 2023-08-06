from unittest import TestCase

from core.pipelining.expression import TerminalExpression, GreaterThanExpression, LessThanExpression, \
    GreaterOrEqualExpression, LessOrEqualExpression, LikeExpression


class ExpressionTest(TestCase):

    def test_should_execute_without_exception(self):
        expression_100 = TerminalExpression(100)
        expression_200 = TerminalExpression(200)

        expression_filename = TerminalExpression('image_152.jpeg')
        expression_extension = TerminalExpression('*.jpeg')
        expression_joker = TerminalExpression('image_15?.jpeg')

        self.assertTrue(GreaterThanExpression(expression_200, expression_100).interpret())
        self.assertFalse(GreaterThanExpression(expression_100, expression_200).interpret())
        self.assertFalse(GreaterThanExpression(expression_100, expression_100).interpret())

        self.assertTrue(GreaterOrEqualExpression(expression_200, expression_100).interpret())
        self.assertFalse(GreaterOrEqualExpression(expression_100, expression_200).interpret())
        self.assertTrue(GreaterOrEqualExpression(expression_100, expression_100).interpret())

        self.assertTrue(LessThanExpression(expression_100, expression_200).interpret())
        self.assertFalse(LessThanExpression(expression_200, expression_100).interpret())
        self.assertFalse(LessThanExpression(expression_100, expression_100).interpret())

        self.assertTrue(LessOrEqualExpression(expression_100, expression_200).interpret())
        self.assertFalse(LessOrEqualExpression(expression_200, expression_100).interpret())
        self.assertTrue(LessOrEqualExpression(expression_100, expression_100).interpret())

        self.assertTrue(LikeExpression(expression_filename, expression_extension).interpret())
        self.assertTrue(LikeExpression(expression_filename, expression_joker).interpret())