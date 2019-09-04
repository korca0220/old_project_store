import json
import re

class JSONParser:

	# Initialize
	def __init__(self, lang="ENU"):
		self.lang=lang
		self.reInit()

		self.pcm = None
		self.name = None

		self.result_dict = {}

	def reInit(self):
		self.hash_ref = re.compile('^ref')
		self.hash_remote = re.compile('^remotehyp')

	# ServerBatch 결과 파싱
	def parser(self):
		self.temp_file = "..\out\TEMP.res"
		with open(self.temp_file, "r", encoding='utf-8') as normalFile:
			lines = normalFile.readlines()
			for line in lines:
				result_type = "server"
				slot = {}
				slot_parse = {}
				if self.hash_ref.match(line):
					ref_line = line.split('#')
					self.name = ref_line[2]
					self.pcm = ref_line[1].split('\\')[-1]
					pcm_name = self.name+" "+self.pcm


				if self.hash_remote.match(line):
					remote_line = line.replace("\\;", ";").replace("\\#", "#")\
										.replace("\\\\\"", "").split("#")
					remote_line = "#".join(remote_line[3:])
					i = json.loads(remote_line)
					try:
						if i["appserver_results"]["final_response"]:
							actions = i["appserver_results"]["payload"]["actions"]
							try:
								interpretations = (actions[0]["Input"]["Interpretations"][0].replace("\n", ""))
								domain = (actions[0]["Instances"][0]["nlu_classification"]["Domain"])
								intention = (actions[0]["Instances"][0]["nlu_classification"]["Intention"])
								confidence = str(actions[0]["Instances"][0]["intent_confidence"])
							except:
								interpretations = (actions[1]["Input"]["Interpretations"][0].replace("\n", ""))
								domain = (actions[1]["Instances"][0]["nlu_classification"]["Domain"])
								intention = (actions[1]["Instances"][0]["nlu_classification"]["Intention"])
								confidence = str(actions[1]["Instances"][0]["intent_confidence"])
							try:
								if 'nlu_slot_details' in actions[0]["Instances"][0]:
									try:
										slot = actions[0]["Instances"][0]['nlu_slot_details']
									except:
										slot = actions[1]["Instances"][0]['nlu_slot_details']
							except:
								try:
									if 'nlu_slot_details' in actions[1]["Instances"][0]:
										try:
											slot = actions[0]["Instances"][0]['nlu_slot_details']
										except:
											slot = actions[1]["Instances"][0]['nlu_slot_details']
								except:
									pass
						else:
							continue

						if "UDE" in domain:

							try:
								slot_parse['Name'] = slot['Name']['literal']
								slot_parse['Location'] = slot['Location']['literal']
								# slot = [slot['Name']['literal'], slot['Location']['literal']]
							except:
								try:
									slot_parse['Location'] = slot['Location']['literal']
									# slot = [slot['Location']['literal']]
								except:
									pass
								try:
									slot_parse['Name'] = slot['Name']['literal']
									# slot = [slot['Name']['literal']]
								except:
									pass

							try:
								slot_parse['Category'] = slot['Category']['literal']
								# slot = [slot['Category']['literal']]
							except:
								pass

						elif "SMS" in domain:
							try:
								slot_parse['Contact-name'] = slot['Contact-name']['literal']
								slot_parse['Message-body'] = slot['Message-body']['literal']
								# slot = [slot['Contact-name']['literal'],slot['Message-body']['literal']]
							except:
								try:
									slot_parse['Contact-name'] = slot['Contact-name']['literal']
									# slot = [slot['Contact-name']['literal']]
								except:
									pass
								try:
									slot_parse['Message-body'] = slot['Message-body']['literal']
									# slot = [slot['Message-body']['literal']]
								except:
									pass

						else: continue

						self.result_dict[pcm_name] = [1, interpretations, domain, \
							intention, slot_parse, result_type]

					except KeyError as e:
						pass
						errorString = "Status : {}".format(i["_status"]), \
										"Message : {}".format(e)
						result_type = "error"
						self.result_dict[pcm_name] = [1, errorString, result_type]

			return self.result_dict
