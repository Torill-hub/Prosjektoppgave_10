import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
 
def moving_avg(times, temperatures, n):
    valid_times = []
    avg = []
    for i in range(n, len(temperatures)-n):
        temp_def = temperatures[i - n:i + n + 1]
        avg_value = sum(temp_def) / len(temp_def)
        valid_times.append(times[i])
        avg.append(avg_value)
    return valid_times, avg
 
# Start tider
start_time = datetime(2021, 6, 11, 17, 31)
end_time = datetime(2021, 6, 12, 3, 5)
start_date = datetime(2021, 6, 11, 0, 0)
 
# Lister for ulike målinger
times_sola = []
temperatures_sola = []
pressures_sola = []
times_local = []
times_bar_local = []
pressures_abs_local = []
pressures_bar_local =[]
temperatures_local =[]
 
sirdal_temp = []
sirdal_trykk = []
sauda_temp = []
sauda_trykk = []
time_sauda_sirdal = []
 
# Lesing av data fra LOKAL.csv
with open("LOKAL.csv", "r") as LOKAL:
    file = csv.reader(LOKAL, delimiter=';')
    next(file)
    for row in file:
        Del = [str(elem.strip()) for elem in row]
        if len(Del) >= 5:
            time = Del[0]
            temperature = Del[4].replace(',', '.')
            pressure_abs = Del[3].replace(',', '.')
            pressure_bar = Del[2].replace(',', '.')
            if pressure_bar == (''):
                try:
                    dato_obj = datetime.strptime(time, "%m.%d.%Y %H:%M")
                    time_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")
                    temperature_float = float(temperature)
                    pressure_abs_float = float(pressure_abs) * 10
                    times_local.append(time_standard)
                    temperatures_local.append(temperature_float)
                    pressures_abs_local.append(pressure_abs_float)
                except ValueError:
                    pass
            else:
                try:
                    dato_obj = datetime.strptime(time, "%m.%d.%Y %H:%M")
                    time_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")
                    temperature_float = float(temperature)
                    pressure_abs_float = float(pressure_abs) * 10
                    pressure_bar_float = float(pressure_bar) * 10
                    pressures_bar_local.append(pressure_bar_float)
                    times_bar_local.append(time_standard)
                    times_local.append(time_standard)
                    temperatures_local.append(temperature_float)
                    pressures_abs_local.append(pressure_abs_float)
                except ValueError:
                    pass
 
# Lesing av data fra SOLA.csv
with open("SOLA.csv", "r") as SOLA:
    file = csv.reader(SOLA, delimiter=';')
    next(file)
    for row in file:
        Del = [str(elem.strip()) for elem in row]
        if len(Del) >= 5:
            time = Del[2]
            temperature = Del[3].replace(',', '.')
            pressure = Del[4].replace(',', '.')
            try:
                if "am" in time or "pm" in time:
                    dato_obj = datetime.strptime(time, "%d/%m/%Y %I:%M:%S %p")
                else:
                    dato_obj = datetime.strptime(time, "%d.%m.%Y %H:%M")
                time_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")
                temperature_float = float(temperature)
                pressure_float = float(pressure)
                times_sola.append(time_standard)
                temperatures_sola.append(temperature_float)
                pressures_sola.append(pressure_float)
            except ValueError:
                pass
 
# Lesing av data fra temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv (2).txt
with open("temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv (2).txt") as f:
    file = csv.reader(f, delimiter=";")
    next(file)
    for line in file:
        if len(line)>2 and line[2]:
            try:
                date_obj = datetime.strptime(line[2], "%d.%m.%Y %H:%M")
                if date_obj >= start_date:
                    if line[0] == "Sirdal - Sinnes":
                        sirdal_temp.append(float(line[3].replace(',', '.')))
                        sirdal_trykk.append(float(line[4].replace(',', '.')))
                    elif line[0] == "Sauda":
                        sauda_temp.append(float(line[3].replace(',', '.')))
                        sauda_trykk.append(float(line[4].replace(',', '.')))
                    if date_obj and date_obj not in time_sauda_sirdal:
                        time_sauda_sirdal.append(date_obj)
            except ValueError:
                pass
 
