import cmd
from myexceptions import NoCallFoundException

class Call():
    # status: 0 - ringing | 1 - answered | 2 - missed | 3 - on_queue | 4 - finished
    def __init__(self, id="", status=0):
        self.id = id
        self.status = status

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
        else:
            # set call status to 3 (on_queue)
            call.status = 3
            print "Call ", call_id, " waiting in queue"

    def do_answer(self, op_id):
        # check if ID is valid
        if not self.is_command_ok(op_id):
            return

        for op in self.operators:
            # search for the given operator and if the state == 1 (ringing)
            if op.id == op_id and op.state == 1:
                op.state = 2

                # TODO: use try/except here (call could not exist)
                # get call and change its status to 1 (answered)
                try:
                    call = self.get_call(op.current_call)
                except NoCallFoundException:
                    return

                call.status = 1

                print "Call ", op.current_call, "answered by operator ", op_id
                return

    def do_reject(self, op_id):
        # check if ID is valid
        if not self.is_command_ok(op_id):
            return

        for op in self.operators:
            if op.id == op_id and op.current_call != "":
                # set operator state to 0 (available)
                op.state = 0
                print "Call ", op.current_call, " rejected by operator ", op_id

                # transfer the call to the next available operator
                op2 = self.get_available_operator()
                current_call = op.current_call
                op.current_call = ""

                # get call and set its status to 0 (ringing)
                call = self.get_call(current_call)

                if op2:
                    self.transfer_call_to_operator(op2, current_call)
                else:
                    # set call status to 3 (on_queue)
                    call.status = 3

                return

    def do_hangup(self, call_id):
        # check if ID is valid
        if not self.is_command_ok(call_id):
            return

        # TODO: use try/except here (call could not exist)
        call = self.get_call(call_id)

        # if the call status is 3 (on_queue), then just
        # set its status to 2 (missed) and print a message
        if call.status == 3:
            call.status = 2
            print "Call ", call_id, " missed"
        else:
            for op in self.operators:
                if op.current_call == call_id:
                    if op.state == 1:
                        print "Call ", call_id, " missed"
                        call.status = 2
                    else:
                        print "Call ", call_id, " finished and operator ", op.id, " available"
                        call.status = 4

                    # set operator state to 0 (available)
                    op.state = 0
                    op.current_call = ""
                    break

        # check if there's any call waiting on queue
        call2 = self.get_call_on_queue()

        if call2:
            # check operator availability
            op2 = self.get_available_operator()
            if op2:
                # transfer call to available operator and set the call status
                # to 0 (ringing)
                self.transfer_call_to_operator(op2, call2.id)
                call2.status = 0

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
        raise NoCallFoundException

    # TODO: create a new function, to get the first call on the queue
    def get_call_on_queue(self):
        for call in self.calls:
            if call.status == 3:
                return call

if __name__ == '__main__':
    prompt = Telephony()
    prompt.start()
    prompt.cmdloop()
