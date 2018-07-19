import cmd

class Operator():
    id = ''
    # states: 0 - available | 1 - ringing | 2 - busy
    state = 0

    def __init__(self,id):
        self.id = id

class CallOperator():
    call_id = ''
    op_id = ''

    def __init__(self, call_id, op_id):
        self.call_id = call_id
        self.op_id = op_id

class Telephony(cmd.Cmd):
    calls = []
    operators = [Operator("A"), Operator("B")]
    call_operators = []

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(Command) '

    def do_call(self, call_id):
        if not self.is_command_ok(call_id):
            return
        if not self.is_call_id_available(call_id):
            return
        
        print "Call ", call_id, " received"
        
        self.calls.append(call_id)
        op = self.get_available_operator()

        if op:
            # set operator state to 1 (ringing)
            op.state = 1
            print "Call ", call_id, " ringing at operator ", op.id
            self.call_operators.append(CallOperator(call_id, op.id))
            # remove call form the calls list
            self.calls.remove(call_id)
        else:
            print "Call ", call_id, " waiting in queue"
        
    def do_answer(self, op_id):
        if not self.is_command_ok(op_id):
            return
        
        for call_op in self.call_operators:
            if call_op.op_id == op_id:
                op = self.get_operator(op_id)
                # check if operator state == 1 (ringing). If so, then set it to 2 (busy)
                if op.state == 1:
                    op.state = 2
                    print "Call ", call_op.call_id, "answered by operator ", call_op.op_id
                else:
                    print "Operator ", op_id, " is busy at the moment."


    def do_reject(self, op_id):
        if not self.is_command_ok(op_id):
            return

        for call_op in self.call_operators:
            if call_op.op_id == op_id:
                op = self.get_operator(op_id)
                # set operator state to 0 (available)
                op.state = 0
                print "Call ", call_op.call_id, " rejected by operator ", call_op.op_id
                # remove this current call from call_operators list
                self.call_operators.remove(call_op)
                # transfer the call to the next available operator
                # TODO: instead, create a new function: transfer_to_avialable_op()
                self.do_call(call_op.call_id)
                return
    
    def do_hangup(self, call_id):
        if not self.is_command_ok(call_id):
            return

        for call_op in self.call_operators:
            if call_op.call_id == call_id:
                op = self.get_operator(call_op.op_id)
                # check if operator already answered the call (state == 2 [busy])
                if op.state != 2:
                    print "Call ", call_id, " missed"
                else:
                    print "Call ", call_id, " finished and operator ", call_op.op_id, " available"
                    # set operator state to 0 (available)
                    op.state = 0
                
                # remove this current call from call_operators list
                self.call_operators.remove(call_op)
                return

    # used to exit 'cleanly'
    def do_exit(self, *args):
        return True

    # check if user passed a valid ID
    def is_command_ok(self, id):
        l = id.split()
        if not l:
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
        print "Operator not found!"
        return           

if __name__ == '__main__':
    prompt = Telephony()
    prompt.cmdloop()
