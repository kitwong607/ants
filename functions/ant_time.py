from datetime import datetime, timedelta
import time

def is_new_date(current_date, input_date):
    if (current_date == None or current_date.date() != input_date.time.date()):
        return True
    return False

def is_time_before(marker_hour, marker_mintue, marker_second, input_hour, input_minute, input_second):
    marker_time = marker_hour*10000 + marker_mintue*100 + marker_second
    input_time = input_hour*10000 + input_minute*100 + input_second
    if input_time < marker_time:
        return True
    else:
        return False

def is_time_after(marker_hour, marker_mintue, marker_second, input_hour, input_minute, input_second):
    marker_time = marker_hour*10000 + marker_mintue*100 + marker_second
    input_time = input_hour*10000 + input_minute*100 + input_second
    if input_time > marker_time:
        return True
    else:
        return False

def remove_time_from_datetime(datetime_to_remove):
    time_offset = timedelta(
                hours=datetime_to_remove.hour,
                minutes=datetime_to_remove.minute,
                seconds=datetime_to_remove.second,
                microseconds=datetime_to_remove.microsecond)
    datetime_to_remove = datetime_to_remove - time_offset
    return datetime_to_remove

def second_between_two_datetime(datetime_1, datetime_2):
    if(datetime_1>datetime_2):
        return abs((datetime_1 - datetime_2).seconds)
    else:
        return abs((datetime_2 - datetime_1).seconds)

def mintue_between_two_datetime(datetime_1, datetime_2):
    if(datetime_1>datetime_2):
        return abs((datetime_1 - datetime_2).seconds) // 60  # in mintues
    else:
        return abs((datetime_2 - datetime_1).seconds) // 60  # in mintues

def start_count_time_used():
    return time.time()

def stop_count_time_used(start_time, task):
    #print("--- "+str(round(time.time() - start_time, 2))+" seconds --- for " + task)
    print("--- "+ str(time.time() - start_time) + " seconds --- for " + task)
