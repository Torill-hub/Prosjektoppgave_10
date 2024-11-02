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
 
def calculate_standard_deviation(data, n):
    std_devs = []
    for i in range(len(data) - n + 1):
        window = data[i:i+n]
        std_dev = np.std(window, ddof=1)
        std_devs.append(std_dev)
    return std_devs
 
# Start tider
start_time = datetime(2021, 6, 11, 17, 31)
end_time = datetime(2021, 6, 12, 3, 5)
start_date = datetime(2021, 6, 11, 0, 0)
 
# Lister for ulike målinger
times_sola = []
temperatures_sola = []
pressures_sola = []
times_local = []
pressures_abs_local = []
temperatures_local = []
 
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
 
# Konvertering av tidspunkter til datetime-objekter
times_local_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_local]
times_sola_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_sola]
 
# Oppgave e: Gjennomsnittlig forskjell mellom temperatur og trykk
# Filtrere data for felles tidspunkter
common_times = set(times_local_datetime).intersection(times_sola_datetime)
common_times = sorted(common_times)
 
# Beregne forskjeller i temperatur og trykk
temp_diffs = []
pressure_diffs = []
for time in common_times:
    local_index = times_local_datetime.index(time)
    sola_index = times_sola_datetime.index(time)
    temp_diff = abs(temperatures_local[local_index] - temperatures_sola[sola_index])
    pressure_diff = abs(pressures_abs_local[local_index] - pressures_sola[sola_index])
    temp_diffs.append(temp_diff)
    pressure_diffs.append(pressure_diff)
 
# Beregne gjennomsnittlig forskjell
avg_temp_diff = np.mean(temp_diffs)
avg_pressure_diff = np.mean(pressure_diffs)
 
# Finne tidspunkter med lavest og høyest forskjell
min_temp_diff_time = common_times[temp_diffs.index(min(temp_diffs))]
max_temp_diff_time = common_times[temp_diffs.index(max(temp_diffs))]
min_pressure_diff_time = common_times[pressure_diffs.index(min(pressure_diffs))]
max_pressure_diff_time = common_times[pressure_diffs.index(max(pressure_diffs))]
 
print(f"Gjennomsnittlig temperaturforskjell: {avg_temp_diff}")
print(f"Gjennomsnittlig trykkforskjell: {avg_pressure_diff}")
print(f"Minste temperaturforskjell: {min(temp_diffs)} ved {min_temp_diff_time}")
print(f"Største temperaturforskjell: {max(temp_diffs)} ved {max_temp_diff_time}")
print(f"Minste trykkforskjell: {min(pressure_diffs)} ved {min_pressure_diff_time}")
print(f"Største trykkforskjell: {max(pressure_diffs)} ved {max_pressure_diff_time}")
 
# Oppgave f: Plotting av standardavvik for den første datafila (Rune Time datasettet)
# Filtrere data for plotting
n=30
valid_times, avg_temp_local = moving_avg(times_local_datetime, temperatures_local, n)
 
temperatures_local_filtered = []
times_local_filtered = []
 
for time, temperature in zip(times_local_datetime, temperatures_local):
    if start_time <= time <= end_time:
        times_local_filtered.append(time)
        temperatures_local_filtered.append(temperature)
 
# Beregne standardavvik for temperaturdataene
std_dev_local = calculate_standard_deviation(temperatures_local_filtered, n)
 
# Juster tidspunktene for å matche lengden på standardavvik-listene
times_local_std = times_local_filtered[n-1:]
 
# Plotting av temperaturdata med standardavvik
plt.figure(figsize=(10, 5))
plt.errorbar(times_local_std, temperatures_local_filtered[n-1:], yerr=std_dev_local, errorevery=30, capsize=5, color='red', label="Standardavvik", zorder=1)
plt.plot(times_local_std, temperatures_local_filtered[n-1:], label="Lokal værstasjon", color="blue", linestyle="-", zorder=2)

plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.title("Temperaturmålinger med standardavvik")
plt.legend()
plt.show()

