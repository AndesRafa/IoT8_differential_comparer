import sys, os, json
from comparer import processApis
from httpinterface import get, post


CONFLICT_SOLVER_URL = os.getenv('CONFLICT_SOLVER_URL')


def main():
    args = sys.argv
    if len(args) < 3:
        print('Requires API v1 and API v2 paths for comparisson')
        return 2

    path_api1 = args[1]
    path_api2 = args[2]

    differentials = processApis(path_api1, path_api2)

    payload = [diff.toJSON() for diff in differentials]

    conflict_uri = '{}/conflict'.format(CONFLICT_SOLVER_URL)
    print('-Delivering data to server {}\n{}\n'.format(conflict_uri, payload))

    response = post(
            '{}/conflict'.format(CONFLICT_SOLVER_URL),
            data=json.dumps(payload),
            json=None,
        )

    print('-Received \n{}\n'.format(response.json))


if __name__ == '__main__':
    main()
