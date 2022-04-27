filename = 'DATA304-project\KevinYeData.txt'
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
for i in range(len(lines)):
    lines[i] = lines[i].split()
f.close()

# Function to search for an event in the list


def find_event(data, event):
    stop = False
    time = None
    for i in range(len(data)):
        for j in range(len(data[i])):
            if lines[i][j] == event:
                time = lines[i][0]
                stop = True
                break
        if stop:
            break
    return time


# calculate interarrival times
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
    interarrival_time = float(arrival_times[i+1])-float(arrival_times[i])
    interarrival_times.append(interarrival_time)


# calculate service times
service_times = []
cond = True
i = 1
while cond:
    letter = 'd' + str(i)
    letter2 = 's' + str(i)
    if find_event(lines, letter) == None or find_event(lines, letter2) == None:
        break
    service_times.append(float(find_event(lines, letter)) -
                         float(find_event(lines, letter2)))
    i += 1
print(interarrival_times)
print(service_times)
