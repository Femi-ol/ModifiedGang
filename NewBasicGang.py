

import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('Agg')  # Prevents the plot from displaying
from typing import List, Tuple, Dict
from collections import deque

def calculate_gang_metrics(processes: List[int], gangs: List[List[int]], response_time: Dict[int, int], waiting_time: List[int], finish_time: Dict[int, int]) -> Dict[str, List[float]]:
    proc_index = {p: i for i, p in enumerate(processes)}
    gang_response_times, gang_turnaround_times, gang_waiting_times = [], [], []

    for gang in gangs:
        g_res = min(response_time[p] for p in gang)
        g_tat = max(finish_time[p] for p in gang)
        g_wait = sum(waiting_time[proc_index[p]] for p in gang) / len(gang)
        gang_response_times.append(g_res)
        gang_turnaround_times.append(g_tat)
        gang_waiting_times.append(g_wait)

    return {
        "gang_response_times": gang_response_times,
        "gang_turnaround_times": gang_turnaround_times,
        "gang_waiting_times": gang_waiting_times
    }

def write_metrics_to_file(filename: str, metrics: Dict[str, List[float]]):
    with open(filename, 'a') as f:
        f.write("\nMetrics:\n")
        for k, v in metrics.items():
            f.write(f"{k.replace('_', ' ').title()}: {v}\n")

def generate_gantt_chart_gang_scheduling(processes: List[int], burst_times: List[List[int]], quantum: int, num_cores: int, gangs: List[List[int]]) -> List[Tuple[int,int,int,str,int]]:
    fig, ax = plt.subplots()
    n = len(processes)
    current_time = [0] * num_cores
    schedule = []
    rem_burst_times = [burst[:] for burst in burst_times]
    burst_tracker = [0] * n
    global_time = 0

    gang_queue = deque(gangs)
    active_cores = [None] * num_cores

    while any(sum(rem_burst_times[i]) > 0 for i in range(n)):
        active_gangs = []
        while gang_queue and len(active_gangs) * len(gangs[0]) < num_cores:
            gang = gang_queue.popleft()
            if len(gang) <= active_cores.count(None):
                active_gangs.append(gang)
                for proc in gang:
                    core = active_cores.index(None)
                    active_cores[core] = proc
                    current_time[core] = max(current_time[core], global_time)

        time_spent = [0] * num_cores

        for core, proc in enumerate(active_cores):
            if proc is None:
                continue
            while burst_tracker[proc] < len(rem_burst_times[proc]) and time_spent[core] < quantum:
                b_type = 'CPU' if burst_tracker[proc] % 2 == 0 else 'IO'
                remaining = rem_burst_times[proc][burst_tracker[proc]]
                time_left = quantum - time_spent[core]
                duration = min(remaining, time_left)

                schedule.append((proc, duration, current_time[core], b_type, core))
                current_time[core] += duration
                time_spent[core] += duration
                rem_burst_times[proc][burst_tracker[proc]] -= duration

                if rem_burst_times[proc][burst_tracker[proc]] == 0:
                    burst_tracker[proc] += 1
                if time_spent[core] >= quantum:
                    break
            if burst_tracker[proc] == len(rem_burst_times[proc]):
                active_cores[core] = None

        for gang in active_gangs:
            if any(sum(rem_burst_times[p]) > 0 for p in gang):
                gang_queue.append(gang)
                for p in gang:
                    if p in active_cores:
                        active_cores[active_cores.index(p)] = None

        global_time = max(current_time)

    max_time = max(start + dur for (_, dur, start, _, _) in schedule)
    ax.clear()
    for (proc, burst, start, b_type, core) in schedule:
        color = 'skyblue' if b_type == 'CPU' else 'lightcoral'
        ax.barh(proc, burst, left=start, color=color, edgecolor='black')
        ax.text(start + burst / 2, proc + core * (n + 1), f'P{proc} (C{core})', ha='center', va='center', color='white')

    ax.set(xlabel='Time', ylabel='Processes',
           title='Gang Scheduling on Multiple Cores',
           xlim=(0, max_time),
           ylim=(0, len(processes) * (num_cores + 1)))
    ax.set_yticks(range(len(processes)))
    ax.set_yticklabels([f'P{p}' for p in processes])

    # ax.set_yticks([i + c * (n + 1) for c in range(num_cores) for i in range(n)])
    # ax.set_yticklabels([f'P{p}' for c in range(num_cores) for p in processes])
    ax.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

    return schedule



