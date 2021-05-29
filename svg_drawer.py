import asyncio
import aiohttp
import pygal
from pygal.style import NeonStyle
import symbols_helper

async def async_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.json()
            return resp

async def get_svgs_async(s, periods):
    #prepare urls
    urls = []
    for p in periods:
        url = f"https://api-adapter.backend.currency.com/api/v1/klines?interval={p}&symbol={s}"
        urls.append(url)

    #prepare requests_corutines
    requests = []
    for url in urls:
        rq = async_request(url)
        requests.append(rq)

    #execute requests_corutines
    responses = await asyncio.gather(*requests)

    #draw svgs
    comment = symbols_helper.get_comment_for_symbol(s)
    print(comment)
    svgs = [get_symbol_svg(p, quotes, levels=comment) for p, quotes in zip(periods, responses)]
    return svgs

def get_symbol_svg(title, quotes, levels="при пробое !50000! покупка с целью !60000!"):
    config = pygal.Config()
    config.show_legend = False
    config.human_readable = True
    config.fill = False
    config.width = 600
    config.height = 450
    config.x_label_rotation = 45
    config.show_dots = False
    config.margin = 5

    st = pygal.style.Style( background = 'black',
                            plot_background = '#111',
                            colors=('#ffebcd', '#daa520', '#daa520', '#daa520', '#daa520'),
                            foreground = '#999',
                            foreground_strong = '#eee',
                            foreground_subtle = '#555'
                            )

    chart = pygal.Line(config, style=st)
    chart.title = title

   # chart.x_labels = map(str, range(2002, 2013))



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
