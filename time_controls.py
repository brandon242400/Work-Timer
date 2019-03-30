# File used to handle time related things for main file
import outsource
global timestamp
timestamp = 0
timestamp_single = 0

def time_up():
    ''' Returns current time in seconds and increments 'timestamp' by 1 s '''
    # time = outsource.return_value('timelogs.txt', 'timestamp')
    # outsource.replace_value('timelogs.txt', 'timestamp', str(int(time) + 1))
    # time = int(time)
    # time += 1
    global timestamp
    timestamp += 60
    return timestamp


def get_time():
    return timestamp + timestamp_single


def time_up_single():
    global timestamp_single
    timestamp_single += 1
    return timestamp_single + timestamp


def format_time(time):
    ''' Formats time to fit into main window. EX - "00:00:00" '''
    time = int(time)
    hours = int(time/3600)
    left = time - (hours * 3600)
    minutes = int(left/60)
    left = left - (minutes * 60)
    seconds = int(left)
    formatted = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return formatted
