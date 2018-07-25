class NoOperatorAvailableException(Exception):
    message = "Unfortunatelly there are no Operators Available, please call again later"
    def __init__(self, msg=message):
        self.msg = msg

class NoOperatorFoundException(Exception):
    message = "Operator not found!"
    def __init__(self, msg=message):
        self.msg = msg

class NoCallFoundException(Exception):
    message = "Call not found!"
    def __init__(self, msg=message):
        self.msg = msg
