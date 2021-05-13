import pygal
import requests

def get_quotes(symbol, period):
    r = requests.get(f"https://api-adapter.backend.currency.com/api/v1/klines?interval={period}&symbol={symbol}")
    return r.json()

def get_symbol_svg(s,p):
    config = pygal.Config()
    config.show_legend = False
    config.human_readable = True
    config.fill = False
    config.width = 400
    config.height = 300
    config.x_label_rotation = 45
    config.show_dots=False
    config.margin = 5

    red = pygal.style.Style(colors=('#E8537A',))
    chart = pygal.Line(config, style=red)
    chart.title = p

   # chart.x_labels = map(str, range(2002, 2013))

    quotes = get_quotes(s,p)

   # open_vals = [float(i[1]) for i in quotes]
    high_vals = [float(i[1]) for i in quotes]
    low_vals = [float(i[1]) for i in quotes]
  #  close_vals = [float(i[1]) for i in quotes]

   # chart.add('Open', open_vals)
    chart.add('High', high_vals)
    chart.add('Low', low_vals)
  #  chart.add('Close', close_vals)

    svg = chart.render(is_unicode=True)
    return svg