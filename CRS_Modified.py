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
    # Load data from Excel file into a pandas DataFrame
    file_path = "C:\\Users\\mabe6\\OneDrive\\Desktop\\Python Programming\\PatientData.xlsx"

    df_sheet1 = pd.read_excel(file_path, sheet_name='Sheet1')
    df_sheet2 = pd.read_excel(file_path, sheet_name='Sheet2')

    # Extract relevant columns
    columns_to_extract = ['Type', 'Call Time', 'Duration', 'Scheduled Time']

    # Create a combined DataFrame
    df_combined = pd.concat([df_sheet1[columns_to_extract], df_sheet2[columns_to_extract]], ignore_index=True)

    queue_type1 = deque()
    queue_type2 = deque()
    
    for index, row in df_combined.iterrows():
        call_type = row['Type']
        call_time = row['Call Time']
        duration = row['Duration']
        scheduled_time = row['Scheduled Time']

        new_patient = Patient(call_time, duration, scheduled_time)

        if call_type == 'Type 1':
            queue_type1.append(new_patient)
        elif call_type == 'Type 2':
            queue_type2.append(new_patient)

    overtime_type1, idle_time_type1, number_Patients1, waiting_Times1 = calculate_overtime_and_idle_time(queue_type1)
    overtime_type2, idle_time_type2, number_Patients2, waiting_Times2 = calculate_overtime_and_idle_time(queue_type2)

    print_overtime_and_idle_time("Type 1 Results", overtime_type1, idle_time_type1, number_Patients1)
    print_overtime_and_idle_time("Type 2 Results", overtime_type2, idle_time_type2, number_Patients2)

def schedule_mix(queue_Type1, queue_Type2):
    queue_both = deque()
    
    machine1_scheduled = datetime(2023, 8, 2, 8, 0)
    machine2_scheduled = datetime(2023, 8, 2, 8, 0)

    while queue_Type1 or queue_Type2:
        if(queue_Type1[0].call_time.date() <= queueType2[0].call_time.date()):
            current_Patient = queue_type1.popleft()
            if machine1_scheduled.date() <= machine2.scheduled.date():
                if machine1_scheduled + timedelta(minutes=30) >= datetime(2023, machine1_scheduled.month, machine1_scheduled.day, 17, 0) or (machine1_scheduled.day <= current_Patient.call_time.day and machine1_scheduled.month <= current_Patient.call_time.month):
                    if machine1_scheduled.day < 31 and machine1_scheduled.month == 8:
                        machine1_scheduled = datetime(2023, 8, machine1_scheduled.day + 1, 8, 0)
                    elif machine1_scheduled.day == 31:
                        machine1_scheduled = datetime(2023, 9, 1, 8, 0)
                    else:
                        machine1_scheduled = datetime(2023, 9, machine1_scheduled.day+1, 8, 0)
                else:
                    machine1_scheduled += timedelta(minutes=30)
            else:
                if machine2_scheduled + timedelta(minutes=30) >= datetime(2023, machine2_scheduled.month, machine2_scheduled.day, 17, 0) or (machine2_scheduled.day <= current_Patient.call_time.day and machine2_scheduled.month <= current_Patient.call_time.month):
                    if machine2_scheduled.day < 31 and machine1_scheduled.month == 8:
                        machine2_scheduled = datetime(2023, 8, machine2_scheduled.day + 1, 8, 0)
                    elif machine2_scheduled.day == 31:
                        machine2_scheduled = datetime(2023, 9, 1, 8, 0)
                    else:
                        machine2_scheduled = datetime(2023, 9, machine2_scheduled.day+1, 8, 0)
                else:
                    machine2_scheduled += timedelta(minutes=30)
        else:
            current_Patient = queue_type2.popleft()
            if machine1_scheduled.date() <= machine2.scheduled.date():
                if machine1_scheduled + timedelta(minutes=40) >= datetime(2023, machine1_scheduled.month, machine1_scheduled.day, 17, 0) or (machine1_scheduled.day <= current_Patient.call_time.day and machine1_scheduled.month <= current_Patient.call_time.month):
                    if machine1_scheduled.day < 31 and machine1_scheduled.month == 8:
                        machine1_scheduled = datetime(2023, 8, machine1_scheduled.day + 1, 8, 0)
                    elif machine1_scheduled.day == 31:
                        machine1_scheduled = datetime(2023, 9, 1, 8, 0)
                    else:
                        machine1_scheduled = datetime(2023, 9, machine1_scheduled.day+1, 8, 0)
                else:
                    machine1_scheduled += timedelta(minutes=40)
            else:
                if machine2_scheduled + timedelta(minutes=40) >= datetime(2023, machine2_scheduled.month, machine2_scheduled.day, 17, 0) or (machine2_scheduled.day <= current_Patient.call_time.day and machine2_scheduled.month <= current_Patient.call_time.month):
                    if machine2_scheduled.day < 31 and machine1_scheduled.month == 8:
                        machine2_scheduled = datetime(2023, 8, machine2_scheduled.day + 1, 8, 0)
                    elif machine2_scheduled.day == 31:
                        machine2_scheduled = datetime(2023, 9, 1, 8, 0)
                    else:
                        machine2_scheduled = datetime(2023, 9, machine2_scheduled.day+1, 8, 0)
                else:
                    machine2_scheduled += timedelta(minutes=40)


def calculate_overtime_and_idle_time(queue):
    overtime = []
    idle_time = []
    number_Patients = []
    waiting_times = []

    while queue:
        time_p = queue[0].scheduled_time
        idle = timedelta()
        numPatients = 0
        
        while queue and queue[0].scheduled_time.date() == time_p.date():
            current_patient = queue.popleft()
            numPatients += 1
            duration_patient = current_patient.duration
            scheduled_time = current_patient.scheduled_time

            if scheduled_time <= time_p:
                waiting_times.append(time_p - scheduled_time)
                time_p += timedelta(minutes=duration_patient)
            else:
                waiting_times.append(timedelta())
                idle += scheduled_time - time_p
                time_p = scheduled_time + timedelta(minutes=duration_patient)

        overtime.append(max(0,(time_p.hour - 17)*60 + time_p.minute))
        idle_time.append(idle.total_seconds() / 60)
        number_Patients.append(numPatients)

    return overtime, idle_time, number_Patients, waiting_times

def print_overtime_and_idle_time(sheet_name, overtime, idle_time, number_Patients):
    # Load existing data from Excel
    existing_file_path = "C:\\Users\\mabe6\\OneDrive\\Desktop\\Python Programming\\PatientData.xlsx"
    df_existing = pd.read_excel(existing_file_path)

    results = pd.DataFrame({
        'Date': pd.date_range(start='2023-08-02', periods=len(overtime)),
        'Overtime': overtime,
        'Idle Time': idle_time,
        'Number of Patients': number_Patients,
    })

    # Append the new sheet to the existing Excel file
    with pd.ExcelWriter(existing_file_path, engine='openpyxl', mode='a') as writer:
        results.to_excel(writer, sheet_name=sheet_name, index=False)

main()
