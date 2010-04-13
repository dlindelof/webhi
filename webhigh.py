import cmd
import wl
try:
    import readline
except:
    pass

class WebHigh(cmd.Cmd):
    info = "Welcome to the WebHigh administration console"
    prompt = "webhigh> "
    
    def do_enroll(self, args):
        print "Enroll called"

    def do_nm_start(self, args):
        print "Starting Node Manager..."
        wl.startNodeManager()

    def do_credentials(self, args):
        argslist = args.split()
        if len(argslist) != 2:
            print "credentials: expected two arguments"
            return
        print "Setting credentials: " + args
        (self.username, self.password) = args.split()
        self.credentials_set = True

    def do_node(self, args):
        print "Setting node: " + args
        (self.host, self.port, self.domain) = args.split()
        self.node_set = True
        
    def do_connect(self, args):
        if self.credentials_set:
            print "Connecting to: " + args
            wl.connect(self.username, self.password, args)
        else:
            print "Set credentials first with 'credentials username password'"

    def do_as_start(self, args):
        if not wl.nm():
            if not (self.credentials_set and self.node_set):
                print "Set credentials and/or node first with 'credentials' and 'node' commands"
            else:
                print "Connecting to Node Manager on: " + self.domain + "@" + self.host
                wl.nmConnect(self.username, self.password,
                             self.host, self.port,
                             self.domain, nmType='plain')
        print "Starting AdminServer"
        wl.nmStart("AdminServer")

    def emptyline(self):
        return True
            
if __name__ == "__main__":
    WebHigh().cmdloop()
