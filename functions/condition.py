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

