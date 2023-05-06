from Services.Exception.ValidationException import ValidationException
import json
import inspect

class Entity:

    def dataAnnotation(self, value, typing):
        # Gets column name
        frame = inspect.currentframe()
        var_name = inspect.getframeinfo(frame.f_back).code_context[0].split('=')[0].strip()
        # Throws an err if type doesn't met
        if not isinstance(value, typing):
            raise ValidationException(f"Expected {typing.__name__}, got {type(value).__name__} ({var_name})")
        return value

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)