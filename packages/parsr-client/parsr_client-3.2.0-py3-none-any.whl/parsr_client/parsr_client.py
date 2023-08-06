#
# Copyright 2020 AXA Group Operations S.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from glob import glob
from itertools import chain
import os
import sys
import json
import time
import ast
from enum import Enum

import semver

import pandas as pd
import requests
from io import StringIO

import diff_match_patch
from sxsdiff import DiffCalculator
from sxsdiff.generators.github import GitHubStyledGenerator


class ParsrClient():
	def __init__(self, server, revision_history:dict={}):
		self.revision_history = revision_history
		self.set_server(server)
		self.set_current_request_id("")

	def __supported_input_files(self) -> list:
		return ['*.pdf', '*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif',]

	def set_server(self, server:str):
		self.server = server

	def set_current_request_id(self, request_id:str):
		self.request_id = request_id

	def send_document(self, file:str, config:str, server:str="", document_name:str=None, revision:str='major', wait_till_finished:bool=False, refresh_period=2, save_request_id:bool=False, silent:bool=True) -> dict:
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		packet = {
			'file': (file, open(file, 'rb'), 'application/pdf'),
			'config': (config, open(config, 'rb'), 'application/json'),
		}
		r = requests.post('http://'+server+'/api/v1/document', files=packet)
		jobId = r.text
		if not document_name:
			document_name = os.path.splitext(os.path.basename(file))[0]
		if document_name not in self.revision_history:
			self.revision_history[document_name] = { str(semver.VersionInfo.parse('1.0.0')): jobId }
		else:
			latest_revision = max(semver.VersionInfo.parse(i) for i in list(self.revision_history[document_name].keys()))
			if revision == 'major':
				new_revision = latest_revision.bump_major()
			elif revision == 'minor':
				new_revision = latest_revision.bump_minor()
			self.revision_history[document_name][str(new_revision)] = jobId
		if save_request_id:
			self.set_current_request_id(jobId)
		if not wait_till_finished:
			return {'file': file, 'config': config, 'status_code': r.status_code, 'server_response': r.text}
		else:
			print('> Polling server for the job {}...'.format(jobId))
			server_status_response = self.get_status(jobId)['server_response']
			while ('progress-percentage' in server_status_response):
				if not silent:
					print('>> Progress percentage: {}'.format(server_status_response['progress-percentage']))
				time.sleep(refresh_period)
				server_status_response = self.get_status(jobId)['server_response']
			print('>> Job done!')
			return {'file': file, 'config': config, 'status_code': r.status_code, 'server_response': r.text}

	def get_request_id(self, document_name:str, revision:str) -> str:
		if document_name in self.revision_history:
			if revision in self.revision_history[document_name].keys():
				return self.revision_history[document_name][revision]
			else:
				print('Revision {} not found for document {}'.format(revision, document_name))
		else:
			print('Document name {} not found'.format(document_name))
		return ""

	def get_revisions(self, document_name:str) -> list:
		if document_name in self.revision_history:
			return list(self.revision_history[document_name].keys())
		else:
			return []

	def get_document_name_from_request_id(self, request_id:str) -> str:
		for document_name in list(self.revision_history.keys()):
			if request_id in [self.revision_history[document_name][i] for i in list(self.revision_history[document_name])]:
				return document_name
		return ""

	def compare_revisions(self, document_name:str, revisions:list = [], pretty_html:bool = False) -> list:
		diffs = []
		if len(revisions) == 0:
			revisions = self.get_revisions(document_name)
		request_ids = [self.get_request_id(document_name, i) for i in revisions]
		for i in range(0, len(request_ids) - 1):
			request_id1 = request_ids[i]
			request_id2 = request_ids[i + 1]
			md1 = self.get_markdown(request_id1)
			md2 = self.get_markdown(request_id2)

			if pretty_html:
				sxsdiff_result = DiffCalculator().run(md1, md2)
				html_store = StringIO()
				GitHubStyledGenerator(file=html_store).run(sxsdiff_result)
				html_diff = html_store.getvalue()
				diffs.append(html_diff)
			else:
				dmp = diff_match_patch.diff_match_patch()
				diff = dmp.diff_main(md1, md2)
				dmp.diff_cleanupSemantic(diff)
				diffs.append(diff)
		return diffs

	def send_documents_folder(self, folder:str, config:str, server:str="") -> list:
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		responses = []
		os.chdir(folder)
		files = [glob.glob(e) for e in self.__supported_input_files()]
		files_flat = list(chain.from_iterable(files))
		for file in files_flat:
			packet = {
				'file': (file, open(file, 'rb'), 'application/pdf'),
				'config': (config, open(config, 'rb'), 'application/json'),
			}
			r = requests.post('http://'+server+'/api/v1/document', files=packet)
			responses.append({'file': file, 'config': config, 'status_code': r.status_code, 'server_response': r.text})
		return responses

	def get_status(self, request_id:str="", server:str=""):
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		if request_id == "":
			if self.request_id == "":
				raise Exception('No request ID provided')
			else:
				request_id = self.request_id
		if self.server == "":
			raise Exception('No server address provided')
		r = requests.get('http://{}/api/v1/queue/{}'.format(server, request_id))
		return {'request_id': request_id, 'server_response': json.loads(r.text)}

	def get_json(self, request_id:str="", server:str=""):
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		if request_id == "":
			if self.request_id == "":
				raise Exception('No request ID provided')
			else:
				request_id = self.request_id
		r = requests.get('http://{}/api/v1/json/{}'.format(server, request_id))
		if r.text != "":
			return r.json()
		else:
			return {'request_id': request_id, 'server_response': r.json()}

	def get_markdown(self, request_id:str="", server:str=""):
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		if request_id == "":
			if self.request_id == "":
				raise Exception('No request ID provided')
			else:
				request_id = self.request_id
		r = requests.get('http://{}/api/v1/markdown/{}'.format(server, request_id))
		if r.text != "":
			return r.text
		else:
			return {'request_id': request_id, 'server_response': r.text}

	def get_text(self, request_id:str="", server:str=""):
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		if request_id == "":
			if self.request_id == "":
				raise Exception('No request ID provided')
			else:
				request_id = self.request_id
		r = requests.get('http://{}/api/v1/text/{}'.format(server, request_id))
		if r.text != "":
			return r.text
		else:
			return {'request_id': request_id, 'server_response': r.text}

	def get_tables_info(self, request_id:str=""):
		return [(table.rsplit('/')[-2], table.rsplit('/')[-1]) for table in ast.literal_eval(self.get_table(request_id=request_id).columns[0])]

	def get_table(self, request_id:str="", page=None, table=None, seperator=";", server:str="", column_names:list=None):
		if server == "":
			if self.server == "":
				raise Exception('No server address provided')
			else:
				server = self.server
		if request_id == "":
			if self.request_id == "":
				raise Exception('No request ID provided')
			else:
				request_id = self.request_id
		if page is None and table is None:
			r = requests.get('http://{}/api/v1/csv/{}'.format(server, request_id))
		else:
			r = requests.get('http://{}/api/v1/csv/{}/{}/{}'.format(server, request_id, page, table))
		if r.text != "":
			try:
				df = pd.read_csv(StringIO(r.text), sep=seperator, names=column_names)
				df.loc[:, ~df.columns.str.match('Unnamed')]
				df = df.where((pd.notnull(df)), " ")
				return df
			except Exception as e:
				return r.text
		else:
			return r.text
