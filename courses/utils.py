import datetime
import math


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

    print((minutes_per_day - (parameter_obj.pause_duration.hour * 60 + parameter_obj.pause_duration.minute)))
    print(block_size)
    blocks_per_day = (minutes_per_day + (parameter_obj.pause_duration.hour * 60 + parameter_obj.pause_duration.minute)) // block_size

    courses_blocks = {}
    for course in selected_courses:
        size = int((int(course.avg_study_time) * 60 + (course.avg_study_time - math.floor(course.avg_study_time)) * 60) // (parameter_obj.study_bloc_size.hour * 60 + parameter_obj.study_bloc_size.minute))
        courses_blocks[course.name] = [(course, True) for x in range(size)]

    zipped = zip(*courses_blocks.values())
    flattened_list = [item for sublist in zipped for item in sublist]

    blocks = []
    for blocks_index in range(0, len(flattened_list), blocks_per_day):
        todays_block = flattened_list[blocks_index:blocks_index + blocks_per_day]
        blocks.append(todays_block)

    return blocks  # return list of block tuple () This avoids circular imports
