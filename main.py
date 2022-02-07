from datetime import datetime, date
from datetimerange import DateTimeRange
dat = date.today()
now = datetime.now()
dt = now.strftime('%H:%M:%S')
time_range = DateTimeRange("06:30:30", "20:30:30")
print(dat)
print(now)
print(dt)
if dt in time_range:
    print("True")
else:
    print('false')

