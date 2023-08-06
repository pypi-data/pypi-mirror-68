import abc
import re


class AbstractExpression(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def interpret(self):
        pass


class NonTerminalExpression(AbstractExpression):

    def __init__(self, expression):
        self._expression = expression

    def interpret(self):
        self._expression.interpret()


class TerminalExpression(AbstractExpression):

    def __init__(self,expression):
        self.__expression = expression

    def interpret(self):
        return self.__expression


class GreaterThanExpression(AbstractExpression):

    def __init__(self, left_expression, right_expression):
        self.__left_expression = left_expression
        self.__right_expression = right_expression

    def interpret(self):
        return self.__left_expression.interpret() > self.__right_expression.interpret()


class GreaterOrEqualExpression(AbstractExpression):

    def __init__(self, left_expression, right_expression):
        self.__left_expression = left_expression
        self.__right_expression = right_expression

    def interpret(self):
        return self.__left_expression.interpret() >= self.__right_expression.interpret()


class LessThanExpression(AbstractExpression):

    def __init__(self, left_expression, right_expression):
        self.__left_expression = left_expression
        self.__right_expression = right_expression

    def interpret(self):
        return self.__left_expression.interpret() < self.__right_expression.interpret()


class LessOrEqualExpression(AbstractExpression):

    def __init__(self, left_expression, right_expression):
        self.__left_expression = left_expression
        self.__right_expression = right_expression

    def interpret(self):
        return self.__left_expression.interpret() <= self.__right_expression.interpret()


class LikeExpression(AbstractExpression):

    def __init__(self, left_expression, right_expression):
        self.__left_expression = left_expression
        self.__right_expression = right_expression

    def interpret(self):
        right_expression = self.__right_expression.interpret()
        right_expression = right_expression.replace('.', '\\.').replace('*', '.*').replace('?', '.')

        return bool(re.match(right_expression, self.__left_expression.interpret()))
