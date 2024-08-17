import datetime as dt

import panel as pn

pn.extension()


datetime_picker = pn.widgets.DatetimePicker(
    name='Datetime Picker', value=dt.datetime(2021, 3, 2, 12, 10)
)

pn.Column(datetime_picker, height=400)

datetime_picker.value