from dotenv import load_dotenv

load_dotenv()

resource_ubigeo = {
    "path": 'data/locations.csv',
    "index": 1
}
url_base = "https://api.resultadoserm2022.onpe.gob.pe/results/01/"
tables = ['generals', 'results', "summary"]

keys = {
    "generals": [
        "generalData",
        "actData",
        "realImages"],
    "results": [
        "C_CODI_AGP",
        "AGRUPACION",
        "IMAGENAGRUPACION",
        "PORC_AVANCE_ACTA",
        "ACTAS_COMPUTADA",
        "TOTAL_MESAS",
        "TOTAL_VOTOS",
        "NLISTA",
        "POR_VALIDOS",
        "POR_EMITIDOS"],
    "summary": [
        "CCODI_UBIGEO",
        "CONTABILIZA",
        "CONT_NORMAL",
        "IMPUGNADA",
        "ERROR_MAT",
        "MESAS_INSTALADAS",
        "ACTAS_PROCESADAS",
        "SOL_NULIDAD",
        "ILEGIBLE",
        "PENDIENTE",
        "OTRAS_OBS",
        "SIN_DATOS",
        "CONT_ANULADA",
        "POR_PROCESAR",
        "EXTRAVIADA",
        "SINIESTRADA",
        "INCOMPLETA",
        "SIN_FIRMA",
        "A_INSTALAR",
        "MESAS_NO_INST",
        "FUSIONADAS",
        "NTOTAL_AUTO",
        "MESAS_HABILES",
        "TOT_CIUDADANOS_VOTARON",
        "ELECTORES_HABIL",
        "ELECTORES_HABIL_50",
        "TOTAL_JEE"]}
