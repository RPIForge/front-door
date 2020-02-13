from classes.calendar import calendar
from classes.variable import variable

variable_object  = variable()
variable_object.calendar = calendar(variable_object)
variable_object.calendar.number = 2
variable_object.calendar.start()
