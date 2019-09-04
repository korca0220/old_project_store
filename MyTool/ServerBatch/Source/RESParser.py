import os
import re
from collections import OrderedDict

class RESParser(object):

	# Initialize
	def __init__(self, files):
		self.select_file = files+".res"
		self.contain_dict ={}
		self.contain_key = ""
		self.reInit()

		# REF Init
		self.pcm = None
		self.ref = None
		self.name = None
		self.ref_slot = None
		self.ref_list = []

		# HYP Init
		self.n_best = None
		self.ctx = None
		self.hyp = None
		self.confidence = None
		self.score = None
		self.lm_score = None
		self.slot_word = {}
		self.hyp_list = []

	# Regular Expression Init
	def reInit(self):
		self.hash_ref = re.compile('^ref')
		self.hash_hyp = re.compile('^hyp')
		self.hash_hyp_trash = re.compile(";?([A-Z]+|[A-Z]+_[A-Z]+)\\\\")
		self.hash_slot = re.compile("SLOT_?[A-Z_?]+")
		self.hash_slot_word = re.compile("[A-Z]+[_?A-Z]+\\\\SLOT_?[A-Z_?]+[_?@?;?-?a-zA-Z<.>0-9\s?]+[\\\\#]?")
		self.hash_slot_trash = re.compile("[A-Z]+[_?A-Z]+\\\\#?")
		self.hash_res_slot = re.compile("SLOT+[_?A-Z]+")


	# Parser
	def parser(self):
		self.select_file = '.\\Input\\'+self.select_file
		with open(self.select_file, "r", encoding='utf-8') as sf:
			lines = sf.readlines()
			result_type = "embedded"
			for line in lines:
				#REF Parsing
				if self.hash_ref.match(line) != None:
					ref_temp = line.split('#')
					self.pcm = ref_temp[1].split('\\')[-1]
					self.ref = ref_temp[-4]
					self.name = ref_temp[2]
					self.ref_slot = self.resSlotWord(ref_temp[-3])
					original_sentence = "#".join(ref_temp[:3])
					self.category = ref_temp[-3].split("@")[0]
					self.ref_list.append([self.pcm, self.name, self.ref,\
					 					self.ref_slot, self.category, \
										original_sentence])
					self.contain_key = self.name+" "+self.pcm
					self.contain_dict[self.contain_key] = self.ref_list[-1]

				#HYP Parsing
				if self.hash_hyp.match(line) != None:
					hyp_temp = line.split('#')
					self.n_best = hyp_temp[1]
					self.ctx = hyp_temp[2]
					self.hyp = ''.join(hyp_temp[4:-9])
					self.slot_word = self.hypSlotWord(self.hyp)
					self.hyp = self.hash_hyp_trash.sub("", self.hyp).replace(";", " ")
					self.hyp = self.hash_slot.sub("", self.hyp).replace(", ", "").replace(" '", "'")
					if self.slot_word != None:
						intention_sentence = self.dictionarySearch(self.hyp, self.slot_word)
					else: intention_sentence = self.hyp
					self.confidence = hyp_temp[-9]
					self.score = hyp_temp[-8]
					self.lm_score = hyp_temp[-7]
					self.hyp_list.append([self.n_best, self.ctx, self.hyp, \
								self.slot_word, self.confidence, self.score, \
							 	self.lm_score, intention_sentence, result_type])
					self.contain_dict[self.contain_key].append(self.hyp_list[-1])
			# self.contain_dict=self.nameNbestSort(self.contain_dict)
		return self.contain_dict

	def compareToSlot(self, ref, hyp):
		if ref and hyp:
			cmp_key = list(zip(ref.keys(), hyp.keys()))
			cmp_value = list(zip(ref.values(), hyp.values()))
		else: return False

		for i in cmp_key:
			if i[0] == i[1]: pass
			else: return False
		for i in cmp_value:
			if i[0] == i[1]: pass
			else: return False

		return True

	def nameNbestSort(self, sort_dict):
		for i in sort_dict:
			category = sort_dict[i][4]
			index = [index for index in range(4) if category=="WaitServerCall" or\
													category=="SMS"]
			for j in index:
				if self.compareToSlot(sort_dict[i][3],\
										sort_dict[i][6+j][3]):
					sort_dict[i][6] = sort_dict[i][6+j]
				else: pass
		return sort_dict

	# 필요없는 문장들을 제거하고 Dictionary형태로 SLOT 사전 반환
	# { SLOT_NAME : SLOT value }
	def hypSlotWord(self, hyp):
		temp_dict = {}
		if self.hash_slot_word.findall(hyp):
			word = self.hash_slot_word.findall(hyp)
			for i in word:
				i = self.hash_slot_trash.sub("", i)
				if i.split(";")[0] not in temp_dict:
					i = i.split(";")
					temp_dict[i[0]] = " ".join(list(filter(lambda x : x != '', i[1:])))
			return temp_dict
		return {}

	# REF 문장중 SLOT 이름만 파싱
	def resSlotWord(self, ref):
		temp_dict = {}
		if self.hash_res_slot.findall(ref):
			word = self.hash_res_slot.findall(ref)
			ref = ref.split("@")[2::2]
			for i, j in enumerate(word):
				if j not in temp_dict:
					temp_dict[j] = ref[i].replace(u'\xa0', u'').strip()
			return temp_dict
		return {}

	# HYP 문장중 SLOT Value를 SLOT_NAME으로 replace
	def dictionarySearch(self, strr, slot):
		for i in slot.items():
			strr = strr.replace(i[1], "<{}>".format(i[0]))

		return strr
