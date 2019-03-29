import outsource


def time_up():
    ''' Returns current time in seconds and increments 'timestamp' by 100 ms '''
    time = outsource.return_value('timelogs.txt', 'timestamp')
    outsource.replace_value('timelogs.txt', 'timestamp', str(int(time) + 1))
    time = int(time)
    time += 1
    return time


def format_time(time):
    ''' Formats time to fit into main window. EX - "00:00:00" '''
    time = int(time)
    hours = int(time/36000)
    left = time - (hours * 36000)
    minutes = int(left/600)
    left = left - (minutes * 600)
    seconds = int(left/10)
    left = left - (seconds * 10)
    milliseconds = int(left)
    formatted = "{:02d}:{:02d}:{:02d}:{}".format(hours, minutes, seconds, milliseconds)
    return formatted
