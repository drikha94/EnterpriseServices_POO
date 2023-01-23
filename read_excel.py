import pandas as pd
import numpy as np

df = pd.read_excel('C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Migracion San Juan.xlsx', sheet_name='B2B')

services = df[['H4-NAME','H4-INT', 'CORE-NAME', 'CORE-INT']]
service_to_list = services.to_numpy().tolist()

def fill_data():

    index = [0,1,2,3]
    for i in range(len(index)):
        for x in range(len(service_to_list)):
            value = str(service_to_list[x][index[i]])
            if value != 'nan':
                only_interface = value
            service_to_list[x][index[i]] = only_interface

    return service_to_list

excel_list = fill_data()
print(excel_list)


