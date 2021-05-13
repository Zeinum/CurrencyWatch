#!/usr/bin/python

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import pygal
import json
import svg_drawer


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("[HTTP](MainHandler) User Connected.")

        s = self.get_argument("s", "BTC/USD")
        periods = ["1d","4h","1h","15m"]

        svgs = []
        for p in periods:
            svgs.append(svg_drawer.get_symbol_svg(s,p))

        self.render("index.html", symbol=s, svgs=svgs)


class WSHandler(tornado.websocket.WebSocketHandler):

    # last data state before sending it to the browser
    def send_event_to_browser(self, event_name, event_data):
        #prepare a valid message, like a protocol for data exchange between server and browser, same protocol should be on js side
        plain_json_ws_payload = json.dumps({'event_name': event_name, 'event_data': event_data})
        self.write_message(plain_json_ws_payload)
        return plain_json_ws_payload


    @staticmethod
    def open():
        print('[WS] Connection was opened.')

    def on_message(self, message):
        """
        all data events will be processed here
        """
        #print(f'[WS] Incoming message:{message}')
        ws_json = json.loads(message)
        event = ws_json['event_name']
        data = ws_json['event_data']

        if event == "rndm_btn":
            pass



    @staticmethod
    def on_close():
        print('[WS] Connection was closed.')


##################################################
if __name__ == "__main__":

    # Tornado Folder Paths
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True #TODO remove when ready
    )
    # Tonado server port
    PORT = 8082

    # init webserver
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/ws', WSHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    main_loop = tornado.ioloop.IOLoop.instance()

    print("Tornado Server started")

    print(f"http://127.0.0.1:{PORT}/")
    main_loop.start()