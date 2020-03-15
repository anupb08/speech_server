import logging
import subprocess
import tornado
import os
import util
#from util.jobdb import getTranscriptionStatus, getTranscriptFilename
import json

from tornado.options import options
from handlers import BaseHandler

class GetTranscriptionStatus(BaseHandler):
	@tornado.web.asynchronous
	def get(self, *args, **kwargs):
		self.run_background(self._get, ())

	def _get(self):
		try:
			request_id = self.request.arguments['request_id'][0].decode()
			check = int(util.getTranscriptionStatus(request_id))
			#t = util.test()
			print(request_id,check)
			if check < 100:
				return json.dumps(util.Response(status=True, message="Either transcription not completed or unsuccessful.", data={'progress': check, 'transcript': None}).__dict__,
                              cls=util.CustomJSONEncoder)
			if check == 100:
				trans_files = util.getTranscriptFilename(request_id).split(',')
				print(trans_files)
				trans_file = trans_files[0]
				if os.path.isfile(trans_file):
					with open(trans_file, 'r') as f:
						transcript = json.load(f)
				transcript2 = None
				if len(trans_files) > 1:
					trans_file2 = trans_files[1]
					if os.path.isfile(trans_file2):
						with open(trans_file2, 'r') as f:
							transcript2 = json.load(f)
				return json.dumps(util.Response(status=True, message="Transcription successful.", data={'progress': check, 'transcript': transcript, 'transcript2': transcript2}).__dict__,
                                cls=util.CustomJSONEncoder)
			return json.dumps(util.Response(status=False, message="Transcribed file is not available.", data={'progress': check, 'transcript': None}).__dict__,
                       cls=util.CustomJSONEncoder)
		except Exception as ex:
			#logging.error(traceback.print_exc())
			logging.error(ex)
			return json.dumps(util.Response(status=False, message=str(ex), data={}).__dict__,
                              cls=util.CustomJSONEncoder)



