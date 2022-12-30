from django.db import connections


def ejecutar_sql(sql, retorno=1):
    cursor = connections['default'].cursor()
    cursor.execute(sql=sql)
    if retorno:
        result = cursor.fetchone()
        cursor.close()
        return result
    else:
        cursor.close()


def obtener_anio_mes_proceso():
    sql = f"SELECT Mes, Anio FROM Inatec.Inatec_Control"
    datos = ejecutar_sql(sql, 1)
    return datos


def mes_en_letra(mes):
    nmes = ''

    if mes == 1:
        nmes = 'Enero'
    elif mes == 2:
        nmes = 'Febrero'
    elif mes == 3:
        nmes = 'Marzo'
    elif mes == 4:
        nmes = 'Abril'
    elif mes == 5:
        nmes = 'Mayo'
    elif mes == 6:
        nmes = 'Junio'
    elif mes == 7:
        nmes = 'Julio'
    elif mes == 8:
        nmes = 'Agosto'
    elif mes == 9:
        nmes = 'Septiembre'
    elif mes == 10:
        nmes = 'Octubre'
    elif mes == 11:
        nmes = 'Noviembre'
    elif mes == 12:
        nmes = 'Diciembre'
    else:
        nmes = 'Desconocido'

    return nmes
