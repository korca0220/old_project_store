# -*- coding: utf-8 -*-
import simplejson as json
import sys


def parsingToJson(LANG):

	if LANG == "FRC":
		encoding_char = 'utf-16'
	else:
		encoding_char = None

	with open(".\Input\{0}\{0}_Result.txt".format(LANG), "r".format(LANG), encoding=encoding_char) as jsonF:
		with open("Test_{}.txt".format(LANG), "w+") as wf:

			lines = jsonF.readlines()
			for i in lines:
				if i == "\n" or i[0] == "D":
					continue
				wf.write(i)


def jsonToText(LANG):

	errorCount = 0
	errorPCM = ""
	errorString = ""
	errorDict = {}
	with open("Test_{}.txt".format(LANG), "r") as tf:
		with open(".\Input\{0}\{0}_Result_out.txt".format(LANG), "w+") as wf:
			lines = tf.readlines()
			count = 200
			for i in lines:
				slot = ""
				i = json.loads(i)
				try:
					if i["appserver_results"]["final_response"]:
						count += 1
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
							if 'nlu_slot_details' in actions[1]["Instances"][0]:
								try:
									slot = actions[0]["Instances"][0]['nlu_slot_details']
								except:
									slot = actions[1]["Instances"][0]['nlu_slot_details']

						wf.write("f{}.pcm".format(count)+"\t"+"Interpretations"+"\t"+interpretations+"\t"+\
								"Domain"+"\t"+domain+"\t"+"Intention"+"\t"+intention+"\t"+\
								"intent_confidence"+"\t"+confidence+"\t")
						try:
							for i in slot:
								slotString = slot[i]['literal']
								wf.write("Slot"+"\t"+slotString+"\t")
						except:
							pass

						wf.write("\n")
					else:
						continue
				except KeyError:
					count += 1
					errorCount += 1
					errorPCM = "f{}.pcm".format(count)
					errorString = "Status : {}".format(i["_status"]), \
									"Message : {}".format(i["_errorMessage"])
					errorDict[errorPCM] = errorString

				if count == 300:
					count = 200
			try:
				with open("error_log.txt", "w+", encoding='utf-8') as ef:
					ef.write("Error : {}\n".format(errorCount))
					try:
						for i in errorDict:
							ef.write("PCM : {}".format(i)+"\t"+"{}".format(errorDict[i]))
					except:
						pass
			except FileNotFoundError:
				print("FileNotFoundError")


if __name__=="__main__":

	parsingToJson(sys.argv[1])
	jsonToText(sys.argv[1])
