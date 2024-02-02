from datetime import datetime as dt

def timestamp_now():
    return dt.now().strftime("%Y/%m/%d %H:%M:%S")#str(dt.now())[0:-7]
def sub_timestamps(a,b):
    return (dt.strptime(a,"%Y/%m/%d %H:%M:%S") - dt.strptime(b,"%Y/%m/%d %H:%M:%S")).total_seconds()

def find_id_position_in_list(list_names,search_name,key):
    for i, name in enumerate(list_names):
        if name[key] == search_name:
            return i
    return -1

