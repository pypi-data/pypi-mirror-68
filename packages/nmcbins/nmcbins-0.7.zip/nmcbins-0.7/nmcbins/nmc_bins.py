# 2020.3.24 LN Client will use this python module on their web server to access NMC Language Normalization Service.
import requests
import json
nmc_ln_host_session = None
nmc_ln_host = "http://www.nmcomputing.com"
#nmc_ln_host = "http://192.168.1.66"
qid = None

def setQid(_qid):
	global qid
	qid=_qid

def normalize(text_to_process):
	global nmc_ln_host_session  # persistent HTTP connection to node.js server.
	if qid is None:
		return 'Error: qid not set!'
	s = ''
	if not qid or not text_to_process:
		return "Error: missing qid or text_to_process"
	if nmc_ln_host_session is None:
		nmc_ln_host_session = requests.Session()
	#qString =nmc_ln_host + "LNconvert?uid="+uid+"&text_to_process="+_text_to_process
	url = nmc_ln_host + "/ln/normalize/"
	#nodejs_response = nmc_ln_host_session.get(qString)  
	_data = {'qid': qid, 'text_to_process':text_to_process}
	nodejs_response = requests.post(url, data = json.dumps(_data))
	
	if not nodejs_response:
		s += "Error connecting to bins server!"
	else:
		s=nodejs_response.text  #.text: utf-8,  .content:  raw bytes.

	return s
