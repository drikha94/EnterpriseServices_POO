import pandas as pd

excel = pd.read_excel('C:/Users/awx910701/Documents/Configuraciones/Script/2023/Enero/Rawson/Migracion_Rawson.xlsx', sheet_name='B2B')

for x in range(len(excel)):
    print(x)
#print(excel)