def run_simulation(processes, burst_times, quantum, num_cores, gangs):
    schedule = generate_gantt_chart_gang_scheduling(processes, burst_times, quantum, num_cores, gangs)

    print(f"Get started")

    finish_time = {}
    for (proc, duration, start, b_type, core) in schedule:
        end_time = start + duration
        if proc not in finish_time or end_time > finish_time[proc]:
            finish_time[proc] = end_time

    turnaround_time = [finish_time[p] for p in processes]
    total_cpu_burst = [sum(burst_times[i]) for i in range(len(processes))]
    waiting_time = [turnaround_time[i] - total_cpu_burst[i] for i in range(len(processes))]

    response_time = {}
    for p in processes:
        cpu_starts = [start for (proc, dur, start, b_type, core) in schedule if proc == p and b_type == 'CPU']
        response_time[p] = min(cpu_starts) if cpu_starts else 0
    response_time_list = [response_time[p] for p in processes]

    gang_metrics = calculate_gang_metrics(processes, gangs, response_time, waiting_time, finish_time)

    total_time = max(finish_time.values()) if finish_time else 0
    core_busy_times = [0] * num_cores
    for (_, dur, _, b_type, c) in schedule:
        if b_type == 'CPU':
            core_busy_times[c] += dur

    core_utilization = [(ct / total_time) * 100 if total_time > 0 else 0 for ct in core_busy_times]
    system_throughput = len(processes) / total_time if total_time > 0 else 0

    print("Processes Burst times Waiting time Turn around time")
    for i in range(len(processes)):
        print(f" {processes[i]} \t {burst_times[i]} \t {waiting_time[i]} \t {turnaround_time[i]}")

    print(f"Average waiting time = {sum(waiting_time) / len(processes):.2f}")
    print(f"Average turn around time = {sum(turnaround_time) / len(processes):.2f}")
    print(f"Core Utilization: {core_utilization}")
    print(f"System Throughput: {system_throughput:.2f} processes/unit time")
    print(f"Response Time: {response_time_list}")
    print(f"Gang Response Times: {gang_metrics['gang_response_times']}")
    print(f"Gang Turnaround Times: {gang_metrics['gang_turnaround_times']}")
    print(f"Gang Waiting Times: {gang_metrics['gang_waiting_times']}")

    metrics = {
        "core_utilization": core_utilization,
        "system_throughput": system_throughput,
        "response_time": response_time_list,
        "gang_response_times": gang_metrics["gang_response_times"],
        "gang_turnaround_times": gang_metrics["gang_turnaround_times"],
        "gang_waiting_times": gang_metrics["gang_waiting_times"]
    }

    write_metrics_to_file('metrics.txt', metrics)
    print(f"Gang Response Times: {gang_metrics['gang_response_times']}")
    print(f"Gang Turnaround Times: {gang_metrics['gang_turnaround_times']}")
    print(f"Gang Waiting Times: {gang_metrics['gang_waiting_times']}")

