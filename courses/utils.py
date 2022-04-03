import datetime


def schedule_this(selected_courses, user, parameter_obj, start_date, end_date):
    total_minutes = (end_date - start_date).days * (parameter_obj.study_time_per_day.hour * 60 + parameter_obj.study_time_per_day.minute)
    block_size = (
        (parameter_obj.study_bloc_size.hour * 60 + parameter_obj.study_bloc_size.minute) + 
        (parameter_obj.pause_duration.hour * 60 + parameter_obj.pause_duration.minute)
    )

    available_slots = (total_minutes) // (block_size)

    minutes_per_day = (parameter_obj.study_time_per_day.hour * 60 + parameter_obj.study_time_per_day.minute)
    block_size = (
        (parameter_obj.study_bloc_size.hour * 60 + parameter_obj.study_bloc_size.minute) +
        (parameter_obj.pause_duration.hour * 60 + parameter_obj.pause_duration.minute)
    )

    blocks_per_day = minutes_per_day // block_size

    return []  # return list of block tuple () This avoids circular imports