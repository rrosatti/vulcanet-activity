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
        # check if ID is valid
        if not self.is_command_ok(call_id):
            return
        if not self.is_call_id_available(call_id):
            return
      
        print "Call ", call_id, " received"
       
        # add call ID to the calls list 
        self.calls.append(call_id)
        op = self.get_available_operator()
        
        # if there's an avialable operator, then assign this call to him
        if op:
            self.transfer_call_to_operator(op, call_id)
            # remove call form the calls list
            self.calls.remove(call_id)
        else:
            print "Call ", call_id, " waiting in queue"
        
    def do_answer(self, op_id):
        # check if ID is valid
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
        # check if ID is valid
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
                op2 = self.get_available_operator()
                if op2:
                    self.transfer_call_to_operator(op2, call_op.call_id)
                    # if the call is in the calls list, then just remove it
                    if call_op.call_id in self.calls:
                        self.calls.remove(call_op.call_id)

                return
    
    def do_hangup(self, call_id):
        # check if ID is valid
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
                # check if there is a call waiting in the queue. If so, then transfer that call 
                # to an available operator
                if self.calls:
                    # check operator availability
                    op2 = self.get_available_operator()
                    if op2:
                        self.transfer_call_to_operator(op2, self.calls[0])
                        # remove the call from the calls list
                        self.calls.remove(self.calls[0]) 
                return
        
        # if call is not in the call_operators list, then it was just missed
        print "Call ", call_id, " missed"
        self.calls.remove(call_id)

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
        print "Call ", call_id, " ringing at operator ", op.id
        self.call_operators.append(CallOperator(call_id, op.id))

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
