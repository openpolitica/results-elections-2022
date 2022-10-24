import sqlite3
from pathlib import Path
import os
from dlresultserm.logger import logger, setLoggerLevel
import json


def adapt_dict(d):
    return json.dumps(d)


sqlite3.register_adapter(dict, adapt_dict)


def connect(filename):
    directory = os.path.dirname(filename)
    Path(directory).mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(filename)


def execute(conn, *args):
    cur = conn.cursor()
    res = cur.execute(*args)
    if(args[0].find("INSERT") >= 0):
        conn.commit()
    return res.fetchall()


def readTable(conn, tableName, columnNames=None):
    query = "SELECT "
    query += columnNames.join(",") if columnNames is not None else "*"
    query += " FROM "
    query += tableName

    return execute(conn, query)


def execCustomQuery(conn, query):
    return execute(conn, query)


def process_column_name(columnName, pk, columnNames, columnTypes):

    if (columnTypes):
        index = zip(*columnNames)[0].index(
            columnName) if columnName in zip(*columnNames)[0] else -1
        if (index >= 0):
            return (
                columnName +
                " " +
                columnTypes[index][1] +
                " " +
                ("NULL" if columnTypes[index][2] else "NOT NULL") +
                (" PRIMARY KEY" if columnName == pk else "")
            )

    return columnName + " TEXT" + (" PRIMARY KEY" if columnName == pk else "")


def createTable(
        conn,
        tableName,
        columnNames,
        pk=None,
        columnTypes=None):
    if (pk is None):
        logger.warning(
            "createTable: [" +
            tableName +
            "] Primary key not defined. Not included in creation"
        )
    else:
        if pk not in columnNames:
            logger.warning(
                "createTable: [" +
                tableName +
                "] Indicated primary key not defined in columns names."
                "Not considered.")

    if (columnTypes is None):
        logger.warning(
            "createTable: [" +
            tableName +
            "] ColumnTypes no provided. All columns set as TEXT."
        )

    query = "CREATE TABLE IF NOT EXISTS "
    query += tableName
    query += " ("
    query += ",".join([process_column_name(
                       columnName, pk, columnNames, columnTypes)
                       for columnName in columnNames
                       ])
    query += ")"

    logger.debug(query)
    return execute(conn, query)


def deleteTable(conn, tableName):
    query = "DROP TABLE IF EXISTS "
    query += tableName

    logger.debug(query)
    return execute(conn, query)


def insertValues(conn, tableName, columnNames, values):
    if (len(columnNames) < len(values)):
        values = values[:len(columnNames)]

    if (len(columnNames) > len(values)):
        columnNames = columnNames[:len(values)]

    query = "INSERT INTO "
    query += tableName
    query += " ("
    query += ",".join(columnNames)
    query += ") VALUES ("
    query += ", ".join(["?" for _ in columnNames])
    query += ")"

    values = [value if value != "" else None for value in values]
    logger.debug(values)
    logger.debug(query)
    return execute(conn, query, tuple(values))


def insertSetOfValues(conn, tableName, columnNames, values):
    return [
        insertValues(conn, tableName, columnNames, value)
        for value in values]


def dropForeignKey(conn, tableOrigin, name):
    query = "ALTER TABLE IF EXISTS "
    query += tableOrigin
    query += " DROP CONSTRAINT IF EXISTS "
    query += name

    logger.debug(query)
    return execute(conn, query)


def createForeignKey(
    conn,
    tableOrigin,
    foreignKey,
    tableForeign,
    primaryKey,
    number=1,
    cascade=True
):
    query = "ALTER TABLE IF EXISTS "
    query += tableOrigin
    query += " ADD CONSTRAINT "
    query += generateForeignKeyName(tableOrigin, tableForeign, number)
    query += " FOREIGN KEY ("
    query += foreignKey
    query += ") REFERENCES "
    query += tableForeign
    query += " ("
    query += primaryKey
    query += ")"
    if (cascade):
        query += " ON DELETE CASCADE ON UPDATE CASCADE"

    logger.debug(query)
    return execute(conn, query)


def createIndex(conn, table, columnNames):
    query = "CREATE INDEX ON "
    query += table
    query += "("
    query += columnNames
    query += ")"

    logger.debug(query)
    return execute(conn, query)


def generateForeignKeyName(tableOrigin, tableForeign, number):
    return tableOrigin + "_" + tableForeign + "_fk" + number


def dropListOfForeignKeys(conn, listOfForeignKeys):
    return [
        dropForeignKey(
            conn,
            foreignKey[0],
            generateForeignKeyName(foreignKey[0], foreignKey[2], 1)
        )
        for foreignKey in listOfForeignKeys
    ]


def createListOfForeignKeys(conn, listOfForeignKeys):
    return [createForeignKey(conn, *foreignKey)
            for foreignKey in listOfForeignKeys]


def createListOfIndexes(conn, listOfIndexes):
    return [
        createIndex(conn, *indexInfo)
        for indexInfo in listOfIndexes
    ]


def addColumn(conn, tableName, columnName, columntype):
    query = "ALTER TABLE IF EXISTS "
    query += tableName
    query += " ADD COLUMN "
    query += columnName
    query += " "
    query += columntype

    return execute(conn, query)


if __name__ == "__main__":

    conn = connect("output/db.sql")
    deleteTable(conn, "results")
    createTable(conn, "results", ["ubigeo", "party"], "ubigeo")
    insertValues(conn, "results", ["ubigeo", "party"], ["0002", "My party"])
