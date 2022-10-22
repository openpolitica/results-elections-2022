import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)',
}


def getResponse(url):

    response = requests.get(url, headers=headers)
    if(response.status_code != 200):
        raise ValueError

    return response.json()


if __name__ == "__main__":

    response_1 = getResponse(
        "https://api.resultadoserm2022.onpe.gob.pe/results/01/010000")

    keys = response_1.keys()

    print(keys)
    for key in list(keys):
        if isinstance(response_1[key], list):
            print(
                f'"{key}"' + ":[" + ",".join(
                    [f'"{item}"' for item in response_1[key][0].keys()]) +
                "]")
        else:
            print(f'"{key}"' + ":[" +
                  ",".join([f'"{item}"' for item in response_1[key].keys()]) +
                  "]")
