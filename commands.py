from document import document
import urllib.request
import urllib.parse
import json

class commands:
    def __init__ (self, connection):
        self.connection = connection
        self.keywords = []
        
        #Add your own KEYWORDS. Please consult the documentation at
        #self.keywords.append({'find': [['*', 'hello', '*', 'you', '*'], 'hello'], 'call': 'hans'})
        #self.keywords.append({'find': [['turn', '*', 'lights', '*'], ['turn', '*', 'light', '*'], ['turn', '*', 'lamp', '*'], ['turn', '*', 'lemp', '*'], ['turn', '*', 'late', '*'], ['turn', '*', 'like', '*'],], 'call': 'light'})
    
    def no_action (self, q, wildcards):
        spvoice_url = 'http://localhost:9000/command'
        params = urllib.parse.urlencode({ 'command': q }).encode('utf8')
        response = urllib.request.urlopen(spvoice_url, params).read().decode("utf-8")
        response = json.loads(response)
        html = document(self.connection)
        html.title("House")
        html.incoming(q)
        html.outgoing(response['response'].replace("\\n","<br />\n"))
        html.send()

    ### Add your commands in this section. Feel free to change EVERYTHING below this comment ###
        
    #def hans(self, q, wildcards):
        #html = document(self.connection)
        #html.title("Welcome")
        #html.outgoing(q)
        #html.incoming("Hi Robin!")
        #html.send()
        
    #def light(self, q, wildcards):
        #if (wildcards[1] == "one"):
            #id = 1
        #elif (wildcards[1] == "two"):
            #id = 2
        #elif (wildcards[1] == "three"):
            #id = 3
        #elif (wildcards[1] == "four"):
            #id = 4
        #elif (wildcards[1] == "five"):
            #id = 5
        #elif (wildcards[1] == "six"):
            #id = 6
        #else:
            #id = -1

        #html = document(self.connection)
        #html.title("Light Switch")
        #html.outgoing(q)
        #if ((wildcards[0] == "on" or wildcards[0] == "off") and id > -1):
            #html.incoming("Okay, let's turn " + wildcards[0] + " lamp " + wildcards[1])
            #html.send()
            #html.request("http://zimmer:2525/remote/" + wildcards[0] + "?id=" + str(id)) #Only works in my setup
        #else:
            #html.incoming("No such lamp available")
            #html.send()

    #def timetable(self, q, wildcards):
        #html = document (self.connection)
        #html.redirect("http://zimmer:5000/index.php?component=timetable&resolution=desktop") #Only works in my setup
        #html.send()
