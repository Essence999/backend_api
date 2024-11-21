import datetime


def data():
    # Obtém o dia atual
    data_atual = datetime.datetime.now()

    # Formata a data no formato SQL
    # data_sql = data_atual.strftime('%Y-%m-%d %H:%M:%S')
    data_sql_str = data_atual.strftime('%Y-%m-%d')
    # data_sql = data_atual.strftime('%Y-%m-%d 00:00:00') #INFO-CARDS
    data_sql = data_atual.strptime(data_sql_str, '%Y-%m-%d').date() #DEV
    print(type(data_sql))
    return data_sql