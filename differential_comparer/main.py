import sys, os, json

from kaz_json import json as kjson

from httpinterface import get, post
from services.comparer import processApis 


CONFLICT_SOLVER_URL = os.getenv('CONFLICT_SOLVER_URL')


def main():
    args = sys.argv
    postContent = False
    
    if len(args) < 3:
        print('Requires API v1 and API v2 paths for comparisson')
        return 2

    if len(args) > 3:
        postContent = bool(args[3])

    path_api1 = args[1]
    path_api2 = args[2]

    differential = processApis(path_api1, path_api2)

    payload = [diff for diff in differential.element_differentials]

    if not postContent:
        print(kjson.toJSON(differential))
        return 0

    #conflict_uri = '{}/conflict'.format(CONFLICT_SOLVER_URL)
    #print('-Delivering data to server {}\n{}\n'.format(conflict_uri, payload))

    #response = post(
    #        '{}/conflict'.format(CONFLICT_SOLVER_URL),
    #        data=json.dumps(payload),
    #        json=None,
    #    )

    #print('-Received \n{}\n'.format(response.json))


if __name__ == '__main__':
    main()
