from parametric import Attribute, parametrize

@parametrize
class MyExperiment:
    x = Attribute('x', 0, converter=int)

def test_attribute_creation():
    exp = MyExperiment(x=3)
    assert exp.x == 3

def test_conversion():
    exp = MyExperiment(x=1.1)
    assert exp.x == 1 and isinstance(exp.x(), int)


def test_parameter_dict():
    exp = MyExperiment(x=0)
    assert exp.__parameters__['x'] == exp.x

def test_instance_isolation():
    exp1 = MyExperiment()
    exp2 = MyExperiment()

    exp1.x(1)
    exp2.x(2)

    assert exp1.x == 1
    assert exp2.x == 2
