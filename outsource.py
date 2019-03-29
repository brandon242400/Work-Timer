# File made to hold all random methods to avoid cluttering up 'dooks_main'
import datetime


def enter_into_logs(session):
    ''' Puts work session into 'logs.txt' with date '''
    file = open('logs.txt', 'a')
    date = datetime.datetime.now().strftime("%m/%d/%Y")
    file.write(date + " - " + session + "\n\n")
    file.close()


def pref(varName):
    ''' Returns the value of variable name from 'preferences.txt' '''
    file = open('preferences.txt', 'r')
    content = file.readlines()
    file.close()
    for i in content:
        if varName in i:
            value = i

    num = value.find(':')
    value = value[num+2:-1]

    return value


def return_value(fileName, varName):
    ''' Returns the value from a given file '''
    file = open(fileName, 'r')
    content = file.readlines()
    file.close()
    for i in content:
        if varName in i:
            value = i

    num = value.find(':')
    value = value[num+2:-1]

    return value


def replace_value(fileName, varName, data):
    ''' Replaces the value from a given file '''
    file = open(fileName, 'r')
    content = file.readlines()
    file.close()
    for i in content:
        if varName in i:
            value = i
            content.remove(i)

    num = value.find(':')
    value = value[:num+1]
    value += ' ' + str(data)

    file = open(fileName, 'w')
    for i in content:
        file.write(i)
    file.write(value + '\n')
    file.close()
