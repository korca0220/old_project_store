import ctypes

class CRFParser:

	# Initialize
	def __init__(self, lang):
		# Input
		self.lang = lang.upper()
		self.cls_file =".\\Input\\SLM\\{}_SLM.cls".format(self.lang).encode()
		self.cls_module = ctypes.WinDLL(".\\Source\\CRF.dll")

		# CLS Parameter Init
		"""
		unsigned int mzCRFOpen(char *ptPath)
		char *mzCRFOpen(char* psReference, char* psOut)
		"""
		self.cls_module.mzCRFOpen.argtypes = [ctypes.c_char_p,]
		self.cls_module.mzCRFResult.argtypes = [ctypes.c_char_p, ctypes.c_char_p,]
		self.cls_module.mzCRFResult.restype = ctypes.c_char_p

		# Run initialize
		self.cls_module.mzCRFOpen(self.cls_file)

	def parser(self, intput_str):
		temp_str = intput_str.encode()
		_ = "".encode()

		crf = self.cls_module.mzCRFResult(temp_str, _).decode('utf-8').split("\f")

		return crf[0]

	def closeCRF(self):
		self.cls_module.mzCRFClose()
