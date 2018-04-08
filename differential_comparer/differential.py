import re
import json
import io

EXP = `'(.*?)'`

class Differential():

    def __init__(self, diff):
        self.pattern = re.compile(EXP)

        self.path = self.ParsePath(diff.path)
        self.value = self.ParseMessage(diff.message)


    def ParsePath(self, path):
        pattern = self.pattern
        route = []

        for node in path:
            search = pattern.search(node)
            if not search:
                continue

            nodestr = node[search.start()+1:search.end()-1]
            route.append(nodestr)

        return route


    def ParseMessage(self, msg):
        if msg[:8].upper() == 'EXPECTED':
            return self.ParseMessageExpected(msg)
        else:
            return self.ParseMessageUnexpected(msg)


    def ParseMessageExpected(self, msg):
        gotIndex = msg.rfind(', got ')

        if gotIndex < 1:
            return None
        
        value = str(msg[gotIndex + 6:]).strip()
        if value.upper() == 'NOTHING':
            return None
        
        search = self.pattern.search(value)
        if not search:
            return value

        value = value[search.start() + 1:search.end() - 1]
        return value 


    def ParseMessageUnexpected(self, msg):
        valueIndex = msg.find(':')

        if valueIndex < 1:
            return None

        value = str(msg[valueIndex + 1:]).strip()
        value = str(value).replace('\'', '"')
        value = value.replace('u"', '"')
        value = value.replace('True', 'true')
        value = value.replace('False', 'false')

        j = json.load(io.StringIO(value.decode("utf-8")))

        self.recurseJSON(j, '')

        return value

    def recurseJSON(self, parent, tab):
        tab = '\t' + tab
        for field in parent:
            if len(field) <= 0:
                return
            #print('{}{} - {}'.format(tab, parent, parent[field]))
            #self.recurseJSON(field, tab)
