import cmd

class Operator():
    id = ''
    # states: 0 - available | 1 - busy | 2 - ringing
    state = 0

    def __init__(self,id):
        self.id = id
    
    def check_if_available(self):
        return True if state == 0 else False
    

class Telephony(cmd.Cmd):
    calls = []
    operators = [Operator("A"), Operator("B")]

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(Command) '

    def do_call(self, id):
        if not self.is_command_ok(id):
            return
        
        print "Call ", id, " received"
        
        self.calls.append(id)
        op = self.get_available_operator(self)

        if op:
            op.state = 2
            print "Call ", id, " ringing at operator ", op.id
        
    def do_answer(self, id):
        if not self.is_command_ok(id):
            return

    def do_reject(self, id):
        if not self.is_command_ok(id):
            return
    
    def do_hangup(self, id):
        if not self.is_command_ok(id):
            return

    def is_command_ok(self, id):
        l = id.split()
        if not l:
            print "You must inform the ID!"
            return 0
        if len(l)!=1:
            print "Only one ID is allowed at a time!"
            return 0
        return 1

    def get_available_operator(self):
        return 0 

if __name__ == '__main__':
    prompt = Telephony()
    prompt.cmdloop()