if __name__ == "__main__":
    processes =  [
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236
]
    gangs =  [
[0, 1, 2, 3], [4], [5, 6, 7, 8], [9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23], [24, 25], [26, 27, 28], [29, 30], [31, 32, 33], [34], [35, 36, 37, 38], [39, 40], [41, 42], [43, 44, 45, 46], [47, 48], [49, 50, 51, 52], [53], [54, 55, 56, 57], [58, 59, 60, 61], [62, 63], [64, 65, 66], [67, 68, 69], [70, 71, 72, 73], [74, 75], [76, 77, 78], [79, 80, 81], [82, 83, 84, 85], [86], [87, 88, 89, 90], [91, 92], [93, 94], [95], [96], [97, 98, 99], [100, 101, 102, 103], [104, 105, 106], [107], [108], [109, 110, 111], [112, 113, 114, 115], [116, 117], [118, 119], [120, 121], [122, 123, 124, 125], [126, 127, 128, 129], [130, 131, 132], [133], [134, 135, 136], [137, 138, 139, 140], [141, 142, 143], [144, 145], [146, 147, 148], [149, 150, 151], [152, 153, 154], [155, 156, 157], [158, 159, 160, 161], [162, 163], [164, 165, 166], [167], [168], [169], [170, 171], [172, 173], [174, 175], [176], [177, 178, 179, 180], [181], [182], [183, 184, 185], [186, 187, 188], [189, 190, 191], [192, 193, 194], [195, 196], [197, 198, 199, 200], [201], [202, 203], [204, 205], [206, 207, 208], [209, 210, 211, 212], [213, 214], [215, 216], [217], [218, 219, 220], [221], [222, 223, 224], [225], [226, 227], [228, 229], [230], [231, 232], [233, 234, 235, 236]
]
    burst_times =  [
[20, 5, 29, 58, 22, 36, 19], [39, 10, 53, 33, 10], [32, 25, 27, 49, 26], [33, 4, 22, 16, 24], [23, 21, 26], [28, 3, 29, 1, 7, 5, 11], [30, 12, 34, 63, 46], [26, 14, 18, 1, 26], [49, 5, 23], [32, 7, 28, 4, 42], [47, 1, 24, 5, 36], [22, 10, 37, 10, 44], [6, 27, 30], [27, 20, 24], [16, 9, 5, 41, 38], [25, 10, 16], [42, 55, 25, 80, 24, 41, 38], [28, 45, 33, 32, 41, 10, 35], [33, 1, 50, 23, 3, 43, 22], [33, 13, 4, 27, 26, 1, 29], [32, 65, 25, 11, 25], [28, 2, 47, 8, 26, 20, 39], [42, 31, 16, 20, 33], [17, 36, 27, 4, 9], [28, 18, 32], [19, 61, 25], [22, 40, 15], [34, 189, 39, 5, 27], [25, 6, 13, 12, 14], [10, 5, 13, 7, 26], [25, 13, 30, 22, 24], [26, 17, 11], [18, 5, 27, 20, 41], [13, 44, 19, 7, 40], [25, 36, 40], [15, 20, 47, 1, 24, 5, 37], [24, 14, 47, 18, 32], [18, 12, 36], [51, 2, 32, 14, 36], [21, 11, 26, 27, 32], [29, 15, 48, 8, 47], [26, 26, 39], [44, 3, 46], [11, 6, 39, 204, 29, 8, 52], [35, 25, 39, 6, 25, 132, 38], [27, 26, 16], [19, 2, 9, 1, 19], [44, 87, 28], [25, 14, 31], [40, 23, 32, 3, 32], [36, 23, 23], [7, 8, 38], [20, 19, 38, 131, 26], [43, 17, 31, 5, 28, 79, 27], [20, 48, 21], [34, 14, 40, 2, 30], [39, 16, 25, 70, 33, 17, 18], [6, 19, 28, 4, 19, 15, 32], [22, 18, 39], [27, 49, 24, 12, 33], [33, 3, 33, 5, 20, 19, 34], [36, 39, 19], [31, 133, 22, 15, 39, 2, 21], [30, 23, 35, 37, 9, 13, 23], [29, 1, 28], [30, 93, 28], [31, 1, 44, 7, 38], [30, 20, 46], [24, 8, 37, 4, 28], [13, 26, 21, 5, 46], [60, 27, 10, 13, 36], [15, 18, 41], [28, 9, 34, 4, 20, 12, 8], [33, 4, 26, 4, 31, 4, 33], [32, 2, 45], [25, 20, 24], [18, 9, 38, 3, 22, 3, 36], [32, 12, 40], [21, 1, 29], [35, 45, 36, 47, 37, 1, 15], [9, 1, 21, 28, 25], [25, 8, 26], [21, 17, 23], [9, 1, 18, 1, 37], [42, 23, 31, 37, 36, 1, 30], [30, 22, 30, 51, 33], [37, 43, 34, 22, 37, 47, 38], [36, 1, 38], [52, 1, 28], [11, 39, 46, 35, 27, 7, 29], [29, 22, 28], [22, 7, 18, 10, 18, 16, 35], [19, 33, 47, 60, 24, 1, 33], [40, 1, 29, 23, 31, 21, 29], [30, 28, 20], [26, 18, 13], [42, 18, 34], [35, 11, 28, 32, 32], [34, 28, 44], [18, 113, 14], [37, 12, 30], [33, 43, 45, 24, 47, 12, 5], [41, 12, 28, 14, 34], [32, 8, 19], [35, 33, 56, 2, 34], [28, 6, 22, 5, 44, 2, 40], [35, 4, 34], [45, 19, 21], [16, 5, 31, 45, 37], [26, 14, 29], [14, 1, 36], [26, 7, 29, 33, 28, 21, 33], [29, 22, 26], [39, 41, 25, 51, 17], [26, 9, 26], [30, 29, 19], [34, 1, 36], [32, 32, 42, 8, 36, 4, 44], [39, 38, 4, 54, 33, 7, 50], [36, 13, 28, 20, 36], [46, 116, 44, 12, 25, 35, 32], [16, 29, 42], [40, 14, 24, 26, 29], [34, 4, 43, 23, 22, 76, 29], [28, 1, 38], [24, 33, 23], [34, 2, 46, 1, 34], [45, 1, 25, 22, 40], [13, 6, 42, 44, 39], [32, 30, 16, 9, 23, 39, 50], [12, 21, 33, 36, 20], [46, 84, 26, 13, 40], [28, 19, 38, 3, 33, 11, 29], [15, 28, 37], [23, 1, 32], [29, 104, 29, 18, 19, 9, 27], [35, 5, 32, 21, 31, 31, 33], [18, 13, 23, 77, 17], [34, 17, 28], [23, 54, 31, 8, 35], [30, 73, 7, 10, 27], [42, 9, 50, 6, 28, 28, 24], [20, 14, 24], [48, 1, 23], [48, 7, 47, 22, 36], [53, 19, 25, 1, 31], [19, 47, 28, 67, 29], [55, 8, 17], [40, 20, 19, 4, 46], [42, 15, 21, 3, 50, 33, 22], [27, 34, 32, 1, 39, 17, 40], [20, 7, 37, 12, 27], [23, 23, 21], [27, 14, 41, 9, 47], [21, 14, 20, 1, 7, 20, 35], [23, 36, 42, 17, 33, 5, 33], [31, 68, 36], [38, 2, 18, 16, 16, 26, 14], [37, 29, 35, 1, 30], [39, 25, 42], [27, 3, 28, 32, 18], [32, 33, 33, 1, 28, 12, 18], [12, 26, 7, 25, 39, 9, 22], [41, 1, 20], [33, 16, 34], [14, 22, 26], [31, 32, 35, 40, 20], [23, 1, 29], [28, 18, 15], [22, 62, 27, 11, 46], [37, 15, 33], [36, 40, 19, 9, 14, 9, 13], [29, 18, 43], [43, 1, 40], [40, 3, 17, 5, 22], [3, 23, 21], [29, 1, 28], [16, 11, 23, 24, 26], [34, 25, 36, 11, 13, 10, 18], [27, 4, 33, 13, 22, 16, 27], [23, 4, 27, 42, 39], [37, 3, 42, 26, 31], [48, 3, 30], [41, 11, 36], [17, 1, 28, 15, 23, 9, 22], [15, 7, 38, 6, 33, 14, 35], [7, 1, 26, 61, 30, 19, 26], [30, 47, 25, 16, 36, 48, 24], [21, 19, 15, 8, 12, 7, 46], [31, 4, 39, 42, 46, 23, 30], [42, 4, 33, 11, 39, 3, 25], [30, 18, 16, 7, 23], [21, 9, 41, 51, 30], [21, 1, 17, 22, 44, 16, 31], [35, 46, 20, 1, 16], [44, 31, 24], [31, 10, 21], [33, 4, 30], [24, 1, 22, 19, 43, 18, 32], [23, 7, 25], [45, 5, 33, 7, 15, 6, 37], [24, 1, 17, 56, 21], [26, 27, 24, 21, 29, 2, 46], [28, 25, 11], [42, 70, 13, 13, 24, 12, 14], [31, 25, 21, 3, 21], [20, 7, 25, 4, 19], [29, 1, 20], [10, 34, 8, 14, 15, 1, 33], [34, 21, 48], [42, 63, 29, 18, 30, 14, 26], [35, 2, 45, 9, 25], [38, 18, 36, 64, 25, 26, 32], [26, 1, 39, 17, 33], [41, 35, 33], [23, 14, 30], [22, 6, 29, 1, 31, 1, 25], [16, 2, 15], [33, 4, 28, 27, 38], [44, 26, 14], [31, 2, 24, 34, 25], [18, 33, 26], [49, 7, 33, 59, 42], [43, 49, 46], [44, 2, 24, 3, 27], [20, 29, 32], [23, 17, 29, 13, 41], [23, 3, 22, 4, 23, 7, 38], [25, 13, 13, 15, 38, 29, 35], [4, 1, 4, 1, 33, 12, 38], [37, 26, 33], [20, 3, 29], [29, 11, 38, 11, 22], [33, 2, 37, 8, 14], [26, 33, 30, 60, 33], [32, 10, 17, 3, 27, 6, 37], [29, 11, 9]
]
    
    quantum = 40
    num_cores = 64
    # quantum = 4
    # num_cores = 4

    
    run_simulation(processes, burst_times, quantum, num_cores, gangs)

