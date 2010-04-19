import cmd
import wl
try:
    import readline
except:
    pass

NEED_CONNECTED_NM = 1 << 0
NEED_CONNECTED_AS = 1 << 1
NEED_CREDENTIALS  = 1 << 2
NEED_NODE         = 1 << 3
NEED_NM           = 1 << 4

def _nm():
    return wl.nm()

class WebHi(cmd.Cmd):
    intro = """
Welcome to the WebHi administration console.
Type 'help' for a list of commands, or a blank line to exit.
"""
    prompt = "webhi> "
    
    requisites = 0
    if _nm(): requisites |= NEED_NM
    
    def do_enroll(self, args):
        print "Enroll called"

    def do_nm_start(self, args):
        print "Starting Node Manager..."
        wl.startNodeManager()
        self.requisites |= NEED_NM

    def do_credentials(self, args):
        argslist = args.split()
        if len(argslist) == 0:
            print "credentials: using defaults weblogic:we8logic"
            self.username = 'weblogic'
            self.password = 'we8logic'
        else:
            print "Setting credentials: " + args
            (self.username, self.password) = args.split()
        self.requisites |= NEED_CREDENTIALS

    def do_node(self, args):
        argslist = args.split()
        if len(argslist) < 1:
            print "node: expected at least one argument"
            return
        self.__set_node(*argslist)
        self.requisites |= NEED_NODE

    def __set_node(self, domain, host='localhost', port='5556'):
        print "node: setting " + domain + "@" + host + ":" + port
        self.domain = domain
        self.host = host
        self.port = port
        
        
    def do_admin_connect(self, args):
        if self.requisites & NEED_CREDENTIALS:
            print "Connecting to: " + args
            wl.connect(self.username, self.password, args)
            self.requisites |= NEED_CONNECTED_AS
        else:
            print "Set credentials first with 'credentials username password'"

    def do_nm_connect(self, _):
        if self.__satisfies_credentials_and_node():
            print "Connecting to Node Manager on: " + self.domain + "@" + self.host
            wl.nmConnect(self.username, self.password,
                         self.host, self.port,
                         self.domain, nmType='plain')
            self.requisites |= NEED_CONNECTED_NM

    def do_admin_start(self, args):
        if not wl.nm():
            self.do_nm_connect(None)
        print "Starting AdminServer"
        wl.nmStart("AdminServer")

    def do_kill(self, args):
        if (self.requisites | NEED_CONNECTED_NM):
            wl.nmKill(args)
        else:
            print "Connect to Node Manager first with nm_connect."

    def do_shell(self, args):
        try:
            self.__wlst(args)
        except:
            pass

    def __wlst(self, args):
        eval('wl.' + args)
        
    def emptyline(self):
        return True

    def __satisfies_credentials_and_node(self):
        if not (self.requisites & (NEED_CREDENTIALS | NEED_NODE)):
            print "Set credentials and/or node first with 'credentials' and 'node' commands"
            return False
        else:
            return True
            
if __name__ == "__main__":
    WebHi().cmdloop()
