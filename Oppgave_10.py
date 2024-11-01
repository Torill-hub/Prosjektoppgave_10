#leser inn data fra filene
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def moving_avg(times, temperatures, n):#reduserer støy ved å beregne gjennomsnittet
    valid_times = []
    avg =[]

    for i in range(n, len(temperatures)-n):
        temp_def = temperatures[i - n:i + n + 1]
        avg_value = sum(temp_def) / len(temp_def)

        valid_times.append(times[i])
        avg.append(avg_value)

    return valid_times, avg

#Start tider 
start_time = datetime(2021, 6, 11, 17, 31)
end_time = datetime(2021, 6, 12, 3, 5)
start_date = datetime(2021, 6, 11, 0, 0)

#lister for ulike målinger
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

with open("./LOKAL.csv", "r") as LOKAL:
    file = csv.reader(LOKAL, delimiter=';')
    next(file)                                      #Hopper over første linje; da denne har "feil" input 
    for row in file:
        Del = [str(elem.strip()) for elem in row]               
        if len(Del) >= 5:
            time = Del[0]
            temperature = Del[4].replace(',', '.')
            pressure_abs = Del[3].replace(',', '.')
            pressure_bar = Del[2].replace(',', '.')            #Strip fjerner mellomrom etc., split lager elementer ved ;
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

with open("./SOLA.csv", "r") as SOLA:
    file = csv.reader(SOLA, delimiter=';')
    next(file)
    for row in file:
        Del = [str(elem.strip()) for elem in row]            #Strip fjerner mellomrom etc., split lager elementer ved ;
        if len(Del) >= 5:                      
            time = Del[2]                            #Legger til 2. element i Del til tid
            temperature = Del[3].replace(',', '.')   #Legger til 3.element i Del til temperatur og bytter , med .
            pressure = Del[4].replace(',', '.')
            try:
                if "am" in time or "pm" in time:      #Tar hensyn til pm og am
                    dato_obj = datetime.strptime(time, "%d/%m/%Y %I:%M:%S %p") 
                else:
                    dato_obj = datetime.strptime(time, "%d.%m.%Y %H:%M")
                
                time_standard = dato_obj.strftime("%Y-%m-%d %H:%M:%S")   #Omformer til standardtid
                temperature_float = float(temperature)
                pressure_float = float(pressure)
                times_sola.append(time_standard)
                temperatures_sola.append(temperature_float)               #Legger til verdier i de tomme listene
                pressures_sola.append(pressure_float)
            except ValueError:                                          #Dersom en verdi error oppstår, slik som i første linje, hopper python over
                pass

#Oppgave D; Tidene er like som for SOLA og SIRDAL_SAUDA            
with open("./SIRDAL_SAUDA.csv") as f:
    file = csv.reader(f, delimiter=";")
    next(file)
    
    for line in file:
        if line[2]:  
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

times_local_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_local]
times_sola_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_sola]
times_bar_local_datetime = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in times_bar_local]
           
n=30
valid_times, avg = moving_avg(times_local_datetime, temperatures_local, n)

temperatures_local_filtered = []
times_local_filtered = []

for time, temperature in zip(times_local_datetime, temperatures_local):
    if start_time <= time <= end_time:
        times_local_filtered.append(time)
        temperatures_local_filtered.append(temperature)

if temperatures_local_filtered:
    max_temp = max(temperatures_local_filtered)
    min_temp = min(temperatures_local_filtered)

    temperaturfall_times = [start_time, end_time]
    temperaturfall_values = [max_temp, min_temp]
else:
    temperaturfall_times = []
    temperaturfall_values = []
    
#plotter inn temperatur fra begge filene
temperatures_sola_filtered = []
times_sola_filtered = []

for time, temperature in zip(times_sola_datetime, temperatures_sola):
    if start_time <= time <= end_time:
        times_sola_filtered.append(time)
        temperatures_sola_filtered.append(temperature)

if temperatures_sola_filtered:
    max_temp = max(temperatures_sola_filtered)
    min_temp = min(temperatures_sola_filtered)

    temperaturfall_times_sola = [start_time, end_time]
    temperaturfall_values_sola = [max_temp, min_temp]
