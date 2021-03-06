# parametric 
[![Build Status](https://travis-ci.org/lab-api/parametric.svg?branch=master)](https://travis-ci.org/lab-api/parametric)
[![Test Coverage](https://api.codeclimate.com/v1/badges/053063816035990cb794/test_coverage)](https://codeclimate.com/github/lab-api/parametric/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/053063816035990cb794/maintainability)](https://codeclimate.com/github/lab-api/parametric/maintainability)

Parametric provides a device-control framework for the other libraries in LabAPI, offering a standardized syntax for connecting to and communicating with experiments. Similar frameworks exist, notably [QCoDeS](https://github.com/QCoDeS/Qcodes), and the syntax here has been designed to allow compatibility.

A physical quantity or a knob on a device is represented by a Parameter:

```python
from parametric import Parameter
x = Parameter('x')
```

The parameter can be called to get or set its state:
```python
x(3)
print(x())
>>> 3
```

By default, the state is represented only internally. You can pass functions to the ``get_cmd`` and ``set_cmd`` arguments of the Parameter constructor to connect the class to your device drivers:

```python
y = Parameter('y', get_cmd=measure_voltage, set_cmd=set_voltage)
```

The Parameter class supports mathematical operations transparently:

```python
voltage = Parameter('voltage', 1)
resistance = 50
power = voltage**2/resistance
print(power)

>> 0.02
```

Parametric can also be used in conjunction with the Optimistic library to effortlessly optimize multiparameter experiments or simulations.