# Konvertering av tidspunkter til datetime-objekter
times_local_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_local]
times_sola_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_sola]
times_bar_local_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_bar_local]
 
# Oppgave a: Temperaturfall for begge filene
n=30
valid_times, avg_local_temp = moving_avg(times_local_datetime, temperatures_local, n)
 
temperatures_local_filtered = []
times_local_filtered = []
 
for time, temperature in zip(times_local_datetime, temperatures_local):
    if start_time <= time <= end_time:
        times_local_filtered.append(time)
        temperatures_local_filtered.append(temperature)
 
if temperatures_local_filtered:
    max_temp_local = max(temperatures_local_filtered)
    min_temp_local = min(temperatures_local_filtered)
    temperaturfall_times_local = [start_time, end_time]
    temperaturfall_values_local = [max_temp_local, min_temp_local]
else:
    temperaturfall_times_local = []
    temperaturfall_values_local = []
 
temperatures_sola_filtered = []
times_sola_filtered = []
 
for time, temperature in zip(times_sola_datetime, temperatures_sola):
    if start_time <= time <= end_time:
        times_sola_filtered.append(time)
        temperatures_sola_filtered.append(temperature)
 
if temperatures_sola_filtered:
    max_temp_sola = max(temperatures_sola_filtered)
    min_temp_sola = min(temperatures_sola_filtered)
    temperaturfall_times_sola = [start_time, end_time]
    temperaturfall_values_sola = [max_temp_sola, min_temp_sola]
else:
    temperaturfall_times_sola = []
    temperaturfall_values_sola = []
 
plt.figure(figsize=(10, 5))
plt.plot(times_local_filtered, temperatures_local_filtered, label="Lokal værstasjon", color='blue')
plt.plot(times_sola_filtered, temperatures_sola_filtered, label="Sola værstasjon", color="green")
plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.title("Temperaturfall")
plt.legend()
plt.show()
 
#Oppgave b: plott et histogram over temperaturene fra begge filene, bruk en hel grad for hver søyle
plt.figure(figsize=(10, 5))
plt.hist(temperatures_local, bins=range(int(min(temperatures_local)), int(max(temperatures_local)) + 1), alpha=0.5, label="Lokal værstasjon")#Lager histogram
plt.hist(temperatures_sola, bins=range(int(min(temperatures_sola)), int(max(temperatures_sola)) + 1), alpha=0.5, label="Sola værstasjon")
plt.xlabel("Temperatur (°C)")
plt.ylabel("Antall")
plt.title("Histogram over temperaturer")
plt.legend()
plt.show()
 
# Oppgave c: Differanse mellom absolutt og barometrisk trykk
pressure_diff_local = [abs - bar for abs, bar in zip(pressures_abs_local, pressures_bar_local)]
pr_diff_time, pr_diff_value = moving_avg(times_bar_local_datetime, pressure_diff_local, 10)
 
plt.figure(figsize=(10, 5))
plt.plot(pr_diff_time, pr_diff_value, label="Differanse mellom absolutt og barometrisk trykk")
plt.xlabel("Tid")
plt.ylabel("Trykkdifferanse (bar)")
plt.title("Differanse mellom absolutt og barometrisk trykk")
plt.legend()
plt.show()
 
# Oppgave d: Data fra andre værstasjoner
plt.figure(figsize=(10, 5))
plt.plot(times_sola_datetime, temperatures_sola, label="Sola værstasjon", color="green")
plt.plot(time_sauda_sirdal[:len(sirdal_temp)], sirdal_temp, label="Sirdal - Sinnes", color="red") #len betyr at vi tar like mange målinger fra sirdal som sola
plt.plot(time_sauda_sirdal[:len(sauda_temp)], sauda_temp, label="Sauda", color="purple")
plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.title("Temperaturmålinger fra flere værstasjoner")
plt.legend()
plt.show()