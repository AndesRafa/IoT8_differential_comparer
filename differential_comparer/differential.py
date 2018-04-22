import re
import json
import io

EXP = `'(.*?)'`

class Differential():

    def __init__(
                    self, 
                    api_name,
                    old_api_version,
                    new_api_version,
                    diff,
                ):
        self.pattern = re.compile(EXP)

        self.api_name = api_name.encode("utf-8")
        self.old_api_version = old_api_version.encode("utf-8")
        self.new_api_version = new_api_version.encode("utf-8")
        self.path = [x.encode("utf-8") for x in self.ParsePath(diff.path)]
        self.type = 'EXPECTED' # EXPECTED or UNEXPECTED
        self.old_value, self.new_value = self.ParseMessage(diff.message)


    def toJSON(self):
        return {
                "api_name":self.api_name,
                "old_api_version":self.old_api_version,
                "new_api_version":self.new_api_version,
                "path":self.path,
                "type":self.type,
                "old_value":self.old_value,
                "new_value":self.new_value,
                }


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
            self.type = 'EXPECTED'
            return self.ParseMessageExpected(msg)
        else:
            self.type = 'UNEXPECTED'
            return self.ParseMessageUnexpected(msg)


    def ParseMessageExpected(self, msg):
        gotIndex = msg.rfind(', got ')
        commaIndex = msg.find(',')
        expectedIndex = 8

        if gotIndex < 1:
            return None, None
        
        oldValue = adjustValueFormat(str(msg[8:commaIndex]).strip())
        newValue = str(msg[gotIndex + 6:]).strip()

        if newValue.upper() == 'NOTHING':
            return oldValue, None
        
        search = self.pattern.search(newValue)
        if not search:
            return oldValue, newValue

        newValue = newValue[search.start() + 1:search.end() - 1]
        return oldValue, newValue


    def ParseMessageUnexpected(self, msg):
        valueIndex = msg.find(':')

        if valueIndex < 1:
            return None, None

        value = str(msg[valueIndex + 1:]).strip()
        value = adjustValueFormat(value)

        return None, value


def adjustValueFormat(value):
    value = str(value).replace('\'', '"')
    value = value.replace('u"', '')
    value = value.replace('True', 'true')
    value = value.replace('False', 'false')
    value = value.replace('"', '')

    return value
