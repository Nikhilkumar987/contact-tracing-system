import random as rd
import time
from datetime import datetime, timezone
import pandas as pd

# List of names
names = [
    "Lionel Messi", "Cristiano Ronaldo", "Neymar", "Kylian Mbappé", "Robert Lewandowski", "Kevin De Bruyne", "Virgil van Dijk", "Erling Haaland", "Luka Modric", "Mohamed Salah",
    "Karim Benzema", "Harry Kane", "Sadio Mané", "Eden Hazard", "Sergio Ramos", "Toni Kroos", "Gerard Piqué", "Paul Pogba", "Manuel Neuer", "Alisson Becker",
    "Marc-André ter Stegen", "Thibaut Courtois", "Jan Oblak", "Andy Robertson", "Trent Alexander-Arnold", "Jadon Sancho", "Phil Foden", "Frenkie de Jong", "Ansu Fati", "Pedri",
    "João Félix", "Mason Mount", "Declan Rice", "Bukayo Saka", "Reece James", "Kalvin Phillips", "Kai Havertz", "Matthijs de Ligt", "Joshua Kimmich", "Leon Goretzka",
    "Alphonso Davies", "Achraf Hakimi", "Raphaël Varane", "Presnel Kimpembe", "Marquinhos", "Thiago Silva", "Casemiro", "Rodri", "Ilkay Gündogan", "Bernardo Silva",
    "Raheem Sterling", "Riyad Mahrez", "Lautaro Martínez", "Romelu Lukaku", "Paulo Dybala", "Angel Di María", "Gianluigi Donnarumma", "Keylor Navas", "Ederson Moraes", "Hugo Lloris",
    "Son Heung-min", "Pierre-Emerick Aubameyang", "Bruno Fernandes", "Anthony Martial", "Marcus Rashford", "Jesse Lingard", "Jack Grealish", "James Maddison", "Jamie Vardy", "Caglar Soyuncu",
    "Wilfried Zaha", "Christian Pulisic", "Timo Werner", "Mason Greenwood", "Dominic Calvert-Lewin", "Richarlison", "James Rodriguez", "Gareth Bale", "Aaron Ramsey", "Joe Allen",
    "Danny Ings", "Ollie Watkins", "Emiliano Buendia", "Emiliano Martínez", "Yann Sommer", "Granit Xhaka", "Fabian Schär", "Xherdan Shaqiri", "Breel Embolo", "Haris Seferovic",
    "Erik Lamela", "Lucas Moura", "Steven Bergwijn", "Giovani Lo Celso", "Davinson Sánchez", "Sergio Reguilón", "Harry Maguire", "Victor Lindelöf", "Raphaël Varane", "Luke Shaw",
    "Donny van de Beek", "Fred", "Scott McTominay", "Edinson Cavani", "Zlatan Ibrahimovic", "Thiago Alcântara", "Jordan Henderson", "Virgil van Dijk", "Joel Matip", "Joe Gomez",
    "Diogo Jota", "Fabinho", "Naby Keïta", "Georginio Wijnaldum", "Roberto Firmino", "Alex Oxlade-Chamberlain", "Takumi Minamino", "Harvey Elliott", "Curtis Jones", "Kostas Tsimikas",
    "Ibrahima Konaté", "Adama Traoré", "Ruben Neves", "João Moutinho", "Pedro Neto", "Raúl Jiménez", "Conor Coady", "Max Kilman", "Romain Saïss", "Leander Dendoncker",
    "Daniel Podence", "Nélson Semedo", "Jonny Otto", "Fernando Muslera", "Arda Turan", "Radamel Falcao", "Fernando Llorente", "Andrés Iniesta", "Xavi Hernandez", "David Villa",
    "Carles Puyol", "Eric Abidal", "Victor Valdés", "Jordi Alba", "Sergio Busquets", "Cesc Fàbregas", "Gerard Moreno", "Dani Parejo", "Raúl Albiol", "Carlos Bacca",
    "Samuel Chukwueze", "Pau Torres", "Daniel Carvajal", "Lucas Vázquez", "Isco Alarcón", "Marco Asensio", "Eden Hazard", "Luka Jovic", "Federico Valverde", "Eduardo Camavinga",
    "Vinícius Júnior", "Rodrygo Goes", "Ferland Mendy", "David Alaba", "Nacho Fernandez", "Eder Militao", "Marcelo Vieira", "Dani Ceballos", "Oscar Mingueza", "Sergi Roberto",
    "Martin Braithwaite", "Luuk de Jong", "Memphis Depay", "Ferran Torres", "Pierre-Emerick Aubameyang", "Franck Kessié", "Andreas Christensen", "Raphinha", "Robert Lewandowski", "Ousmane Dembélé",
    "Jules Koundé", "Ronald Araújo", "Eric García", "Marcos Alonso", "Alejandro Balde", "Pablo Torre", "Gavi", "Ansu Fati", "Sergio Agüero", "Philippe Coutinho",
    "Gérard Moreno", "Borja Iglesias", "Willian José", "Iñaki Williams", "Raúl García", "Alex Berenguer", "Mikel Merino", "Mikel Oyarzabal", "Alexander Isak", "David Silva",
    "Robin Le Normand", "Joselu", "Lucas Pérez", "Iago Aspas", "Santi Mina", "Denis Suárez", "Nolito", "Bryan Gil", "Carlos Soler", "José Gayà",
    "Gonçalo Guedes", "Maximiliano Gómez", "Sergio Canales", "Nabil Fekir", "Juanmi", "William Carvalho", "Guido Rodríguez", "Borja Iglesias", "Loren Morón", "Aitor Ruibal",
    "Rui Silva", "Luis Suárez", "Ezequiel Garay", "Pablo Zabaleta", "Javier Mascherano", "Gonzalo Higuaín", "Carlos Tevez", "Ezequiel Lavezzi", "Angel Correa", "Rodrigo de Paul",
    "Leandro Paredes", "Nicolás Otamendi", "Emiliano Martínez", "Alejandro Gómez", "Marcos Acuña", "Germán Pezzella", "Cristian Romero", "Lisandro Martínez", "Nicolás Tagliafico", "Joaquín Correa",
    "Giovani Lo Celso", "Julián Álvarez", "Lionel Scaloni", "Walter Samuel", "Roberto Ayala", "Juan Roman Riquelme", "Carlos Bianchi", "Marcelo Gallardo", "Hernan Crespo", "Matias Almeyda",
    "Claudio Caniggia", "Gabriel Batistuta", "Diego Simeone", "Oscar Ruggeri", "Dani Alves", "Thiago Silva", "Marquinhos", "Gabriel Jesus", "Vinicius Jr.", "Raphinha",
    "Lucas Paquetá", "Casemiro", "Fabinho", "Richarlison", "Gabriel Martinelli", "Antony", "Philippe Coutinho", "Arthur Melo", "Alex Sandro", "Danilo",
    "Eder Militao", "Renan Lodi", "Douglas Luiz", "Fred", "Matheus Cunha", "Willian", "Andreas Pereira", "Pedro", "Everton Ribeiro", "Roberto Firmino"
]


# Date range
start_date = datetime(2020, 7, 1)  
end_date = datetime(2020, 7, 31)

# Latitude and Longitude range
lat_range = [10.0, 20.0]
lon_range = [70.0, 80.0]

# Data generation
data = []
for name in names:
    for _ in range(rd.randint(1, 50)):  
        # Generate a random timestamp within the given date range
        timestamp = start_date + (end_date - start_date) * rd.random()
        
        # Convert to UTC timestamp and format it as 'YYYY-MM-DD HH:MM:SS'
        timestamp_utc = timestamp.astimezone(timezone.utc)
        timestamp_str = timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')  # Format to desired string
        
        # Generate random latitude and longitude
        latitude = round(rd.uniform(*lat_range), 7)
        longitude = round(rd.uniform(*lon_range), 7)
        
        # Append the data for each entry
        data.append({
            "id": name,
            "timestamp": timestamp_str,
            "latitude": str(latitude),
            "longitude": str(longitude)
        })

# Create a DataFrame
df = pd.DataFrame(data)

# Save to JSON
df.to_json("livedata2.json", orient="records", lines=False)

# Save to CSV
df.to_csv("livedata2.csv", index=False)

print("Files 'livedata2.json' and 'livedata2.csv' have been created successfully.")
