import matplotlib.pyplot as plt
import io
import base64

def plot_data(indicator_data):
    plots = {}
    for key, data in indicator_data.items():
        fig, ax = plt.subplots()
        data.plot(ax=ax)
        plt.title(key)
        figfile = io.BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf8')
        plots[key] = "data:image/png;base64," + figdata_png
        plt.close(fig)
    return plots