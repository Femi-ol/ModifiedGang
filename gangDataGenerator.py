

import numpy as np
import pandas as pd

# Function to generate gang scheduling data with a fixed number of gangs
def generate_gang_data(num_gangs):
    # Fixed number of jobs per gang (or randomize if needed)
    gang_jobs = [np.random.randint(1, 5) for _ in range(num_gangs)]

    # Generate random odd numbers of bursts for each job (between 3 and 7)
    gang_bursts = [[np.random.choice([3, 5, 7]) for _ in range(jobs)] for jobs in gang_jobs]

    # Function to generate alternating execution and I/O bursts
    def generate_bursts(n):
        bursts = []
        for i in range(n):
            if i % 2 == 0:  # Even index -> Execution Time
                bursts.append(int( max(1, abs(np.random.normal(loc=30, scale=10))) ) )  # Rounded to whole numbers
            else:  # Odd index -> I/O Time
                bursts.append(int( max(1,np.random.exponential(scale=20) ) ))  # Rounded to whole numbers
        return bursts

    # Create gangs, processes, and burst times
    processes = []
    burst_times = []
    gangs = []

    process_id = 0
    for gang_id, (num_jobs, bursts_per_job) in enumerate(zip(gang_jobs, gang_bursts)):
        gang = []
        for bursts_count in bursts_per_job:
            bursts = generate_bursts(bursts_count)
            processes.append(process_id)
            burst_times.append(bursts)
            gang.append(process_id)
            process_id += 1
        gangs.append(gang)

    # Convert to structured dictionary format
    output_data = {
        "processes": processes,
        "burst_times": burst_times,
        "gangs": gangs
    }

    # Print a summary
    print(f"\nGenerated {num_gangs} gangs with a total of {len(processes)} jobs.")
    df = pd.DataFrame({"Process": processes, "Burst Times": burst_times})
    # print(df.head())  # Display first few rows


    print("\n processes = ", processes)
    print("\n gangs = ", gangs)
    print("\n burst_times = ", burst_times)

    return output_data

# Run for different gang sizes
for num_gangs in [63, 83, 93]:
    generate_gang_data(num_gangs)
