import pygal
import requests
from pygal.style import NeonStyle

def get_quotes(symbol, period):
    r = requests.get(f"https://api-adapter.backend.currency.com/api/v1/klines?interval={period}&symbol={symbol}")
    return r.json()

def get_symbol_svg(s,p, levels = "при пробое !50000! покупка с целью !60000!"):
    config = pygal.Config()
    config.show_legend = False
    config.human_readable = True
    config.fill = False
    config.width = 600
    config.height = 450
    config.x_label_rotation = 45
    config.show_dots=False
    config.margin = 5

    st = pygal.style.Style( background = 'black',
                            plot_background = '#111',
                            colors=('#ffebcd', '#daa520', '#daa520', '#daa520', '#daa520'),
                            foreground = '#999',
                            foreground_strong = '#eee',
                            foreground_subtle = '#555'
                           )

    chart = pygal.Line(config, style=st)
    chart.title = p

   # chart.x_labels = map(str, range(2002, 2013))

    quotes = get_quotes(s,p)

   # open_vals = [float(i[1]) for i in quotes]
   # high_vals = [float(i[1]) for i in quotes]
   # low_vals = [float(i[1]) for i in quotes]
    close_vals = [float(i[3]) for i in quotes]

   # chart.add('Open', open_vals)
   # chart.add('High', high_vals)
   # chart.add('Low', low_vals)
    chart.add('Close', close_vals)


    levels = parse_levels(levels)
    mn = min(close_vals)
    mx = max(close_vals)

    for level in levels:
        if mn <= level <= mx:
            vals = [level for v in close_vals]
            chart.add(level, vals)
    svg = chart.render(is_unicode=True)

    return svg

def parse_levels(string):
    tokens = [int(t) for t in string.split("!") if t.isnumeric()]
    return (tokens)
