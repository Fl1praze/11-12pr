from datetime import datetime
import pytz

#Приводим datetime к мск времени
def to_moscow_time(dt: datetime) -> datetime:
    msk = pytz.timezone('Europe/Moscow')
    if dt.tzinfo is None:
        return msk.localize(dt)
    else:
        return dt.astimezone(msk) 