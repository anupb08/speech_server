import tornado
import logging
import json
import asyncio
from multiprocessing.pool import ThreadPool
from tornado.platform import asyncio as async_torn


asyncio.set_event_loop_policy(async_torn.AnyThreadEventLoopPolicy())


class BaseHandler(tornado.web.RequestHandler):
    """Base Handler class for all the request."""
    _workers = ThreadPool(30)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X - Requested - With, X - Requested - By, If - Modified - Since, X - File - Name, Cache - Control")
        info = {
            'Method': self.request.method,
            'URL': self.request.uri,
            'Remote_IP': self.request.remote_ip
        }
        logging.info(json.dumps(info))

    def run_background(self, func, args=(), kwds={}):
        loop = tornado.ioloop.IOLoop.instance()

        def _callback(result):
            loop.add_callback(callback=lambda: self.on_complete(result))

        self._workers.apply_async(func, args, kwds, _callback)

    def on_complete(self, res):
        self.write(res)
        self.finish()
