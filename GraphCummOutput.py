# import matplotlib.pyplot as plt



import matplotlib.pyplot as plt
import numpy as np

# Labels
categories = [
    "Avg Core Utilization", 
    "System Throughput", 
    "Avg Gang Response Time", 
    "Avg Gang Turnaround Time", 
    "Avg Gang Waiting Time"
]

# Values
basic_vals    = [43.58, 0.22, 91.11, 726.93, 482.75]
modified_vals = [47.88, 0.27, 91.11, 710.63, 443.95]
ml_vals       = [43.89, 0.23, 91.11, 725.69, 472.88]

# Positioning
x = np.arange(len(categories))
width = 0.25

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width, basic_vals, width, label='Basic')
bars2 = ax.bar(x, modified_vals, width, label='Modified')
bars3 = ax.bar(x + width, ml_vals, width, label='ML-Modified')

# Labels
ax.set_ylabel('Value')
ax.set_title('Gang Scheduling Metrics Comparison')
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=15)
ax.legend()

# Value labels
def label_bars(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom')

label_bars(bars1)
label_bars(bars2)
label_bars(bars3)

plt.tight_layout()
plt.show()


# # ------------------------------------------------------------------------
# # 1) Example: Three Runs for Each Approach (63, 83, 93 Gangs or whatever)
# # ------------------------------------------------------------------------
# # For demonstration, I'm inventing some numbers. You should replace them with 
# # the actual results you collected from your 3 runs (63, 83, 93).
# # Each approach has 3 runs. We'll average them.

# # ===== BASIC GANG =====
# basic_core_util_runs = [
#     [70.65727699530517, 65.61032863849765, 68.30985915492957, 57.159624413145536, 68.54460093896714, 63.732394366197184, 52.69953051643193, 57.3943661971831, 72.41784037558685, 61.267605633802816, 63.14553990610329, 61.267605633802816, 71.12676056338029, 72.53521126760563, 66.54929577464789, 67.25352112676056, 68.7793427230047, 66.54929577464789, 73.12206572769952, 69.24882629107981, 69.01408450704226, 65.49295774647888, 73.00469483568075, 58.333333333333336, 71.12676056338029, 69.36619718309859, 62.08920187793427, 65.84507042253522, 69.71830985915493, 74.29577464788733, 70.4225352112676, 69.36619718309859, 58.21596244131455, 65.72769953051643, 68.42723004694837, 68.89671361502347, 59.38967136150235, 69.13145539906104, 59.154929577464785, 68.07511737089203, 49.88262910798122, 38.028169014084504, 22.300469483568076, 20.422535211267608, 0.35211267605633806, 4.577464788732395, 1.643192488262911, 0.0, 0.4694835680751174, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],   # run1 (e.g., 63 gangs)
#     [73.30275229357798, 71.55963302752293, 71.19266055045873, 64.95412844036697, 70.8256880733945, 72.8440366972477, 72.11009174311927, 73.30275229357798, 75.68807339449542, 67.52293577981652, 66.05504587155964, 60.27522935779817, 70.18348623853211, 76.14678899082568, 69.81651376146789, 71.37614678899082, 65.68807339449542, 62.018348623853214, 72.01834862385321, 77.70642201834862, 66.5137614678899, 65.41284403669725, 64.6788990825688, 74.86238532110092, 69.1743119266055, 70.73394495412843, 63.853211009174316, 71.46788990825688, 70.09174311926606, 76.23853211009174, 67.06422018348623, 61.65137614678899, 69.35779816513762, 65.5045871559633, 63.76146788990825, 61.00917431192661, 74.40366972477064, 71.28440366972477, 63.76146788990825, 46.055045871559635, 50.36697247706422, 46.788990825688074, 28.899082568807337, 23.119266055045873, 29.541284403669728, 15.045871559633028, 14.495412844036698, 14.403669724770642, 3.577981651376147, 6.055045871559633, 7.339449541284404, 3.211009174311927, 0.0, 0.0, 1.1009174311926606, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# ,   # run2 (e.g., 83 gangs)
#     [69.79166666666666, 71.97916666666667, 64.0625, 77.8125, 77.5, 68.64583333333333, 58.64583333333333, 69.89583333333333, 68.54166666666667, 68.125, 73.33333333333333, 58.229166666666664, 71.14583333333333, 76.35416666666667, 63.74999999999999, 69.16666666666667, 66.77083333333333, 70.9375, 66.66666666666666, 65.0, 60.62499999999999, 69.79166666666666, 70.10416666666667, 64.375, 66.5625, 67.8125, 76.66666666666667, 73.75, 50.625, 59.895833333333336, 72.91666666666666, 73.95833333333334, 63.22916666666667, 65.3125, 76.35416666666667, 60.3125, 66.45833333333333, 66.35416666666667, 70.0, 65.83333333333333, 66.77083333333333, 59.583333333333336, 61.5625, 62.81250000000001, 73.22916666666667, 63.645833333333336, 61.875, 75.0, 64.6875, 61.979166666666664, 73.4375, 56.25, 65.0, 47.91666666666667, 42.291666666666664, 25.937500000000004, 33.229166666666664, 15.0, 15.937499999999998, 10.0, 4.166666666666666, 3.854166666666667, 0.0, 0.0]
# ,   # run3 (e.g., 93 gangs)
# ]
# basic_throughput_runs = [0.19, 0.11, 0.25]
# basic_gang_response_runs = [
#     [0, 4, 8],  # run1
#     [0, 4, 9],  # run2
#     [0, 4, 8],  # run3
# ]
# basic_gang_turnaround_runs = [
#     [737, 740, 785, 619, 515, 332, 495, 485, 751, 754, 740, 737, 730, 358, 514, 504, 614, 664, 666, 651, 659, 668, 676, 662, 673, 760, 532, 560, 387, 731, 557, 748, 542, 724, 662, 852, 768, 801, 408, 710, 778, 692, 796, 692, 804, 788, 687, 587, 789, 574, 693, 791, 312, 701, 705, 776, 781, 772, 761, 722, 723, 797, 633]
# ,
#     [1012, 945, 237, 927, 805, 1062, 819, 438, 943, 839, 938, 1041, 1090, 995, 644, 665, 807, 971, 982, 869, 1055, 1043, 456, 468, 1065, 1046, 1067, 963, 641, 968, 488, 681, 876, 847, 510, 681, 857, 977, 712, 1057, 970, 868, 964, 545, 1044, 881, 1022, 705, 1079, 1082, 329, 749, 884, 531, 899, 757, 1027, 1023, 728, 1022, 884, 728, 1045, 1024, 1033, 727, 800, 786, 772, 1018, 1069, 949, 947, 773, 1009, 1021, 937, 771, 1039, 946, 937, 791, 1027]
# ,
#     [685, 803, 818, 912, 811, 908, 385, 814, 803, 389, 718, 705, 558, 814, 804, 538, 539, 874, 582, 850, 758, 757, 843, 848, 875, 748, 943, 755, 878, 753, 563, 738, 586, 853, 723, 592, 875, 433, 876, 586, 844, 740, 637, 619, 760, 852, 756, 884, 791, 629, 866, 778, 944, 843, 629, 629, 866, 879, 873, 634, 849, 923, 780, 468, 904, 921, 896, 669, 908, 498, 882, 771, 509, 899, 960, 912, 949, 649, 944, 345, 896, 815, 909, 899, 911, 881, 802, 701, 885, 820, 810, 931, 709]
# ,
# ]
# basic_gang_waiting_runs = [
#     [370.0, 466.6666666666667, 466.6666666666667, 380.0, 270.0, 240.0, 320.0, 360.0, 426.6666666666667, 330.0, 333.3333333333333, 440.0, 390.0, 240.0, 360.0, 360.0, 346.6666666666667, 480.0, 373.3333333333333, 320.0, 346.6666666666667, 480.0, 480.0, 413.3333333333333, 453.3333333333333, 520.0, 320.0, 360.0, 280.0, 400.0, 400.0, 470.0, 280.0, 460.0, 370.0, 560.0, 560.0, 520.0, 320.0, 480.0, 440.0, 386.6666666666667, 460.0, 480.0, 480.0, 470.0, 520.0, 440.0, 430.0, 440.0, 500.0, 453.3333333333333, 240.0, 520.0, 440.0, 530.0, 540.0, 520.0, 520.0, 386.6666666666667, 506.6666666666667, 540.0, 420.0]
# ,
#     [570.0, 720.0, 160.0, 540.0, 640.0, 560.0, 586.6666666666666, 320.0, 453.3333333333333, 586.6666666666666, 453.3333333333333, 653.3333333333334, 660.0, 640.0, 520.0, 520.0, 500.0, 640.0, 500.0, 466.6666666666667, 690.0, 666.6666666666666, 360.0, 360.0, 510.0, 740.0, 640.0, 470.0, 520.0, 706.6666666666666, 400.0, 400.0, 586.6666666666666, 540.0, 400.0, 560.0, 620.0, 666.6666666666666, 560.0, 746.6666666666666, 560.0, 680.0, 613.3333333333334, 440.0, 706.6666666666666, 640.0, 773.3333333333334, 560.0, 640.0, 660.0, 280.0, 600.0, 580.0, 440.0, 586.6666666666666, 440.0, 760.0, 640.0, 440.0, 710.0, 640.0, 600.0, 706.6666666666666, 670.0, 693.3333333333334, 460.0, 600.0, 640.0, 640.0, 640.0, 740.0, 720.0, 660.0, 586.6666666666666, 700.0, 670.0, 760.0, 500.0, 780.0, 680.0, 680.0, 580.0, 660.0]
# ,
#     [333.3333333333333, 500.0, 460.0, 460.0, 420.0, 380.0, 280.0, 360.0, 600.0, 280.0, 386.6666666666667, 440.0, 400.0, 546.6666666666666, 600.0, 340.0, 400.0, 440.0, 440.0, 520.0, 386.6666666666667, 500.0, 640.0, 640.0, 480.0, 440.0, 613.3333333333334, 500.0, 520.0, 500.0, 270.0, 470.0, 440.0, 613.3333333333334, 500.0, 440.0, 520.0, 320.0, 540.0, 380.0, 400.0, 520.0, 340.0, 400.0, 520.0, 600.0, 520.0, 453.3333333333333, 570.0, 440.0, 620.0, 540.0, 506.6666666666667, 580.0, 400.0, 480.0, 640.0, 573.3333333333334, 640.0, 420.0, 500.0, 570.0, 440.0, 360.0, 573.3333333333334, 480.0, 640.0, 440.0, 533.3333333333334, 400.0, 550.0, 600.0, 400.0, 506.6666666666667, 640.0, 493.3333333333333, 493.3333333333333, 520.0, 500.0, 280.0, 600.0, 520.0, 613.3333333333334, 600.0, 620.0, 600.0, 533.3333333333334, 560.0, 653.3333333333334, 600.0, 600.0, 680.0, 560.0]
# ,
# ]

# # ===== MODIFIED GANG =====
# modified_core_util_runs = [
#     [50.0, 50.0, 52.3, 60.4],
#     [48.9, 51.2, 53.1, 59.8],
#     [49.5, 49.7, 52.9, 60.7],
# ]
# modified_throughput_runs = [0.14, 0.15, 0.13]
# modified_gang_response_runs = [
#     [0, 4, 8],
#     [0, 4, 8],
#     [0, 4, 8],
# ]
# modified_gang_turnaround_runs = [
#     [86, 67, 82],
#     [88, 70, 80],
#     [85, 66, 81],
# ]
# modified_gang_waiting_runs = [
#     [29.25, 34.0, 30.75],
#     [30.0, 35.0, 29.0],
#     [28.5, 33.0, 31.0],
# ]

# # ===== MODIFIED GANG ML ===== (the new approach you want to add)
# # Provide your actual data from 63, 83, 93 runs
# ml_core_util_runs = [
#     [55.0, 55.0, 56.0, 65.0],
#     [54.1, 54.3, 57.0, 64.8],
#     [55.2, 54.8, 55.9, 65.5],
# ]
# ml_throughput_runs = [0.16, 0.15, 0.17]
# ml_gang_response_runs = [
#     [0, 4, 8],
#     [0, 4, 8],
#     [0, 4, 8],
# ]
# ml_gang_turnaround_runs = [
#     [80, 60, 75],
#     [78, 62, 74],
#     [81, 59, 76],
# ]
# ml_gang_waiting_runs = [
#     [25.5, 28.0, 26.5],
#     [26.0, 29.0, 27.0],
#     [25.0, 27.0, 28.5],
# ]


# # ----------------------------------------------------------------------------------
# # 2) Helper functions to average the runs for each approach
# # ----------------------------------------------------------------------------------

# def average_list_of_lists(list_of_lists):
#     """
#     Given something like [[1,2,3],[4,5,6],[7,8,9]],
#     returns the elementwise average => [ (1+4+7)/3, (2+5+8)/3, (3+6+9)/3 ].
#     """
#     if not list_of_lists:
#         return []
#     length = len(list_of_lists[0])
#     sums = [0]*length
#     count = len(list_of_lists)
#     for run in list_of_lists:
#         for i in range(length):
#             sums[i] += run[i]
#     return [s/count for s in sums]

# def average_scalar_list(vals):
#     """Simple average for a list of scalars, e.g. [0.09, 0.11, 0.10]."""
#     if not vals:
#         return 0
#     return sum(vals)/len(vals)

# # average 2D array for "Gang metrics" (like [ [0,4,8], [0,4,9], [0,4,8] ])
# # typically each run might have the same number of gangs. We'll do elementwise average:
# def average_gang_runs(runs):
#     """
#     runs: list of lists, e.g. [[0,4,8],[0,4,9],[0,4,8]]
#     returns a single list for the average: [0,4,8.333...]
#     """
#     return average_list_of_lists(runs)


# # ----------------------------------------------------------------------
# # 3) Compute Averages for each Approach (Basic, Modified, Modified ML)
# # ----------------------------------------------------------------------

# # A) Core Utilization: let's do an overall average (not core by core),
# #    or you might do elementwise average if you prefer.
# #    *If you want a single "avg utilization" number, do:
# def overall_avg_utilization(core_util_runs):
#     # each run is a list of core utilizations => average across cores, then average across runs
#     per_run_avgs = []
#     for run in core_util_runs:
#         # average for that run across all cores
#         per_run_avgs.append( sum(run)/len(run) )
#     # now average those run-averages
#     return sum(per_run_avgs)/len(per_run_avgs)


# # ---- BASIC ----
# basic_avg_core_util = overall_avg_utilization(basic_core_util_runs)
# basic_avg_throughput = average_scalar_list(basic_throughput_runs)
# basic_avg_gang_response = average_gang_runs(basic_gang_response_runs)
# basic_avg_gang_turnaround = average_gang_runs(basic_gang_turnaround_runs)
# basic_avg_gang_waiting = average_gang_runs(basic_gang_waiting_runs)

# # ---- MODIFIED ----
# modified_avg_core_util = overall_avg_utilization(modified_core_util_runs)
# modified_avg_throughput = average_scalar_list(modified_throughput_runs)
# modified_avg_gang_response = average_gang_runs(modified_gang_response_runs)
# modified_avg_gang_turnaround = average_gang_runs(modified_gang_turnaround_runs)
# modified_avg_gang_waiting = average_gang_runs(modified_gang_waiting_runs)

# # ---- MODIFIED ML ----
# ml_avg_core_util = overall_avg_utilization(ml_core_util_runs)
# ml_avg_throughput = average_scalar_list(ml_throughput_runs)
# ml_avg_gang_response = average_gang_runs(ml_gang_response_runs)
# ml_avg_gang_turnaround = average_gang_runs(ml_gang_turnaround_runs)
# ml_avg_gang_waiting = average_gang_runs(ml_gang_waiting_runs)

# # Print or debug-check
# print("===== AVERAGED METRICS =====")
# print(f"Basic   => CoreUtil= {basic_avg_core_util:.2f}, Throughput= {basic_avg_throughput:.2f}, "
#       f"GangResponse= {basic_avg_gang_response}, GangTurn= {basic_avg_gang_turnaround}, "
#       f"GangWait= {basic_avg_gang_waiting}")
# print(f"Mod     => CoreUtil= {modified_avg_core_util:.2f}, Throughput= {modified_avg_throughput:.2f}, "
#       f"GangResponse= {modified_avg_gang_response}, GangTurn= {modified_avg_gang_turnaround}, "
#       f"GangWait= {modified_avg_gang_waiting}")
# print(f"Mod_ML  => CoreUtil= {ml_avg_core_util:.2f}, Throughput= {ml_avg_throughput:.2f}, "
#       f"GangResponse= {ml_avg_gang_response}, GangTurn= {ml_avg_gang_turnaround}, "
#       f"GangWait= {ml_avg_gang_waiting}")


# # ------------------------------------------------------------------
# # 4) Now Plot the final AVERAGED metrics for each approach
# # ------------------------------------------------------------------

# import numpy as np

# # 4a) Single bar for average core utilization
# plt.figure()
# labels = ["Basic", "Modified", "Mod ML"]
# vals = [basic_avg_core_util, modified_avg_core_util, ml_avg_core_util]
# plt.bar(labels, vals)
# plt.ylabel("Avg Core Utilization (%)")
# plt.title("Average Core Utilization (63/83/93 Gangs)")
# for i, v in enumerate(vals):
#     plt.text(i, v + 0.5, f"{v:.2f}", ha='center')
# plt.show()

# # 4b) Single bar for average system throughput
# plt.figure()
# vals = [basic_avg_throughput, modified_avg_throughput, ml_avg_throughput]
# plt.bar(labels, vals)
# plt.ylabel("Processes / unit time")
# plt.title("Average System Throughput (63/83/93 Gangs)")
# for i, v in enumerate(vals):
#     plt.text(i, v + 0.005, f"{v:.2f}", ha='center')
# plt.show()

# # 4c) Gang Response Times (side-by-side). 
# # For consistency, let's assume all three approaches have the same # of gangs 
# # in this average scenario, e.g. 3 gangs. If so, we do:
# plt.figure()
# x_vals = np.arange(len(basic_avg_gang_response))  # e.g. [0,1,2]
# width = 0.25

# plt.bar(x_vals - width, basic_avg_gang_response, width=width, label='Basic')
# plt.bar(x_vals,        modified_avg_gang_response, width=width, label='Modified')
# plt.bar(x_vals + width, ml_avg_gang_response, width=width, label='Mod ML')

# plt.xticks(x_vals, [f"Gang {i}" for i in x_vals])
# plt.ylabel("Response Time")
# plt.title("Average Gang Response Times")
# plt.legend()
# plt.show()


# # 4d) Gang Turnaround
# plt.figure()
# x_vals = np.arange(len(basic_avg_gang_turnaround))
# width = 0.25

# plt.bar(x_vals - width, basic_avg_gang_turnaround, width=width, label='Basic')
# plt.bar(x_vals,        modified_avg_gang_turnaround, width=width, label='Modified')
# plt.bar(x_vals + width, ml_avg_gang_turnaround, width=width, label='Mod ML')

# plt.xticks(x_vals, [f"Gang {i}" for i in x_vals])
# plt.ylabel("Turnaround Time")
# plt.title("Average Gang Turnaround Times")
# plt.legend()
# plt.show()


# # 4e) Gang Waiting
# plt.figure()
# x_vals = np.arange(len(basic_avg_gang_waiting))
# width = 0.25

# plt.bar(x_vals - width, basic_avg_gang_waiting, width=width, label='Basic')
# plt.bar(x_vals,        modified_avg_gang_waiting, width=width, label='Modified')
# plt.bar(x_vals + width, ml_avg_gang_waiting, width=width, label='Mod ML')

# plt.xticks(x_vals, [f"Gang {i}" for i in x_vals])
# plt.ylabel("Waiting Time")
# plt.title("Average Gang Waiting Times")
# plt.legend()
# plt.show()

