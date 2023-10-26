time = {
    "second" : 1,
    "minute" : 60,
    "hour" : 60*60,
    "day" : 24*60*60,
    "year" : 365*24*60*60
}


def sec_to_time(duration):
    years = str((duration % time['year'])) + ' years' if duration / time['year'] >= 1 else ''
    days = str((duration - int(years) * time['year']) % time['days']) + ' days' if (duration - int(years) * time['year']) / time['days'] >= 1 else ''
    hours = str((duration - int(years) * time['year'] - int(days) * time['days']) % time['hour']) + ' hours' if (duration - int(years) * time['year'] - int(days) * time['days']) / time['hour'] >= 1 else ''
    minutes = str((duration - int(years) * time['year'] - int(days) * time['days'] - int(hours) * time['hours']) % time['hour']) + ' minutes' if (duration - int(years) * time['year'] - int(days) * time['days'] - int(hours) * time['hours'])  time['hour'] >= 1 else ''
    seconds = str((duration - int(years) * time['year'] - int(days) * time['days'] - int(hours) * time['hours'] - int(minutes) * time['minutes'])) + 'seconds' if (duration - int(years) * time['year'] - int(days) * time['days'] - int(hours) * time['hours'] - int(minutes) * time['minutes']) >= 1 else ''
    return print(str(years) + str(days) + str(hours) + str(minutes) + str(seconds))

sec_to_time(61)