from dlresultserm.db.sqlite import createTable, deleteTable, insertSetOfValues, insertValues


def reset_tables(conn, tables, columns):

    for table in tables:
        deleteTable(conn, table)
        createTable(conn, table, columns[table])

    return


def extend_list(base, prefix=[], suffix=[]):
    return prefix + base + suffix


def extend_nested_list(list_base, prefix=[], suffix=[]):
    return [extend_list(base, prefix, suffix) for base in list_base]


def extend_columns(columns, prefix=[], suffix=[]):
    new_columns = {}
    for k, v in columns.items():
        new_columns[k] = extend_list(v, prefix, suffix)

    return new_columns


def reset_results_tables(conn, tables, keys, include_ubigeo=True):

    if include_ubigeo:
        columns = extend_columns(keys, ["ubigeo"])
    else:
        columns = keys

    return reset_tables(conn, tables, columns)


def insert_results_values(conn, tables, columns, data, ubigeo_key="ubigeo"):

    for table in tables:
        if isinstance(data[table][0], list):

            insertSetOfValues(
                conn,
                table,
                extend_list(columns[table], [ubigeo_key]),
                extend_nested_list(
                    data[table], [data[ubigeo_key]]))
        else:
            insertValues(
                conn,
                table,
                extend_list(columns[table], [ubigeo_key]),
                extend_list(
                    data[table], [data[ubigeo_key]]))


if __name__ == "__main__":

    from dlresultserm.utils.json import get_json_from_file
    from dlresultserm.db.sqlite import connect

    data = get_json_from_file("output/results.json")
    conn = connect("output/db.sql")

    tables = data["header"]["tables"]
    columns = data["header"]["keys"]
    reset_results_tables(conn, tables, columns)
    insert_results_values(conn, tables, columns, data["data"][0])
