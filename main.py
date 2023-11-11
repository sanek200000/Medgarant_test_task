from datetime import datetime, timedelta

# Время работы врача
START_TIME = datetime.strptime("09:00", "%H:%M")
END_TIME = datetime.strptime("21:00", "%H:%M")

# Занятые временные интервалы
BUSY = [
    {"start": "10:30", "stop": "10:50"},
    {"start": "18:40", "stop": "18:50"},
    {"start": "14:40", "stop": "15:50"},
    {"start": "16:40", "stop": "17:20"},
    {"start": "20:05", "stop": "20:20"},
]


def get_busy_intervals(intervals: list) -> list:
    """
    Преобразование занятых интервалов в объекты datetime
    """
    return [
        (
            datetime.strptime(interval["start"], "%H:%M"),
            datetime.strptime(interval["stop"], "%H:%M"),
        )
        for interval in intervals
    ]


def get_is_slot_free(current_time: datetime, busy_intervals: list) -> tuple | None:
    """
    Функция возвращает занятый временной интервал, если текущее время в него попадает
    """
    for busy_start, busy_end in busy_intervals:
        if busy_start <= current_time < busy_end:
            return busy_start, busy_end


def find_free_slots(start: datetime, end: datetime, slot_duration: int) -> list:
    """
    Функция определения свободных интервалов
    """
    result = list()
    current_time = start
    busy_intervals = get_busy_intervals(BUSY)

    while current_time + timedelta(minutes=slot_duration) <= end:
        slot_end_time = current_time + timedelta(minutes=slot_duration)
        is_slot_free = get_is_slot_free(current_time, busy_intervals)
        if is_slot_free:
            busy_start, busy_end = is_slot_free

            result[-1]["stop"] = busy_start.strftime("%H:%M")
            current_time = busy_end
        else:
            result.append(
                {
                    "start": current_time.strftime("%H:%M"),
                    "stop": slot_end_time.strftime("%H:%M"),
                }
            )

            current_time += timedelta(minutes=slot_duration)

    return result


if __name__ == "__main__":
    # Поиск свободных интервалов по 30 минут
    free_slots = find_free_slots(START_TIME, END_TIME, slot_duration=30)

    # Вывод результатов
    for slot in free_slots:
        print(f"Свободное окно: {slot['start']} - {slot['stop']}")
