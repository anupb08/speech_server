import json
import tornado
from handlers import BaseHandler


class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.run_background(self._get, ())

    def _get(self):
        """
            Default end point for service status.
        :return:
            string: service status
        """
        return json.dumps({"status": True, "message": "Service running."})
