"""Performer is an base class for pluggable function calls"""
import re
import types
import inspect
from time import time as tm


class Performer(object):
    """Implements common direct and dynamic interface for accessing functions"""
    def __init__(self):
        self.perform_re = re.compile('^perform_(.*?)$')
        self.funcs = []
        self.load()
        self.perform = self.perform_action

    def perform_action(self, action, action_args):
        name = "perform_%s" % (action)
        # prevent recursive loop
        if name == "perform_action":
            return
        func = None
        try:
            func = getattr(self, name)
        except AttributeError:
            print("Action does not exist: %s" % action)
            self.supported_actions()
        if isinstance(func, types.MethodType):
            t1 = tm()
            return_value = func(action_args)
            t2 = tm()
            d = t2 - t1
            return ActionResponse(action=action, result=return_value, call_time=d)

    def load(self):
        """Evaluate class for perform functions"""
        perform_functions = []
        inspected_methods = inspect.getmembers(self, predicate=inspect.ismethod)
        inspected_methods += inspect.getmembers(self, predicate=inspect.isfunction)
        for i in inspected_methods:
            v = i[0]
            match = self.perform_re.match(v)
            if match and match.group(1) != 'action':
                perform_functions.append(match.group(1))
        perform_functions.sort()
        self.funcs = perform_functions

    @classmethod
    def register(cls, func):
        """Register a new performer function with the instance"""
        if _validate_signature(func) is True:
            setattr(cls, func.__name__, func)

    def supported_actions(self):
        """Print out supported actions"""
        for action in self.funcs:
            print(action)


def _validate_signature(func):
    """Ensures any perform function has the correct signature"""
    def s(self, action_args):
        pass
    valid_spec = inspect.getfullargspec(s)
    func_spec = inspect.getfullargspec(func)
    if valid_spec.args != func_spec.args:
        raise ValueError("Must provide valid signature on func that is being registered: %s" % (valid_spec.args))
    return True


class ActionResponse(object):
    """Response returned by perform action used to store additional meta for call"""
    __slots__ = ['action', 'result', 'call_time']

    def __init__(self, action, result, call_time=None):
        self.action = action
        self.result = result
        self.call_time = call_time
