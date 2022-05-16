import numpy as np

# Function to search for an event in the list


def find_event(data, event):
    stop = False
    time = None
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == event:
                time = data[i][0]
                stop = True
                break
        if stop:
            break
    return time


def CalculateLorB(filenames, calc):
    total_sum = 0
    total_denom = 0
    for name in filenames:
        lines = ReadSplitLines(name, split=False)
        letter1 = "a"
        letter2 = "d"
        total = 0
        table = [[], []]
        times = table[0]
        number = table[1]
        del lines[-1]
        sum = 0
        for ind, line in enumerate(lines):
            lst1 = []
            lst2 = []
            for pos, char in enumerate(line):
                if(char == letter1):
                    lst1.append(pos)
                if(char == letter2):
                    lst2.append(pos)
            total = total + len(lst1) - len(lst2)

            times.append(line.split()[0])
            number.append(total)
        for i in range(len(times)-1):
            if calc == "B":
                if float(number[i]) > 0:
                    sum = sum + (float(times[i+1])-float(times[i]))
            if calc == "L":
                sum = sum + (float(number[i]) *
                             (float(times[i+1])-float(times[i])))

        denom = float(times[-1])-float(times[0])
        total_sum = total_sum + sum
        total_denom = total_denom + denom
    return total_sum/total_denom

# Sets up the data in a specific line format for the other calculation functions to calculate the times


def ReadSplitLines(name, split):
    filename = name
    lines = []

    # open file and read all lines into a list
    f = open(filename, 'r')
    while True:
        line = f.readline()
        if line == '':
            break
        lines.append(line)

    # Leave only lines with times and split each line into a list of 2 terms or more
    lines = lines[4:]
    if split:
        for i in range(len(lines)):
            lines[i] = lines[i].split()
    f.close()
    return lines

# This function calculates interarrival times


def CalculateArrivals(lines):
    arrival_times = []
    cond = True
    i = 1
    while cond:
        letter = 'a' + str(i)
        if find_event(lines, letter) == None:
            break
        arrival_times.append(find_event(lines, letter))
        i += 1
    interarrival_times = []
    for i in range(len(arrival_times)-1):
        interarrival_time = float(
            arrival_times[i+1])-float(arrival_times[i])
        interarrival_times.append(interarrival_time)
    return interarrival_times

# This fucntion can calculate service times, queue times and total times in system


def CalculateTimesBetween(lines, calc_name="service"):
    letter1 = 'd'
    letter2 = 's'
    if (calc_name == "queue"):
        letter1 = 's'
        letter2 = 'a'
    if (calc_name == "total"):
        letter1 = 'd'
        letter2 = 'a'
    times = []
    cond = True
    i = 1
    while cond:
        event1 = letter1 + str(i)
        event2 = letter2 + str(i)
        if find_event(lines, event1) == None or find_event(lines, event2) == None:
            break
        times.append(float(find_event(lines, event1)) -
                     float(find_event(lines, event2)))
        i += 1
    return times


# use this function to read the data - see the main program for an example of how call this function
def ReadData(filenames):
    AllArrivals = []
    AllServices = []
    AllQueues = []
    AllTotaltime = []
    for name in filenames:
        lines = ReadSplitLines(name, split=True)

        # calculate interarrival times
        AllArrivals.extend(CalculateArrivals(lines))

        # Calculate service times
        AllServices.extend(CalculateTimesBetween(lines))

        # calculate queue waiting time before start service

        AllQueues.extend(CalculateTimesBetween(lines, "queue"))

        # Calculate total time in system
        AllTotaltime.extend(CalculateTimesBetween(lines, "total"))
    return AllArrivals, AllServices, AllQueues, AllTotaltime


# main program - will not run if imported into another py file for use

# Run this program to calculate parameters to be used in building M1 and M2 models and some performance measures for comparison
if __name__ == "__main__":
    filenames = ["DATA304-project\Data Collection\KevinYeData.txt",
                 "DATA304-project\Data Collection\PatrickQData.txt",
                 "DATA304-project\Data Collection\TamaHoareData.txt",
                 "DATA304-project\Data Collection\dataviviandong.txt"]
    results = ReadData(filenames=filenames)
    AllArrivals = results[0]
    AllServices = results[1]
    AllQueues = results[2]
    AllTotaltime = results[3]
    print("Calculated Parameters used for building models")

    print("============================")

    print("Average Inter-arrival time:")
    print(np.mean(AllArrivals))

    print("")

    print("Average Service time, W_s:")
    print(np.mean(AllServices))

    print("")

    print("Average Queue Time, W_q: ")
    print(np.mean(AllQueues))

    print("===========================")

    print("Performance Measures")

    print("Average time in system, W:")
    print(np.mean(AllTotaltime))

    print("")

    print("Average number of customers in the system, L")
    print(CalculateLorB(filenames, "L"))

    print("")

    print("Proportion of time servers are busy in the system, B")
    print(CalculateLorB(filenames, "B"))

    print("")

    print("The effective arrival rate, Lambda Effective")
    print(CalculateLorB(filenames, "L")/np.mean(AllTotaltime))