else:
    temperaturfall_times_sola = []
    temperaturfall_values_sola = []

#Temperatur PLOT
plt.figure(figsize=(10, 5))
plt.subplot(2, 2, 1)
plt.plot(times_local_filtered, temperatures_local_filtered, label="Lokal værstasjon", color='blue')
plt.plot(times_sola_datetime, temperatures_sola, label="Sola værstasjon", color="green")
plt.plot(times_local_datetime, temperatures_local, label="Lokal værstasjon ufiltrert", color='red')
plt.plot(valid_times, avg, label="Gjennomsnitt (n=30)", color="black")
plt.plot(temperaturfall_times, temperaturfall_values, label="Temperaturmålinger far Maksimal til Minimal")
plt.plot(temperaturfall_times, temperaturfall_values, label="Temperaturfall Lokal værstasjon")
plt.plot(temperaturfall_times_sola, temperaturfall_values_sola, label="Temperaturfall Sola værstasjon")

plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.title("Temperatur fra begge værstasjoner")
plt.legend()

#TEMPERATUR SIRDAL/SAUDA 
plt.subplot(2, 2, 2)
plt.plot(time_sauda_sirdal, sirdal_temp, label= "Sirdal værstasjon")
plt.plot(time_sauda_sirdal, sauda_temp, label = "Sauda værstasjon")
plt.plot(times_sola_datetime, temperatures_sola, label = "Sola værstasjon")
plt.plot(valid_times, avg, label="UIS værstasjon, n = 30")

plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.title("Temperaturer fra Sola, Sirdal, Sauda og filtrert UIS data")
plt.legend()

#Trykk PLOT
plt.subplot(2, 2, 3)
plt.title("Trykk fra begge værstasjoner")
plt.plot(times_local_datetime, pressures_abs_local, label = "Absoluttrykk Lokal stasjon") 
plt.plot(times_bar_local_datetime, pressures_bar_local, label = "Barometrisk trykk lokal stasjon") 
plt.plot(times_sola_datetime, pressures_sola, label = "Barometrisk trykk Sola værstasjon") 
plt.xlabel("Tid")
plt.ylabel("Trykk Pha")
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()

#Trykk fra nye data
valid_time, average_pressure = moving_avg(times_bar_local_datetime, pressures_bar_local, 30)

plt.subplot(2, 2, 4)
plt.plot(time_sauda_sirdal, sirdal_trykk, label = "Sirdal lufttrykk")
plt.plot(time_sauda_sirdal, sauda_trykk, label = "Sauda lufttrykk")
plt.plot(times_sola_datetime, pressures_sola, label = "Barometrisk trykk Sola værstasjon")
plt.plot(valid_time, average_pressure, label = "UIS lufttrykk, n = 30") 

plt.xlabel("Tid")
plt.ylabel("Trykk Pha")
plt.title("Trykkmålinger fra Sirdal, Sauda, Sola og UIS")
plt.legend()

#plott temperaturfall fra begge filene
plt.figure(figsize=(10, 5))
plt.plot(temperaturfall_times, temperaturfall_values, label="Temperaturfall Lokal værstasjon")
plt.plot(temperaturfall_times_sola, temperaturfall_values_sola, label="Temperaturfall Sola værstasjon")
plt.xlabel("Tid")
plt.ylabel("Temperatur (°C)")
plt.title("Temperaturfall fra maks til min temperatur")
plt.legend()

#plott et histogram over temperaturene fra begge filene, bruk en hel grad for hver søyle
plt.figure(figsize=(10, 5))
plt.hist(temperatures_local, bins=range(int(min(temperatures_local)), int(max(temperatures_local)) + 1), alpha=0.5, label="Lokal værstasjon")#Lager histogram
plt.hist(temperatures_sola, bins=range(int(min(temperatures_sola)), int(max(temperatures_sola)) + 1), alpha=0.5, label="Sola værstasjon")
plt.xlabel("Temperatur (°C)")
plt.ylabel("Antall")
plt.title("Histogram over temperaturer")
plt.legend()
plt.show()