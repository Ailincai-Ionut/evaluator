from evaluator import Evaluator

ev = Evaluator()

ev.setExpression("sin(pi)")
print(ev.getExpression())
print(ev.getObj())
print(ev.evaluateWithSetValues())
#2*(3+4)-1 -> 234+*1-
