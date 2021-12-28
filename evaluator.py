'''

@author: Ailincai Ionut

This module provides the class Evaluator that gets an expression in the form of
 a string and evaluates it
'''

import ops


class Evaluator:
    def __init__(self):
        self.__string_expression = ""
        self.__obj_expression = []
        self.__declared_operations = {
            "+": ops.Addition,
            "-": ops.Difference,
            "*": ops.Multiplication,
            "/": ops.Division,
            "^": ops.Power,
            "(": ops.OpenBracket,
            "!": ops.Factorial,
            "pi": ops.Pi,
            "abs": ops.AbsoluteValue,
            "log": ops.Logarithm,
            "min": ops.Min,
            "max": ops.Max,
            "sin": ops.Sin,
            "cos": ops.Cos,
            "tan": ops.Tan,
            "arcsin": ops.ArcSin,
            "arccos": ops.ArcCos,
            "arctan": ops.ArcTan,
            "sqrt": ops.SquareRoot
        }
        self.__variables = []

    def __isExpressionCorrect(self):
        nr_open = 0
        nr_closed = 0
        for chr in self.__string_expression:
            if chr == "(":
                nr_open += 1
            if chr == ")":
                nr_closed += 1
        if nr_open != nr_closed:
            return False
        return True

    def setExpression(self, expression):
        '''
        Sets the expression to the given expression
        If the expression is syntactically incorrect raises an error
        '''
        previous_string = self.__string_expression
        previous_obj = self.__obj_expression
        if self.__isExpressionCorrect():
            try:
                self.__string_expression = expression
                self.__translate()
                self.evaluateWithSetValues()
            except:
                self.__string_expression = previous_string
                self.__obj_expression = previous_obj
                raise ValueError(
                    "The expression given is syntactically incorrect!")
        else:
            raise ValueError(
                "The expression given is syntactically incorrect!")

    def getVariables(self):
        return self.__variables

    def getNrOfVariables(self):
        return len(self.__variables)

    def getObj(self):
        # TODO: Remove this, it's for debugging
        return self.__obj_expression

    def getExpression(self):
        return self.__string_expression

    def __getOperation(self, operation):
        # Returns the operation class from the literal form
        return self.__declared_operations[operation]

    def __translate(self):
        # This function gets an expression in the form of a string and
        # converts it into a list of operands and operations in the posfix notation
        # Ex.: 1+1 = 11+ in postfix

        opstack = []  # the operation stack
        self.__obj_expression = []
        # We go through every character
        i = 0
        while i < len(self.__string_expression):
            print(self.__obj_expression)
            if self.__string_expression[i] == "(":
                opstack.append(
                    self.__getOperation(self.__string_expression[i])())
            elif self.__string_expression[i] in self.__declared_operations:
                # if its and operation we pop and add to the output the operations on the opstack
                # that have a lower or equal priority
                # Priority ex: +<*<log
                if self.__string_expression[
                        i] == "-" and self.__string_expression[i - 1] == "(":
                    opstack.append(ops.Negation())
                else:
                    operation = self.__getOperation(
                        self.__string_expression[i])
                    while len(opstack) > 0 and operation().getPriority(
                    ) <= opstack[-1].getPriority():
                        if not isinstance(opstack[-1], ops.OpenBracket):
                            self.__obj_expression.append(opstack.pop())
                        else:
                            opstack.pop()
                            # and we add it to the opstack
                    opstack.append(operation())
            elif self.__string_expression[i] == ")":
                while not isinstance(opstack[-1], ops.OpenBracket):
                    self.__obj_expression.append(opstack.pop())
                opstack.pop()
                if len(opstack) > 0 and opstack[-1].isFunc():
                    self.__obj_expression.append(opstack.pop())

            elif self.__string_expression[
                    i] != " " and self.__string_expression[i] != ",":
                # Here we check for numerical constants, variables or multiple characters
                # operations
                to = i
                if self.__string_expression[i].isalpha():
                    # Variables and multiple characters operations
                    while to < len(
                            self.__string_expression
                    ) - 1 and self.__string_expression[to + 1].isalpha(
                    ) and self.__string_expression[to + 1] != "(":
                        to += 1
                    if self.__string_expression[
                            i:to + 1] in self.__declared_operations:
                        # if it's a multiple characters operation we did the
                        # same trick as for normal operations
                        operation = self.__getOperation(
                            self.__string_expression[i:to + 1])
                        while len(opstack) > 0 and operation().getPriority(
                        ) <= opstack[-1].getPriority():
                            if not isinstance(opstack[-1], ops.OpenBracket):
                                self.__obj_expression.append(opstack.pop())
                            else:
                                opstack.pop()
                        opstack.append(operation())
                    else:
                        # Here we get a variable
                        if not self.__string_expression[i:to +
                                                        1] in self.__variables:
                            self.__variables.append(
                                self.__string_expression[i:to + 1])
                        self.__obj_expression.append(
                            ops.Variable(self.__string_expression[i:to + 1],
                                         0))

                elif self.__string_expression[i].isnumeric():
                    # Numerical constants
                    while to < len(self.__string_expression) - 1 and (
                            self.__string_expression[to + 1].isnumeric()
                            or self.__string_expression[to + 1] == "."):
                        to += 1
                    self.__obj_expression.append(
                        ops.Constant(float(self.__string_expression[i:to +
                                                                    1])))
                i = to
            i += 1
        if len(opstack) > 0:
            # if we still have some operation on the stack we put them in the output
            while len(opstack) > 0:
                self.__obj_expression.append(opstack.pop())

    def evaluateWithSetValues(self):
        '''
        This function evaluates the expression with the already set
        values for the variables
        You can set the values of the function with setValueOfVariable()
        '''
        value = 0
        stack = []
        for el in self.__obj_expression:
            if isinstance(el, ops.Operand):
                stack.append(el.getValue())
            elif isinstance(el, ops.Operation):
                operands = []
                for i in range(el.getNrInputs()):
                    operands.append(stack.pop())
                operands.reverse()
                # print("Operation:", str(el))
                # print("Operands:", operands)
                # print("Stack:", stack)
                # print()
                if not el.isMultiple():
                    value = el.evaluate(operands)
                    stack.append(value)
        if len(stack) > 1:
            raise ValueError(
                "The expression has too many operands for its operations")
        return stack.pop()

    def __set_value_of_variable(self, variable, value):
        for e in self.__obj_expression:
            if isinstance(e, ops.Variable):
                if e.getName() == variable:
                    e.setValue(value)

    def setValueOfVariable(self, variable, value):
        '''
        Sets the value of the given variable to the value
        Input:
            -variable - a string with the name of the variable
            -value - a number
        Raises a ValueError if the given variable doesn't exist in the expression
        '''
        if not isinstance(value, float):
            raise ValueError("The value must be a float!")
        if not (isinstance(variable, str) and variable in self.__variables):
            raise ValueError("The variable is not found in the expression!")
        self.__set_value_of_variable(variable, value)

    def evaluate(self, values):
        '''
         This function evaluates the given expression and returns the value
         It will return None if there is an invalid operation
         Input: values - a list of values for each variable in the expression
         ordered by the apparition in the expression
         Output: a numerical value that coresponds to the expression or
         None if the expression has an invalid operation
         Raises a ValueError if there are not enough values in the list
        '''
        if len(values) == len(self.__variables):
            for i in range(len(values)):
                self.__set_value_of_variable(self.__variables[i], values[i])
            return self.evaluateWithSetValues()
        else:
            if len(values) < len(self.__variables):
                raise ValueError(
                    "There aren't enough values for all the variables")
            else:
                raise ValueError(
                    "There are too many values for all the variables")
