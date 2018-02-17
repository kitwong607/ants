import json

def check_required_value(keys, target_dict):
    is_pass = True
    missed_key = []
    for key in keys:
        if key not in target_dict:
            is_pass = False
            missed_key.append(key)

    d = {}
    if is_pass:
        return True
    else:
        return create_socketio_response("fail", ", ".join(missed_key) + " are missed", d)

def create_socketio_response(status, description, action, data={}):
    return_d = {}
    return_d['status'] = status
    return_d['description'] = description
    return_d['action'] = action
    return_d['data'] = data
    return return_d