import sys
import json
from treecompare import diff
from differential import Differential
from api_descriptor import ApiDescriptor


def loadJSONApi(path):
    f = open(path, 'r')
    japi = json.loads(f.read())
    api_descriptor = ApiDescriptor(
                name=japi['info']['title'],
                version=japi['info']['version'],
                model=japi,
            )
    f.close()
    return api_descriptor


def compareApis(api1, api2):
    return diff(api1.model, api2.model)


def parseDifferentials(
            original_api,
            new_api,
            diffs
        ):

    differentials = []
    for diff in diffs:
        differentials.append(Differential(
                original_api.name,
                original_api.version,
                new_api.version,
                diff,
            ))

    return differentials


def processApis(path_api1, path_api2):
    api_descriptor1 = loadJSONApi(path_api1)
    api_descriptor2 = loadJSONApi(path_api2)

    diffs = compareApis(
                api_descriptor1, 
                api_descriptor2,
            )

    parsed_diffs = parseDifferentials(
                api_descriptor1,
                api_descriptor2,
                diffs,
            )

    return parsed_diffs


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
