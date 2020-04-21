
def get_matplotlib_figure_weather_new():

    t = np.arange(0, 3, .01)
    fig, ax1 = plt.subplots()
    fig.subplots_adjust(left=0, bottom=0.01, right=0.99, top=0.99, wspace=None, hspace=None)

    # fig = plt.figure(figsize=(1, 1), dpi=100)
    # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t), label='Kurve1')
    data1 = 2 * np.sin(2 * np.pi * t)
    data2 = 3 * np.sin(3 * np.pi * (t + 0.5))

    ax1.plot(t, data1, label='Kurve1')
    ax1.plot(t, data2, label='Kurve2')

    ax1.tick_params(axis='x', rotation=45)
    ax1.tick_params(axis='both', which='both', direction='in', pad=-20)
    # ax1.grid()
    ax1.legend(frameon=False)

    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('Messgröße2', color=color)  # we already handled the x-label with ax1
    # ax2.plot(t, data2*0.1, color=color)
    return fig
