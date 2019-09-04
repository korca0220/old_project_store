import os
import sys

def makeAndCopy(ini_full_path, ini_path, orgin_ini_path, ctx_path, out_path, origin_ctx):
	from subprocess import call

	call(["mkdir", ini_path], shell=True)
	call(["mkdir", ctx_path], shell=True)
	call(["mkdir", out_path], shell=True)
	call(["copy", orgin_ini_path, ini_full_path], shell=True)
	call(["xcopy", origin_ctx, ctx_path, "/e", "/y"], shell=True)

def gen(args, domains):
	import re

	origin_sound_path = re.compile("SOUND/.*")
	origin_date = re.compile("[0-9]{8}")
	hrl = re.compile("HRL")

	for i in args:
		if i == "":
			print("Please, fill empty Value")
			return
		else: pass
	zone, platform, car, date, convert_car, sound, convert_date = args
	domain_list = domains.split(",")

	if zone == "KOR":
		langs = ["KOK"]
	elif zone == "USA":
		langs = ["ENU", "FRC", "SPM"]
	elif zone == "EUR":
		langs = ["CZC", "DAD", "DUN", "ENG", "FIF", "FRF", "GED", "ITI", "NON",\
				"PLP", "PTP", "RUR", "SPE", "SWS", "TRT"]
		langs_VDE = ["DUN", "ENG", "FRF", "GED", "ITI", "SPE"]

	for lang in langs:
		for domain in domain_list:
			try:
				ini = "{platform}_{convert}_{lang}_{domain}-Noise.ini".format(\
					platform=platform, lang=lang, convert=convert_car, domain=domain)

				origin_ini = "{platform}_{car}_{lang}_{domain}-Clean.ini".format(\
					platform=platform, lang=lang, car=car, domain=domain)
				origin_ctx = ".\\data\\ctx\\{platform}\\{zone}\\{car}\\{lang}".\
				format(platform=platform, zone=zone, lang=lang, car=car)

				ini_path = ".\\data\\cfg\\{platform}\\{zone}\\{convert}\\{lang}\\{dir}".\
				format(platform=platform, zone=zone, lang=lang, convert=convert_car,\
						dir=convert_date+"_"+domain+"-Noise")
				ctx_path = ".\\data\\ctx\\{platform}\\{zone}\\{convert}\\{lang}".\
				format(platform=platform, zone=zone, lang=lang, convert=convert_car)
				out_path = ".\\data\\out\\{platform}\\{zone}\\{convert}\\{lang}\\{dir}".\
				format(platform=platform, zone=zone, lang=lang, convert=convert_car,\
						dir=convert_date+"_"+domain+"-Noise")


				origin_ini_path = ".\\data\\cfg\\{platform}\\{zone}\\{car}\\{lang}\\{dir}\\{ini}".\
				format(platform=platform, zone=zone, lang=lang, car=car,\
						dir=date+"_"+domain+"-Clean", ini=origin_ini)
				dest_ini_path = ".\\data\\cfg\\{platform}\\{zone}\\{convert}\\{lang}\\{dir}\\{ini}".\
				format(platform=platform, zone=zone, lang=lang, convert=convert_car,\
						dir=convert_date+"_"+domain+"-Noise", ini=ini)

				with open(origin_ini_path, "r", encoding="utf-8") as origin:
					org_file = origin.readlines()

				makeAndCopy(dest_ini_path, ini_path, origin_ini_path, ctx_path, out_path, origin_ctx)

				with open(dest_ini_path, "w", encoding="utf-8") as re_file:
					for i in org_file:
						if not hrl.search(i):
							i = i.replace(car, convert_car)
							i = i.replace("CLEAN", "NOISE")
							i = i.replace("Clean", "NOISE")
							i = re.sub(origin_sound_path, "SOUND/{sound_path}".\
								format(sound_path=sound), i)
							if origin_date.search(i):
								i = i.replace(date, convert_date)
						re_file.write(i)
			except: pass

if __name__ == '__main__':

	gen(sys.argv[1:-1], sys.argv[-1])
