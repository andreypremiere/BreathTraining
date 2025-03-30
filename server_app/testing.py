# import time
# from datetime import datetime
# import pandas as pd
#
# import requests
#
# # Пример данных
# data = {
#     "timestamp": [],
#     "mark_belly": [],
#     "mark_breast": []
# }
#
# k = 0
# while k < 10:
#     data['timestamp'].append(datetime.now())
#     data['mark_belly'].append(k+0.5)
#     data['mark_breast'].append(k+0.1)
#     time.sleep(1)
#     k += 1
#
# # Создание DataFrame
# df = pd.DataFrame(data)
#
# print(df)
#
# # Преобразование в JSON
# df_json = df.to_json(orient="records")
# print(df_json)
#
# new_df = pd.DataFrame(df_json)

print([] is None)
