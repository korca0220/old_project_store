#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime, date

class BatchBatch:


	def __init__(self, *arg):
		self.date_today = datetime.today().strftime("%Y%m%d")

		self.load_chedck = arg[0]
		self.platform = arg[1]
		self.country = arg[2]
		self.lang = arg[3]
		self.car = arg[4]
		self.acmod = arg[5]
		self.sound = arg[6]
		self.origin_path = ""
		self.hrl_name = ""
		self.hrl_path = ""

		self.clean_noise_regex = re.compile("[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"][Clean, Noise]+$")

		try: # description이 존재할 경우에
			if arg[7]:
				self.description = arg[7]
				self.path = "{platform}\\{country}\\{car}\\{lang}\\{date}_{des}".\
					format(platform=self.platform, country=self.country, \
						lang=self.lang, car=self.car, date=self.date_today, des=self.description)
				self.full_name = "{platform}_{car}_{lang}_{des}".\
					format(platform=self.platform, lang=self.lang, \
						car=self.car, des=self.description)
				self.date_path = self.date_today+"_"+self.description

		except: # description이 존재하지 않을 경우에
			self.path = "{platform}\\{country}\\{car}\\{lang}\\{date}".\
				format(platform=self.platform, lang=self.lang,
					country=self.country, car=self.car, date=self.date_today)
			self.full_name = "{platform}_{car}_{lang}_". \
				format(platform=self.platform, lang=self.lang, car=self.car)
			self.date_path = self.date_today


	def make_dir(self, mode="Clean"):
		from subprocess import call

		self.origin_path = self.path
		self.path = self.path+"-{}".format(mode)
		self.hrl_path = self.path
		self.hrl_path = self.clean_noise_regex.sub("", self.hrl_path)
		ctx_path = "{platform}\\{country}\\{car}\\{lang}".\
			format(platform=self.platform, country=self.country, \
					car=self.car, lang=self.lang)
		try:
			# cfg path
			call(["md", "..\\..\\data\\cfg\\{path}".format(\
										path=self.path)], shell=True)
			# HRL path
			call(["md", "..\\..\\data\\hrl\\{path}".format(\
										path=self.hrl_path)], shell=True)
			# ctx path
			call(["md", "..\\..\\data\\ctx\\{path}".format(\
										path=ctx_path)], shell=True)
			# output path
			call(["md", "..\\..\\data\\out\\{path}".format(\
										path=self.path)], shell=True)
			return True
		except:
			return False

	def overwriteCheck(self, target):
		import os

		overwrite_count = 1

		while True:
			if os.path.exists(target):
				overwrite_count += 1
				change_full_name = self.full_name+"_{}".format(overwrite_count)
				target = "..\\..\\data\\cfg\\{path}\\{name}.ini".format(\
					path=self.path, name=change_full_name)
				continue
			else:
				return target

	def make_ini(self, context, mode="Clean"):
		import configparser
		import os
		from shutil import copyfile

		origin_full_name = self.full_name
		self.full_name = self.full_name+"-{}".format(mode)
		config_loaded = configparser.ConfigParser()
		config_default = configparser.ConfigParser()

		self.default_lines = ""
		target = "..\\..\\data\\cfg\\{path}\\{name}.ini".format(\
			path=self.path, name=self.full_name, mode=mode)

		if self.clean_noise_regex.findall(self.full_name):
			 self.hrl_name = self.clean_noise_regex.sub("", self.full_name)
		else: self.hrl_name = self.full_name

		# target overwrite check loop
		target = self.overwriteCheck(target)

		# hrl_data = self.clean_noise_regex.sub("", self.date_path)
		try:
			if self.load_chedck:
				copyfile(self.load_chedck, ".\\temp.ini")
				try:
					config_loaded.read(".\\temp.ini", encoding="utf-8-sig")
				except:
					config_loaded.read(".\\temp.ini", encoding="utf-16")

				config_default.read("..\\_default\\{context}\\default_{lang}.ini".\
					format(context=context, lang=self.lang), encoding="utf-8-sig")

				# default config parameter load - start
				LOGFILE = config_default['GLOBAL']['LOGFILE']
				TEST_SETTINGS_LOGFILE = config_default['GLOBAL']['TESTSETTINGSLOGFILE']
				TEST_TIMINGHEAP_LOGFL = config_default['GLOBAL']['TESTTIMINGHEAPLOGFL']
				HRLFILE = config_default['GLOBAL']['HRLFILE']
				SOUND_DIR_PATH = config_default['GLOBAL']['SOUNDDIRPATH']

				CTX1FILES = config_default['TEST1']['CTX1FILES']
				RESULT_FILE = config_default['TEST1']['RESULTFILE']
				PARAMETER_DUMP_FILE = config_default['TEST1']['PARAMETERDUMPFILE']
				HEAP_STATISTICS_FILE = config_default['TEST1']['HEAPSTATISTICSFILE']

				SLOTCTXFILENAME = config_default['TEST1_CTX1_SL1']['SLOTCTXFILENAME']
				# end

				# set loaded config parameter - start
				try:
					config_loaded['GLOBAL']['LOGFILE'] = LOGFILE
					config_loaded['GLOBAL']['TESTSETTINGSLOGFILE'] = TEST_SETTINGS_LOGFILE
					config_loaded['GLOBAL']['TESTTIMINGHEAPLOGFL'] = TEST_TIMINGHEAP_LOGFL
					config_loaded['GLOBAL']['HRLFILE'] = HRLFILE
					config_loaded['GLOBAL']['SOUNDDIRPATH'] = SOUND_DIR_PATH

					config_loaded['TEST1']['CTX1FILES'] = CTX1FILES
					config_loaded['TEST1']['RESULTFILE'] = RESULT_FILE
					config_loaded['TEST1']['PARAMETERDUMPFILE'] = PARAMETER_DUMP_FILE
					config_loaded['TEST1']['HEAPSTATISTICSFILE'] = HEAP_STATISTICS_FILE

					config_loaded['TEST1_CTX1_SL1']['SLOTCTXFILENAME'] = SLOTCTXFILENAME
				except:
					pass
				# end

				with open(".\\temp.ini", "w+", encoding="utf-8-sig" ) as default:
					config_loaded.write(default)

				with open(".\\temp.ini", "r", encoding="utf-8-sig") as default:
					self.default_lines = default.readlines()

				os.remove(".\\temp.ini")

			else:
				try:
					with open("..\\_default\\{context}\\{platform}\\default_{lang}.ini".\
						format(context=context, platform=self.platform, lang=self.lang), "r", encoding='utf-8') as default:
						self.default_lines = default.readlines()

				except:
					with open("..\\_default\\{context}\\default_{lang}.ini".\
						format(context=context, lang=self.lang), "r", encoding='utf-8') as default:
						self.default_lines = default.readlines()

			with open(target, "w+", encoding='utf-8-sig') as target:
				for i in self.default_lines:
					try:
						i = i.replace("description", "{}".format(self.description).upper())
					except:
						pass
					i = i.replace("platform", "{}".format(self.platform).upper())
					i = i.replace("country", "{}".format(self.country).upper())
					i = i.replace("car_model", "{}".format(self.car).upper())
					i = i.replace("full_name", "{}".format(self.full_name).upper())
					i = i.replace("hrl_name", "{}".format(self.hrl_name).upper())
					i = i.replace("model_spec", "{}".format(self.acmod).lower())
					i = i.replace("lang", "{}".format(self.lang).upper())
					i = i.replace("date", "{}".format(self.date_path+"-"+mode).upper())
					i = i.replace("hrl_path", "{}".format(self.date_path).upper())
					i = i.replace("sound_path", "{}\n".format(self.sound).upper())
					target.write(i.upper())

		except Exception as e:
			print(e)
			return False

		self.full_name = origin_full_name
		self.path = self.origin_path
		return True

	def make_server_ini(self):
		with open("..\\_default\\server\\default_server.ini",\
			"r", encoding='utf-8') as default_server:
			server_ini = default_server.readlines()
		with open("..\\..\\data\\cfg\\server\\server_{lang}.ini".format(\
			lang=self.lang), "w+", encoding='utf-8') as server:
			for i in server_ini:
				i = i.replace("TEMP_lang", "server_{}".format(self.lang))
				server.write(i)

	def make_hrl(self):
		with open("..\\..\\data\\\hrl\{path}\{name}.hrl".\
			format(lang=self.lang, path=self.hrl_path, name=self.hrl_name), "w+",\
			 		encoding='utf-8') as hrl:
			hrl.write("#head;hrl;2.0;utf-8\n")
			hrl.write("#ref#speechfile#speaker#reference word sequence#category\n")
			hrl.write("head\n")

	def generate(self, context, clean_noise):
		try:
			if clean_noise[0] and clean_noise[1]:
				self.make_dir(mode="Clean")
				self.make_ini(context, mode="Clean")
				self.make_dir(mode="Noise")
				self.make_ini(context, mode="Noise")
			elif not clean_noise[0] and clean_noise[1]:
				self.make_dir(mode="Noise")
				self.make_ini(context, mode="Noise")
			else:
				self.make_dir()
				self.make_ini(context)
			self.make_hrl()
			print("Directory structure founded..")
		except:
			print("Directory structure found fail..")
