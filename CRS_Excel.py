import random
from collections import deque
from scipy.stats import poisson
from datetime import datetime, timedelta
import pandas as pd

class Patient:
    def __init__(self, call_time, duration, scheduled_time):
        self.call_time = call_time
        self.duration = duration
        self.scheduled_time = scheduled_time

def main():
    queue_type1 = deque()
    queue_type2 = deque()
    calls_patient1(queue_type1)
    calls_patient2(queue_type2)

    df_type1 = extract_data(queue_type1, "Type 1")
    df_type2 = extract_data(queue_type2, "Type 2")

    # Write DataFrames to Excel
    write_to_excel([df_type1, df_type2], 'PatientData.xlsx')

def extract_data(queue, patient_type):
    data = []

    while queue:
        current_patient = queue.popleft()
        #waiting_time = current_patient.call_time - current_patient.scheduled_time
        data.append([patient_type, current_patient.call_time, current_patient.duration, current_patient.scheduled_time])

    columns = ['Type', 'Call Time', 'Duration', 'Scheduled Time']
    df = pd.DataFrame(data, columns=columns)
    return df

def write_to_excel(dfs, file_name):
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for i, df in enumerate(dfs, start=1):
            sheet_name = f'Sheet{i}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def duration_patient1():
    mean = 0.4326608 * 60
    std_dev = 0.097645 * 60
    return int(random.gauss(mean, std_dev))

def duration_patient2():
    mean = 0.669339 * 60
    std_dev = 0.186894 * 60
    return int(random.gauss(mean, std_dev))

def calls_patient1(queue_type1):
    current_date = datetime(2023, 8, 1, 8, 0)  # Start on 01.08.2023 at 08:00
    time_scheduled = datetime(2023, 8, 1, 8, 0) # Start on 02.08.2023 at 08:00

    for i in range(31):
        if time_scheduled.day <= i+1:
            if i < 30:
                time_scheduled = datetime(2023, 8, i+2, 8, 0)
            else: 
                time_scheduled = datetime(2023, 9, 1, 8, 0)
        
        call_time = current_date + timedelta(days=i)

        while call_time.time() < datetime(2023, 8, i+1, 17, 0).time():
            call_time += timedelta(minutes=poisson.rvs(60*0.505989))
            if call_time.time() < datetime(2023, 8, i+1, 17, 0).time():
                new_patient = Patient(call_time, duration_patient1(), time_scheduled)
                queue_type1.append(new_patient)
                if time_scheduled + timedelta(minutes=30) >= datetime(2023, time_scheduled.month, time_scheduled.day, 17, 0) or (time_scheduled.day <= call_time.day and time_scheduled.month <= call_time.month):
                    if time_scheduled.day < 31 and time_scheduled.month == 8:
                        time_scheduled = datetime(2023, 8, time_scheduled.day + 1, 8, 0)
                    elif time_scheduled.day == 31:
                        time_scheduled = datetime(2023, 9, 1, 8, 0)
                    else:
                        time_scheduled = datetime(2023, 9, time_scheduled.day+1, 8, 0)
                else:
                    time_scheduled += timedelta(minutes=30)

def calls_patient2(queue_type2):
    current_date = datetime(2023, 8, 1, 8, 0)  # Start on 01.08.2023 at 08:00
    time_scheduled = datetime(2023, 8, 2, 8, 0) # Start on 02.08.2023 at 08:00

    for i in range(31):
        if time_scheduled.day <= i+1:
            if i < 30:
                time_scheduled = datetime(2023, 8, i+2, 8, 0)
            else: 
                time_scheduled = datetime(2023, 9, 1, 8, 0)
        
        call_time = current_date + timedelta(days=i)

        while call_time.time() < datetime(2023, 8, i+1, 17, 0).time():
            call_time += timedelta(minutes=int(random.gauss(0.812092*60, 0.332368*60)))
            if call_time.time() < datetime(2023, 8, i+1, 17, 0).time():
                new_patient = Patient(call_time, duration_patient2(), time_scheduled)
                queue_type2.append(new_patient)
                if time_scheduled + timedelta(minutes=40) >= datetime(2023, time_scheduled.month, time_scheduled.day, 17, 0) or (time_scheduled.day <= call_time.day and time_scheduled.month <= call_time.month):
                    if time_scheduled.day < 31 and time_scheduled.month == 8:
                        time_scheduled = datetime(2023, 8, time_scheduled.day + 1, 8, 0)
                    elif time_scheduled.day == 31:
                        time_scheduled = datetime(2023, 9, 1, 8, 0)
                    else:
                        time_scheduled = datetime(2023, 9, time_scheduled.day+1, 8, 0)
                else:
                    time_scheduled += timedelta(minutes=40)
    

main()
