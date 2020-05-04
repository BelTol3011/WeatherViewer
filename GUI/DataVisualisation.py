import numpy as np
import matplotlib.pyplot as plt
from Plugin.API.Main import database as db
from Core import Timersdates
from pylab import *
from Core.Timersdates import unix_to_datestring


def get_matplotlib_figure_weather_new():
    current_date = Timersdates.datestring_to_unix('', 0, 0, False)
    current_date_str = Timersdates.unix_to_datestring(current_date, 1, 0, False)
    time_frame_viewport = [-21600, 21600]  # +-6h ;3600 s = 1h
    time_frame_gridres = 60  # 1 min
    # t = np.arange(current_date + time_frame_viewport[0], current_date + time_frame_viewport[1], time_frame_gridres)
    # print(t)
    current_position = (12.3, 23.2)

    print(current_date, current_date_str)
    # print(db[current_position]["data"]["weather"])

    # [(key, db[current_position]['data']['weather'][key]) for key in db[current_position]['data']['weather']]

    a = []
    for key in db[current_position]['data']['weather']:
        a.append((key[0], db[current_position]['data']['weather'][key]["temperature_real"]))
    date_strings = []
    for date in a:
        date_strings.append(unix_to_datestring(date[0], 1, 0, False))

    print(date_strings)

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(left=0, bottom=0.01, right=0.99, top=0.99, wspace=None, hspace=None)
    fig = plt.figure(figsize=(1, 1), dpi=100)

    # ax1.ticklabel_format(useOffset=False)
    # data1 = 2 * np.sin(2 * np.pi * t)
    axis1 = [i[0] for i in a]
    data1 = [j[1] for j in a]
    fig.add_subplot(111).plot(axis1, data1, 'bo-', label='Kurve1')
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='both', which='both', direction='in', pad=-20)
    ax.set_xticks(axis1)
    ax.set_xticklabels(date_strings, minor=False, rotation=45)
    ax.grid()
    ax.legend(frameon=False)



    # ax1.plot(t, data1, label=current_date_str)


    # data2 = 3 * np.sin(3 * np.pi * (t + 0.5))
    #ax1.plot(axis1, data1, label='Kurve2')
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('Messgröße2', color=color)  # we already handled the x-label with ax1
    # ax2.plot(t, data2*0.1, color=color)

    return fig
