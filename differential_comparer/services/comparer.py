import re
import json

from treecompare import diff

from models.differentials import DifferentialType, ApiDifferential, ElementDifferential

EXP = `'(.*?)'`
EXP_PATTERN = re.compile(EXP)


def loadJSONApi(path):
    f = open(path, 'r')
    japi = json.loads(f.read())
    f.close()
    return japi


def compareJSONApis(japi1, japi2):
    return diff(japi1, japi2)


def processApis(path_api1, path_api2):
    japi1 = loadJSONApi(path_api1)
    japi2 = loadJSONApi(path_api2)


    diffs = compareJSONApis(japi1, japi2)
    if not len(diffs) > 0:
        return None

    api_differential = ApiDifferential(
                api_name=japi1['info']['title'],
                api_server=japi1['servers'][0]['url'],
                api_old_version=japi1['info']['version'],
                api_new_version=japi1['info']['version']
            )

    for diff in diffs: 
        element_path = parsePath(diff.path)
        old_element, new_element = parseMessage(diff.message)
        
        diff_type = DifferentialType.MODIFY
        if old_element is None and not new_element is None:
            diff_type = DifferentialType.ADD
        if not old_element is None and new_element is None:
            diff_type = DifferentialType.DELETE

        api_differential.addElementDifferential(ElementDifferential(
                    differential_type=diff_type.value,
                    element_path=element_path,
                    old_element=old_element,
                    new_element=new_element, 
                ))

    return api_differential


def parsePath(path):
    route = []

    for node in path:
        search = EXP_PATTERN.search(node)
        if not search:
            continue

        nodestr = node[search.start()+1:search.end()-1]
        route.append(nodestr)

    return route


def parseMessage(msg):
    if msg[:8].upper() == 'EXPECTED':
        diff_type = 'EXPECTED'
        return _parseMessageExpected(msg)
    else:
        diff_type = 'UNEXPECTED'
        return _parseMessageUnexpected(msg)


def _parseMessageExpected(msg):
    gotIndex = msg.rfind(', got ')
    commaIndex = msg.find(',')
    expectedIndex = 8

    if gotIndex < 1:
        return None, None
    
    oldValue = _adjustValueFormat(str(msg[8:commaIndex]).strip())
    newValue = str(msg[gotIndex + 6:]).strip()

    if newValue.upper() == 'NOTHING':
        return oldValue, None
    
    search = EXP_PATTERN.search(newValue)
    if not search:
        return oldValue, newValue

    newValue = newValue[search.start() + 1:search.end() - 1]
    return oldValue, newValue


def _parseMessageUnexpected(msg):
    valueIndex = msg.find(':')

    if valueIndex < 1:
        return None, None

    value = str(msg[valueIndex + 1:]).strip()
    value = _adjustValueFormat(value)

    return None, value


def _adjustValueFormat(value):
    value = str(value).replace('\'', '"')
    value = value.replace('u"', '')
    value = value.replace('True', 'true')
    value = value.replace('False', 'false')
    value = value.replace('"', '')

    return value
