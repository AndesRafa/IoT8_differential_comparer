import sys
import json
from treecompare import diff
from differential import Differential


def loadJSONApi(path):
    f = open(path, 'r')
    japi = json.loads(f.read())
    f.close()
    return japi


def compareApis(api1, api2):
    return diff(api1, api2)


def parseDifferentials(diffs):
    differentials = []
    for diff in diffs:
        differentials.append(Differential(diff))

    for d in differentials:
        print('\t- route: {}\n\t- value: {}'.format(d.route, d.value))


def processApis(path_api1, path_api2):
    api1 = loadJSONApi(path_api1)
    api2 = loadJSONApi(path_api2)

    diffs = compareApis(api1, api2)
    parseDifferentials(diffs)

    return diffs


def main():
    args = sys.argv
    if len(args) < 3:
        print('Requires API v1 and API v2 paths for comparisson')
        return 2

    path_api1 = args[1]
    path_api2 = args[2]


    print(processApis(path_api1, path_api2))


if __name__ == '__main__':
    main()
