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

    def do_call(self, id):
        if not self.is_command_ok(id):
            return
        if not self.is_call_id_available(id):
            return
        
        print "Call ", id, " received"
        
        self.calls.append(id)
        op = self.get_available_operator()

        if op:
            op.state = 1
            print "Call ", id, " ringing at operator ", op.id
            self.call_operators.append(CallOperator(id, op.id))
        
    def do_answer(self, id):
        if not self.is_command_ok(id):
            return
        
        for call_op in self.call_operators:
            if call_op.op_id == id:
                op = self.get_operator(id)
                # check if operator state == 1 (ringing). If so, then set it to 2 (busy)
                if op.state == 1:
                    op.state = 2
                    print "Call ", call_op.call_id, "answered by operator ", call_op.op_id
                else:
                    print "Operator ", id, " is busy at the moment."


    def do_reject(self, id):
        if not self.is_command_ok(id):
            return
    
    def do_hangup(self, id):
        if not self.is_command_ok(id):
            return

    # just to exit 'cleanly'
    def do_exit(self, *args):
        return True

    def is_command_ok(self, id):
        l = id.split()
        if not l:
            print "You must inform the ID!"
            return 0
        if len(l)!=1:
            print "Only one ID is allowed at a time!"
            return 0
        return 1

    def is_call_id_available(self, id):
        if id in self.calls:
            print "Call ", id, " already in queue"
            return 0
        return 1

    def get_available_operator(self):
        for op in self.operators:
            if op.state == 0:
                return op
    
    def get_operator(self, id):
        for op in self.operators:
            if op.id == id:
                return op
        print "Operator not found!"
        return           

if __name__ == '__main__':
    prompt = Telephony()
    prompt.cmdloop()
