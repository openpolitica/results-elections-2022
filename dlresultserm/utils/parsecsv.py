import csv


def get_csv(filename):
    response = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            response.append([item.strip() for item in row])

    return response


def get_csv_from_string(string):
    response = []
    reader = csv.reader(
        string.splitlines(),
        delimiter=',',
        quoting=csv.QUOTE_NONE)
    for row in reader:
        response.append([item.strip() for item in row])

    return response


if __name__ == "__main__":

    import pkgutil

    data = pkgutil.get_data(__name__, "../data/locations.csv")
    if data is not None:
        data = data.decode('utf-8')
    else:
        exit(1)

    print(get_csv_from_string(data))
