import threading
from subprocess import call, \
						Popen, \
						PIPE

class BatchGenerate(threading.Thread):

	def __init__(self, arg=None, button=None):
		"""
		platform = arg[0]
		zone = arg[1]
		lang = arg[2]
		car_model = arg[3]
		description =arg[4]
		dir_date = arg[5]
		batch_version = arg[6]

		button = [clean, noise, batchon, batchoff, bnf, slm]
		"""
		threading.Thread.__init__(self)
		self._stop = threading.Event()
		self.lang = arg[2]
		self.platform = arg[0]
		self._check = ""

		if arg[4] != "":
			self.cfg = "{platform}_{lang}_{car}_{des}".\
			format(platform=arg[0], lang=arg[2], car=arg[3], des=arg[4])
			date_des = "{date}_{des}".format(date=arg[5], des=arg[4])
		else:
			self.cfg = "{platform}_{lang}_{car}".\
			format(platform=arg[0], lang=arg[2], car=arg[3])
			date_des = "{date}".format(date=arg[5])

		self.clean_full_path =\
		 "..\\..\\data\\cfg\\{platform}\\{zone}\\{lang}\\{car}\\{date}-Clean\\{cfg}".\
		 format(platform=arg[0], zone=arg[1], lang=arg[2], car=arg[3],\
		 		date=date_des, cfg=self.cfg)

		self.noise_full_path =\
		 "..\\..\\data\\cfg\\{platform}\\{zone}\\{lang}\\{car}\\{date}-Noise\\{cfg}".\
		 format(platform=arg[0], zone=arg[1], lang=arg[2], car=arg[3],\
		 		date=date_des, cfg=self.cfg)

		self.clean_output_path =\
		 "..\\..\\data\\out\\{platform}\\{zone}\\{lang}\\{car}\\{date}-Clean".\
		 format(platform=arg[0], zone=arg[1], lang=arg[2], car=arg[3],\
		 		date=date_des, cfg=self.cfg)

		self.noise_output_path =\
		 "..\\..\\data\\out\\{platform}\\{zone}\\{lang}\\{car}\\{date}-Noise".\
		 format(platform=arg[0], zone=arg[1], lang=arg[2], car=arg[3],\
		 		date=date_des, cfg=self.cfg)

		self.batch_path = "..\\..\\__Batch\\batch_{}\\batch_fl_static.exe".format(arg[6])
		self.scorit_path = "..\\..\\__Batch\\tools\\scorit.exe"
		self.res_phaser_path = "..\\..\\__Batch\\_setting_file\\Res_Phaser.exe"
		self.scorit_phaser_path = "..\\..\\__Batch\\_setting_file\\Score_phaser.exe"
		self.button = button

	def gen(self):
		"""
		선택된 option 에 따라서 수행 방식 결정
		Option = Clean or Noise or Clean+Noise
		         Post Test On or Off
		"""
		self._check = ""
		clean_cfg = self.clean_full_path+"-Clean.ini"
		noise_cfg = self.noise_full_path+"-Noise.ini"
		error = ""
		# clean only
		if self.button[0]:
			if self.button[2]:
				proc = Popen(["start", "/wait", "cmd", "/C", "{batch}".format(batch=self.batch_path),\
				 "{path}".format(path=clean_cfg)], stdout=PIPE, stderr=PIPE, shell=True)
				out, err = proc.communicate()

			try:
				if self.errorTracking():
					# Post off
					if self.button[5]:
						call(["mkdir",  "..\\..\\__Batch\\out\\{_}\\{_}\\CRF".format(_=self.cfg+"-Clean")], shell=True)
						self.bnfGenerate()
						call(["rmdir", "/S", "/Q", self.clean_output_path], shell=True)

					# Post on
					elif self.button[4]:
						call(["mkdir",  "..\\..\\__Batch\\out\\{_}\\{_}\\CRF".format(_=self.cfg+"-Clean")], shell=True)
						call(["mkdir",  "..\\..\\__Batch\\out\\{_}\\{_}_W\\CRF".format(_=self.cfg+"-Clean")], shell=True)
						self.bnfGenerate()
						self.slmGenerate()
					self.moveToOut()
					return ""
				else: return self.clean_output_path+"\\"+self.cfg+"-Clean-LOGSCREEN.txt"
			except:
				print("Check To INI File.{}".format(clean_cfg))


		# noise only
		if self.button[1]:
			if self.button[2]:
				proc = Popen(["start", "/wait", "cmd", "/C", "{batch}".format(batch=self.batch_path),\
				 "{path}".format(path=noise_cfg)], stdout=PIPE, stderr=PIPE, shell=True)
				out, err = proc.communicate()

			try:
				if self.errorTracking(mode="Noise"):
					# Post off
					if self.button[5]:
						call(["mkdir", "..\\..\\__Batch\\out\\{_}\\{_}\\CRF".format(_=self.cfg+"-Noise")], shell=True)
						self.bnfGenerate(mode="Noise")
						call(["rmdir", "/S", "/Q", self.noise_output_path], shell=True)

					# Post on
					# On 상태는 Off 상태일때의 프로세스를 포함한다.
					if self.button[4]:
						call(["mkdir", "..\\..\\__Batch\\out\\{_}\\{_}\\CRF".format(_=self.cfg+"-Noise")], shell=True)
						call(["mkdir", "..\\..\\__Batch\\out\\{_}\\{_}_W\\CRF".format(_=self.cfg+"-Noise")], shell=True)
						self.bnfGenerate(mode="Noise")
						self.slmGenerate(mode="Noise")
					self.moveToOut(mode="Noise")
					return ""
				else: return self.noise_output_path+"\\"+self.cfg+"-Noise-LOGSCREEN.txt"
			except Exception as e:
				print("Check To INI File.{}".format(noise_cfg))

	def errorTracking(self, mode="Clean"):
		if mode =="Clean": full_path = self.clean_output_path
		else: full_path = self.noise_output_path

		with open(full_path+"\\"+self.cfg+"-"+mode+"-LOGSCREEN.txt", "r", encoding="utf-8") as log:
			read = log.read()
			if "error" in read:
				return False
			return True

	def bnfGenerate(self, mode="Clean"):
		"""
		postprocess Off
		"""
		self.copyToOut(mode)
		self.resPhaser(mode)

		call(["rmdir", "/S", "/Q", "..\\..\\__Batch\\out\\{_}\\{_}\\CRF\\".\
		format(_=self.cfg+"-"+mode)], shell=True)

		call(["xcopy", "..\\..\\__Batch\\CRF\\OUT.yml", \
		"..\\..\\__Batch\\out\\{_}\\{_}\\CRF\\".format(_=self.cfg+"-"+mode),\
		"/Y"], shell=True)

		call(["copy", "..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
		format(_=self.cfg+"-"+mode), "..\\..\\__Batch\\scorit\\{_}.res".\
		format(_=self.cfg+"-"+mode)], shell=True)


		call([self.scorit_path, "-m", "..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
		format(_=self.cfg+"-"+mode), "-o",\
		"..\\..\\__Batch\\out\\{_}\\{_}\\{_}_out_ALL.txt".format(_=self.cfg+"-"+mode),\
		"--columnsOfTable=Best-5-SER", "--rejectionThreshold=0"], shell=True)

		call([self.scorit_phaser_path, "..\\..\\__Batch\\out\\{_}\\{_}\\{_}_out_ALL.txt".\
		format(_=self.cfg+"-"+mode),\
		"..\\..\\__Batch\\out\\{_}\\{_}\\{_}_out_ALL.out".\
		format(_=self.cfg+"-"+mode)], shell=True)

	def slmGenerate(self, mode="Clean"):
		"""
		postprocess On
		"""
		self.copyToOut(mode, nlu="on")
		self.resPhaser(mode, nlu="on")

		call(["rmdir", "/S", "/Q", "..\\..\\__Batch\\out\\{_}\\{_}_W\\CRF\\".\
		format(_=self.cfg+"-"+mode)], shell=True)

		call(["xcopy", "..\\..\\__Batch\\CRF\\OUT.yml", \
		"..\\..\\__Batch\\out\\{_}\\{_}_W\\CRF\\".format(_=self.cfg+"-"+mode), "/Y"], shell=True)

		call(["copy", "..\\..\\__Batch\\out\\{_}\\{_}_W\\{_}.res".\
		format(_=self.cfg+"-"+mode), "..\\..\\__Batch\\scorit\\{_}.res".\
		format(_=self.cfg+"-"+mode)], shell=True)

		call([self.scorit_path, "-m", "..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
		format(_=self.cfg+"-"+mode), "-o",\
		"..\\..\\__Batch\\out\\{_}\\{_}_W\\{_}_out_ALL.txt".format(_=self.cfg+"-"+mode),\
		"--columnsOfTable=Best-5-SER", "--rejectionThreshold=0"], shell=True)

		call([self.scorit_phaser_path, "..\\..\\__Batch\\out\\{_}\\{_}\\{_}_out_ALL.txt".\
		format(_=self.cfg+"-"+mode),\
		"..\\..\\__Batch\\out\\{_}\\{_}_W\\{_}_out_ALL.out".\
		format(_=self.cfg+"-"+mode)], shell=True)

	def copyToOut(self, mode, nlu="off"):

		if mode =="Clean": full_path = self.clean_output_path
		else: full_path = self.noise_output_path
		if nlu=="on":
			__ = self.cfg+"-"+mode+"_W"
			cmd = "move"
		else :
			__ = self.cfg+"-"+mode
			cmd = "copy"
		_ = self.cfg+"-"+mode
		call([cmd,\
		 full_path+"\\"+self.cfg+"-{mode}-SETTING.log".\
		 format(mode=mode),\
		 "..\\..\\__Batch\\out\\{_}\\{__}\\{_}-SETTING.log".\
		 format(_=_, __=__)], shell=True)

		call([cmd,\
		 full_path+"\\"+self.cfg+"-{mode}-TIMING.csv".\
		 format(mode=mode),\
		 "..\\..\\__Batch\\out\\{_}\\{__}\\{_}-TIMING.csv".\
		 format(_=_, __=__)], shell=True)

		call([cmd,\
		 full_path+"\\"+self.cfg+"-{mode}-DUMP.txt".\
		 format(mode=mode),\
		 "..\\..\\__Batch\\out\\{_}\\{__}\\{_}-DUMP.txt".\
		 format(_=_, __=__)], shell=True)

		call([cmd,\
		 full_path+"\\"+self.cfg+"-{mode}-HEAP.txt".\
		 format(mode=mode),\
		 "..\\..\\__Batch\\out\\{_}\\{__}\\{_}-HEAP.txt".\
		 format(_=_, __=__)], shell=True)

		call([cmd,\
		 full_path+"\\"+self.cfg+"-{mode}-LOGSCREEN.txt".\
		 format(mode=mode),\
		 "..\\..\\__Batch\\out\\{_}\\{__}\\{_}-LOGSCREEN.txt".\
		 format(_=_, __=__)], shell=True)

		call(["copy",\
		 full_path+"\\"+self.cfg+"-{mode}.res".\
		 format(mode=mode),\
		 "..\\..\\__Batch\\out\\{_}\\{__}\\{_}_org.res".\
		 format(_=_, __=__)], shell=True)

	def resPhaser(self, mode, nlu="off"):

		if mode =="Clean": full_path = self.clean_output_path
		else: full_path = self.noise_output_path
		if nlu != "on":
			call([self.res_phaser_path,\
			full_path+"\\"+self.cfg+"-{mode}.res".\
			format(mode=mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}_NBEST.txt".\
			format(_=self.cfg+"-"+mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
			format(_=self.cfg+"-"+mode), "0"], shell=True)

			call([self.res_phaser_path,\
			full_path+"\\"+self.cfg+"-{mode}.res".\
			format(mode=mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}_ONEBEST.txt".\
			format(_=self.cfg+"-"+mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
		 	format(_=self.cfg+"-"+mode), "1"], shell=True)

			call([self.res_phaser_path,\
			full_path+"\\"+self.cfg+"-{mode}.res".\
			format(mode=mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}_ONEBESTALL.txt".\
			format(_=self.cfg+"-"+mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
			format(_=self.cfg+"-"+mode), "2"], shell=True)

			call([self.res_phaser_path,\
			full_path+"\\"+self.cfg+"-{mode}.res".\
			format(mode=mode), "..\\..\\__Batch\\CRF\\OUT.yml",\
			"..\\..\\__Batch\\out\\{_}\\{_}\\{_}.res".\
			format(_=self.cfg+"-"+mode), "3",\
			"..\\..\\__Batch\\_setting_file\\input.txt"], shell=True)

		else:
			call(["..\\..\\__Batch\\_setting_file\\Res_Phaser_weight.exe",\
			full_path+"\\"+self.cfg+"-{mode}.res".format(mode=mode),\
			"..\\..\\__Batch\\out\\{_}\\{_}_W\\".format(_=self.cfg+"-"+mode),\
			self.cfg+"-"+mode, "..\\..\\__Batch\\_setting_file\\CONFIGFILE\\{platform}\\CONFIGFILE_{lang}.txt".\
			format(platform=self.platform, lang=self.lang)], shell=True)

			call(["del",\
			 full_path+"\\"+self.cfg+"-{mode}.res".\
			 format(mode=mode)], shell=True)

	def moveToOut(self, mode="Clean"):
		if mode =="Noise": path = self.noise_output_path
		else : path = self.clean_output_path
		call(["xcopy", "..\\..\\__Batch\\out\\{_}".format(_=self.cfg+"-"+mode),\
			path+"\\", "/Y", "/E"], shell=True)


	def run(self):
		self._check = self.gen()
		if not self._check:
			self._stop.set()
		else:
			print("Batch execute fail, Please confirm error from LOGSCREEN file")
			self._stop.set()
			call([self._check], shell=True)
