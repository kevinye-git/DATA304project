#!/usr/bin/python
""" monitor.py is used to observe a sequence of events and record
their times in a text file for later analysis
input: requested:
-   heading (Several lines, terminated by a blank line)
-   observer name
-   file name to write to
Each data observation consists of a line of text. Blank lines are allowed.
The program is terminated by inputting 'end' or a <ctrl-d>.

output:
- a file with the chosen name
- with comments giving the heading (several lines), observer,
  and starting date and time
- a series of timed lines using the input text for each event.
  times are floating point seconds since midnight.
  60462.771244  a

$Revision: 1.26 $
$Date: 2010/08/08 05:05:15 $
started: gav 2008 10 16
"""
import datetime
import sys


def time2float(line):
    """ converts formatted time 'nn:nn:nn:nnnnn' to float
    >>> time2float('21:33:25:5342')
    77605.005342000004
    """
    spline = line.split(':')
    ints = [int(spline[i]) for i in range(4)]
    result = 3600*ints[0] + 60*ints[1] + ints[2] + 1E-6*ints[3]
    return result


def origtime2float(time):
    """ converts current datetime to float
    >>> import datetime
    >>> t = datetime.datetime(2010, 8, 5, 14, 45, 41, 778877)
    >>> origtime2float(t)
    53141.778876999997
    """
    t3fmt = time.strftime("%H:%M:%S:%f")
    return time2float(t3fmt)


def readheaders():
    """ requests the header information
    (doctest removed as it involves input)
    """
    line = input("Data description. Blank line ends: ")
    heading = line
    while line:
        line = input("")
        if line:
            heading += "\n# "+line
    observer = input("please enter the observer's name: ")
    filename = input(
        "please enter the name of the file to be written to: ")
    version = '$Revision: 1.26 $'[11:-2]
    return (heading, observer, filename, version)


def formatheaders(headerstuff, t=''):
    """ Format the headers as a string for
    the first part of the returned file
    """
    fmt = "%a %b %d, %Y %H:%M:%S"
    datefmt = "%a %b %d, %Y"
    fmt2 = "%H:%M:%S:%f"
    fmt3 = "%H:%M:%S"
    heading, observer, filename, version = headerstuff
    if not t:
        t = datetime.datetime.now()
    startdate = t.strftime(datefmt)
    starttime = t.strftime(fmt3)
    start_obs_time = origtime2float(t)
    headers2 = """# heading:  %(heading)s
# observer: %(observer)s
# filename: %(filename)s
# date:     %(startdate)s at %(starttime)s  v%(version)s
%(start_obs_time)12.6f  begin
"""
    return filename, headers2 % vars()


def main():
    """ Reads in headers and then the series of lines
    writing to the specified file."""
    filename, headers = formatheaders(readheaders())
    f = open(filename, 'w')
    f.write(headers)
    print("now enter a line for each event. Terminate with 'end':")
    going = True
    while going:
        try:
            lin = input()
            if lin == 'end':
                going = False
        except EOFError:
            going = False
            lin = 'end'
        t3 = datetime.datetime.now()
        t3fmt = t3.strftime("%H:%M:%S:%f")
        t3fmt = time2float(t3fmt)
        r = "%12.6f  %s\n" % (t3fmt, lin)
        f.write(r)
    f.close()


if __name__ == '__main__':
    main()
