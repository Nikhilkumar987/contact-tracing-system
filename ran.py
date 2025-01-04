import random as rd
import time
from datetime import datetime, timedelta
import pandas as pd


names = [
    "Ajay", "carlos", "Messi", "Dyabala", "E.ten.stegen", "kunde", "Gavi", "Asu fati", "Jude", "Haaland",
    "torres", "Banckerbaur", "Rudigiier", "D.paul", "maradona", "Ronaldino", "can", "Tom", "baggio", "Veria",
    "Willshar", "Xians", "Yorke", "Toni", "Modric", "Theo", "Lewendoski", "Owen", "Peries", "Romario"
]


start_date = datetime(2020, 7, 1)  
end_date = datetime(2020, 7, 31)   


lat_range = [10.0, 20.0]
lon_range = [70.0, 80.0]
data = []


for name in names:
    for i in range(rd.randint(1, 50)):  
        timestamp = start_date + (end_date - start_date) * rd.random()
        timestamp = int(time.mktime(timestamp.timetuple()))
        latitude = round(rd.uniform(*lat_range), 7)
        longitude = round(rd.uniform(*lon_range), 7)
        data.append({
            "id": name,
            "timestamp": timestamp,
            "latitude": str(latitude),
            "longitude": str(longitude)
        })


df = pd.DataFrame(data)
df.to_json("livedata2.json", orient="records", lines=False)

print("JSON file 'generated_data.json' has been created successfully.")
