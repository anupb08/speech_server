import tornado.web
from tornado.options import define, options
import sys
import handlers
import os
import logging.handlers
from conf import config


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
    else:
        mode = 'dev'

    configurations = getattr(config, mode)
    define("configurations", default=configurations, help="environment configurations.")

    options.log_file_prefix = configurations.get('server_configuration').get('log_file_prefix')
    options.parse_command_line()

    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    port = options.configurations.get('app_port', 5000)
    application = tornado.web.Application([
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_dir, "default_filename": "index.html"}),
        (r"/", handlers.MainHandler),
        (r"/api/start_file_transcription", handlers.StartFileTranscriptionHandler),
        (r"/api/get_transcription_status", handlers.GetTranscriptionStatus),
    ])

    server = tornado.httpserver.HTTPServer(application, max_buffer_size=167772160)  # 10G
    server.listen(port)
    # application.listen(port)
    print("Server started on port : " + str(port))
    logging.info("Server started on port : " + str(port))
    tornado.ioloop.IOLoop.instance().start()
