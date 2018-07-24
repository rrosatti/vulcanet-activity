import cmd

class Call():
    def __init__(self, id=""):
        self.id = id

class Operator():

    # states: 0 - available | 1 - ringing | 2 - busy
    def __init__(self,id="", state=0, current_call=""):
        self.id = id
        self.state = state
        self.current_call = current_call

class Telephony(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(Command) '
        self.operators = []
        self.calls = []

    def start(self):
        self.operators.append(Operator("A"))
        self.operators.append(Operator("B"))

    def do_call(self, call_id):
        # check if ID is valid
        if not self.is_command_ok(call_id):
            return
        if not self.is_call_id_available(call_id):
            return

        print "Call ", call_id, " received"

        call = Call(call_id)
        # add call ID to the calls list
        self.calls.append(call)
        op = self.get_available_operator()

        # if there's an avialable operator, then assign this call to him
        if op:
            self.transfer_call_to_operator(op, call_id)
            # remove call form the calls list
            self.calls.remove(call)
        else:
            print "Call ", call_id, " waiting in queue"

    def do_answer(self, op_id):
        # check if ID is valid
        if not self.is_command_ok(op_id):
            return

        for op in self.operators:
            if op.id == op_id:
                # check if operator state == 1 (ringing). If so, then set it to 2 (busy)
                if op.state == 1:
                    op.state = 2
                    call = self.get_call(op.current_call)
                    print "Call ", op.current_call, "answered by operator ", op_id
                else:
                    print "Operator ", op_id, " is busy at the moment."

    def do_reject(self, op_id):
        # check if ID is valid
        if not self.is_command_ok(op_id):
            return

        for op in self.operators:
            if op.id == op_id:
                # set operator state to 0 (available)
                op.state = 0
                print "Call ", op.current_call, " rejected by operator ", op_id
                # transfer the call to the next available operator
                op2 = self.get_available_operator()
                call = self.get_call(op.current_call)
                current_call = op.current_call
                op.current_call = ""
                if op2:
                    self.transfer_call_to_operator(op2, current_call)
                    # if the call is in the calls list, then just remove it
                    call = self.get_call(current_call)
                    if call:
                        self.calls.remove(call)
                return

    def do_hangup(self, call_id):
        # check if ID is valid
        if not self.is_command_ok(call_id):
            return

        call = self.get_call(call_id)

        for op in self.operators:
            if op.current_call == call_id:
                # check if operator already answered the call (state == 2 [busy])
                if op.state != 2:
                    print "Call ", call_id, " missed"
                else:
                    print "Call ", call_id, " finished and operator ", op.id, " available"

                # set operator state to 0 (available)
                op.state = 0
                op.current_call = ""

                # check if there is a call waiting in the queue. If so, then transfer that call
                # to an available operator
                if self.calls:
                    # check operator availability
                    op2 = self.get_available_operator()
                    if op2:
                        self.transfer_call_to_operator(op2, self.calls[0].id)
                        # remove the call from the calls list
                        self.calls.remove(self.calls[0])
                return

        if call:
            # if call is not assigned to an operator yet, then it was just missed
            print "Call ", call_id, " missed"
            self.calls.remove(call)

    # used to exit 'cleanly'
    def do_exit(self, *args):
        return True

    # check if user passed a valid ID
    def is_command_ok(self, id):
        l = id.split()
        if not l:
            # printk("You must inform the ID!"); <--- damn, kernel debugging  hahaha
            print "You must inform the ID!"
            return 0
        if len(l)!=1:
            print "Only one ID is allowed at a time!"
            return 0
        return 1

    # check if the given call ID is already in the queue
    def is_call_id_available(self, id):
        if id in self.calls:
            print "Call ", id, " already in queue"
            return 0
        return 1

    # transfer the call to the given operator
    def transfer_call_to_operator(self, op, call_id):
        # set operator state to 1 (ringing)
        op.state = 1
        op.current_call = call_id
        print "Call ", call_id, " ringing at operator ", op.id

    # get the first available operator
    def get_available_operator(self):
        for op in self.operators:
            if op.state == 0:
                return op

    # get the operator corresponding to the given ID
    def get_operator(self, id):
        for op in self.operators:
            if op.id == id:
                return op
        return

    # get the call corresponding to the given ID
    def get_call(self, id):
        for call in self.calls:
            if call.id == id:
                return call
        return

if __name__ == '__main__':
    prompt = Telephony()
    prompt.start()
    prompt.cmdloop()
