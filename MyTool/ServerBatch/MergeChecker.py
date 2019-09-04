import re
import sys
from Source import CRFParser,\
					RESParser,\
					JSONParser


class MergeChecker:

	# Initialize
	def __init__(self, files, server, nbest=4, lang="enu"):
		self.lang = lang.lower()
		self.files = files
		self.res_obj = RESParser.RESParser(files)
		self.res_data = self.res_obj.parser() # REF/HYP data object
		self.json_obj = JSONParser.JSONParser()
		self.crf_module = CRFParser.CRFParser(lang)
		self.merged_data = {}
		self.nbest = nbest
		self.true_count_intention = 0 # Intention 적중 개수
		self.true_count_slot = 0 # Slot 적중 개수
		self.true_count_total = 0 # Intention + Slot 적중 개수
		self.ref_count = 0 # 정답 문장 개수

		self.server_intention = {'WaitServerCategory':'UDE',\
								'WaitServerSMS':'SMS'}

		self.name_values = ['SLOT_CONTACT_SINGLE',\
							'SLOT_CONTACT_FULL_FIRST',\
							'SLOT_CONTACT_REVERSE_LAST']

		self.path = "..\\data"
		self.server_batch_path = server

		self.gol = re.compile("@$")

	def serverIntentionToHRL(self):
		"""
		if intention is "server intention",
		create temp HRL that constructed only "server intention"
		"""
		with open(self.path+"\\hrl\\TEMP_{lang}.hrl".format(lang=self.lang), "w+") as hrl:
			hrl.write("#head;hrl;2.0;utf-8\n")
			hrl.write("#ref#speechfile#speaker#reference word sequence#category\n")
			hrl.write("head\n")
			for i in self.res_data:
				try:
					sentence = ""
					intention = self.crf_module.parser(self.res_data[i][6][-2])
					if intention in self.server_intention:
						sentence = sentence + self.res_data[i][5]+"#"+self.res_data[i][6][2]+"#"+\
							intention+"@"
						for x in self.res_data[i][6][3]:
							sentence = sentence +"<{}>@".format(x)+self.res_data[i][6][3][x]+"@"
						sentence = self.gol.sub("", sentence)
						hrl.write(sentence + "\n")
				except:
					pass


	def serverHRLToRes(self):
		"""
		server_bach_fl execute "server intention" HRL
		"""
		from subprocess import call
		path = self.path+"\cfg\TEMP_{lang}.ini".format(lang=self.lang)
		call([self.server_batch_path, path], shell=True)
		call(["mkdir", "..\\out"], shell=True)
		call(["move", "..\data\\out\\x86_win32_remote\\TEMP.res".format(self.lang.lower()),\
		 				"..\\out\\TEMP.res"], shell=True)

	def mergeToResult(self):
		self.json_data = self.json_obj.parser()
		result_type = ""
		for i in self.res_data:
			try:
				if i in self.json_data:
					hyp = self.json_data[i][1]
					intention = self.json_data[i][2]
					result_type = self.json_data[i][-1]
					slot = self.json_data[i][4]
					if intention == "SMS" and slot != None:
						slot = self.nameChangeToEmbedded(slot, i, result_type)
					if slot == None: slot=""

				else:
					hyp = self.res_data[i][6][2]
					intention = self.crf_module.parser(self.res_data[i][6][-2])
					confidence = self.res_data[i][6][4]
					result_type = self.res_data[i][6][-1]
					slot = self.res_data[i][6][3]
					if slot == None: slot = ""
					if intention in "WaitServerCall" and slot != None:
						slot = self.nameChangeToEmbedded(slot, i, result_type)
				ref = self.res_data[i][2]
				ref_slot = self.res_data[i][3]
				ref_intention = self.res_data[i][4]

				self.merged_data[i] = [ref, \
									ref_slot, slot, \
									ref_intention, intention, \
									result_type]
			except:
				if self.res_data[i]:
					self.merged_data[i] = ["server rejection"]
				else:
					self.merged_data[i] = ["embedded rejection"]

	# Slot checker
	def compareToSlot(self, ref, hyp):
		key = False
		if ref and hyp:
			cmp_key = list(zip(ref.keys(), hyp.keys()))
			cmp_value = list(zip(ref.values(), hyp.values()))
		else: return False

		for i in cmp_key:
			if i in self.name_values: key==True

		if not key:
			for i in cmp_key:
				if i[0] == i[1]: pass
				else: return False
			for i in cmp_value:
				if i[0] == i[1]: pass
				else: return False
		else:
			for i in cmp_value:
				if i[0] == i[1]: pass
				else: return False

		return True

	def nameChangeToEmbedded(self, slot, i, result):
		count = 0
		while count < 4:
			for key in list(self.res_data[i][6+count][3].keys()):
				if key in self.name_values:
					ref_name = ''.join([self.res_data[i][3][x] for x in self.name_values \
								if x in self.res_data[i][3].keys()])
					if self.res_data[i][6+count][3][key].lower() == ref_name.lower():
						real_name = self.res_data[i][6+count][3][key]
						if result == "server":
							try:
								slot['Contact-name'] = real_name
							except:
								pass
							return slot
						else: # embedded
							for i in self.name_values:
								if i in slot:
									del slot[i]
								else:
									pass
							slot[key] = real_name
							return slot
			count += 1
		return slot

	# Server Slot checker
	def convertToLowerCompare(self, result, other):
		result = [result_convert.lower().strip().\
			replace(".", "").replace("?", "").replace("-", " ").\
			replace(",", "") for result_convert in result]
		other = [other_convert.lower().strip().\
		 	replace(".", "").replace("?", "").replace("-", " ").\
			replace(",", "") for other_convert in other]
		if result == other: return True
		else: return False

	def recognitionCheck(self):
		success = 0
		fail = 0
		for i in self.merged_data:
			try: # if result type is embdded
				if self.merged_data[i][-1] == "embedded":
					intention = self.crf_module.parser(self.res_data[i][6][-2])
					#인텐션이 서버 인텐션인 경우
					if self.res_data[i][4] in list(self.server_intention.values()):
						if intention in self.server_intention:
							fail += 1
							self.merged_data[i][-2] = self.server_intention[intention]
							if self.merged_data[i][-2] != self.merged_data[i][-3]:
								self.merged_data[i][-1] = "server"
								self.merged_data[i].append("Server domain fail")
							else:
								self.merged_data[i][-1] = "server"
								self.merged_data[i].append("Server not result fail")
						else:
							fail += 1
							self.merged_data[i].append("Intention fail")

					else: # 인텐션이 서버가 아닌경우
						  # 정답에 SLOT이 존재 하지 않는 경우
						if not self.res_data[i][3]:
							if self.res_data[i][4] == self.merged_data[i][-2]:
								success += 1
								self.merged_data[i].append("success")
							else:
								fail += 1
								self.merged_data[i].append("Intention fail")

						# 정답에 SLOT이 있는 경우
						elif self.res_data[i][3] and \
							self.res_data[i][4] == self.merged_data[i][-2]:
							if self.compareToSlot(self.res_data[i][3], self.merged_data[i][2]):
								success += 1
								self.merged_data[i].append("success")
							else:
								fail += 1
								self.merged_data[i].append("Slot fail")
						else:
							fail += 1
							self.merged_data[i].append("Intention fail")


				# if result type is server
				elif self.merged_data[i][-1] == "server":
					if i in self.res_data:
						if self.res_data[i][4] == self.merged_data[i][-2]:
							if self.convertToLowerCompare(list(self.res_data[i][3].values()),\
							 								self.merged_data[i][2].values()):
								success += 1
								self.merged_data[i].append("success")
							else:
								fail += 1
								self.merged_data[i].append("Server fail")
						else:
							fail += 1
							self.merged_data[i].append("Server fail")
				else:
					fail += 1
					self.merged_data[i].append("Unexpected domain")
			except:
				pass

		with open(".\\Output\\_merge_result_{}.txt"\
				.format(self.files), "w+", encoding='utf-8') as wf:
			for i in self.merged_data:
				try:
					self.merged_data[i][2] = list(self.merged_data[i][2].values())
				except:
					pass
				name = i.split(" ")[0]
				pcm = i.split(" ")[1]
				wf.write(name+"\t"+pcm+"\t")
				for j in self.merged_data[i]:
					wf.write(str(j)+"\t")
				wf.write("\n")
			wf.write("fail:"+str(fail)+"\t"+"success:"+str(success)+"\n")
			wf.write("recognition rate:"+str(round(success/(fail+success),2)*100)+"%")

		self.crf_module.closeCRF()


if __name__=='__main__':

	checker = MergeChecker(files=sys.argv[1], server=sys.argv[2], lang=sys.argv[3])
	checker.serverIntentionToHRL()
	checker.serverHRLToRes()
	checker.mergeToResult()
	checker.recognitionCheck()
