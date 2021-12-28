import math


class Operand:
    def getValue():
        return None

    def __str__(self):
        return str(self.getValue())


class Constant(Operand):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value


class Variable(Operand):
    def __init__(self, name, value):
        self.value = value
        self.name = name

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def __str__(self):
        return str(self.getName())


class Operation:
    prio = None

    def __init__(self):
        self.prio = None
        self.symbol = None
        self.func = False
        self.mulOut = False
        self.nrInput = 0

    def evaluate(self, operands):
        # This function gets a list of the needed operands and outputs the
        # result, if one of the operands is None, this returns None
        for op in operands:
            if op is None:
                return None
        return self.getResult(operands)

    def isFunc(self):
        return self.func

    def getSymbol(self):
        return self.symbol

    def getPriority(self):
        return self.prio

    def getResult(self, operands):
        return None

    def isMultiple(self):
        return self.mulOut

    def getNrInputs(self):
        return self.nrInput

    def __str__(self):
        return self.getSymbol()


class Addition(Operation):
    def __init__(self):
        self.prio = 1
        self.symbol = "+"
        self.func = False
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        return operands[0] + operands[1]


class Difference(Operation):
    def __init__(self):
        self.prio = 1
        self.symbol = "-"
        self.func = False
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        return operands[0] - operands[1]


class Multiplication(Operation):
    def __init__(self):
        self.prio = 2
        self.symbol = "*"
        self.func = False
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        return operands[0] * operands[1]


class Division(Operation):
    def __init__(self):
        self.prio = 2
        self.symbol = "/"
        self.func = False
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        if operands[1] == 0:
            return None
        return operands[0] / operands[1]


class Power(Operation):
    def __init__(self):
        self.prio = 2
        self.symbol = "^"
        self.func = False
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        return operands[0]**operands[1]


class Logarithm(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "log"
        self.func = True
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        # log(x,base)
        if operands[0] <= 0 or operands[0] == 1:
            return None
        return math.log(operands[1], operands[0])


class Min(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "min"
        self.func = True
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        return min(operands)


class Max(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "max"
        self.func = True
        self.mulOut = False
        self.nrInput = 2

    def getResult(self, operands):
        return max(operands)


class Sin(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "sin"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        return math.sin(operands[0])


class Cos(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "cos"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        return math.cos(operands[0])


class Tan(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "tan"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        return math.tan(operands[0])


class ArcSin(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "arcsin"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        if operands[0] > 1 or operands[0] < -1:
            return None
        return math.asin(operands[0])


class ArcCos(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "arccos"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        if operands[0] > 1 or operands[0] < -1:
            return None
        return math.acos(operands[0])


class ArcTan(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "arctan"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        if operands[0] > 1 or operands[0] < -1:
            return None
        return math.atan(operands[0])


class SquareRoot(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "sqrt"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        if operands[0] < 0:
            return None

        # TODO: Implement multiple possible solutions
        # return [math.sqrt(op1), -math.sqrt(op1)]
        return math.sqrt(operands[0])


class Factorial(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "!"
        self.func = False
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        return math.factorial(operands[0])


class AbsoluteValue(Operation):
    def __init__(self):
        self.prio = 3
        self.symbol = "abs"
        self.func = True
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        return abs(operands[0])


class Negation(Operation):
    def __init__(self):
        self.prio = 0  # Why tf it needs priority 0???
        self.symbol = "No symbol"
        self.func = False
        self.mulOut = False
        self.nrInput = 1

    def getResult(self, operands):
        return -operands[0]


# TODO: Add support for 0 operands operations
class Pi(Operation):
    def __init__(self):
        self.prio = 0
        self.symbol = "pi"
        self.func = False
        self.mulOut = False
        self.nrInput = 0

    def getResult(self, operands):
        return math.pi


class OpenBracket(Operation):
    def __init__(self):
        self.prio = 0
        self.func = False
