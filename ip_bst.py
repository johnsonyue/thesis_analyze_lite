class ip_bst():
	def __init__(self):
		self.bst = { '0' : {} }
		self.ip_cnt = 0
	
	def has_key_ip(self, ip):
		bin = self.pfx2bin(ip.split('.',1)[1], 24)
		class_a = ip.split('.')[0]
		if (not self.bst.has_key(class_a)):
			return False
		
		ptr = self.bst[class_a]
		for b in bin:
			if not ptr.has_key(b):
				return False
			ptr = ptr[b]
		
		return True
	
	def insert_key_ip(self, ip, value):
		bin = self.pfx2bin(ip.split('.',1)[1], 24)
		class_a = ip.split('.')[0]
		if (not self.bst.has_key(class_a)):
                        self.bst[class_a] = {}

                ptr = self.bst[class_a]
                for b in bin:
                        if not ptr.has_key(b):
                                ptr[b] = {}
                        ptr = ptr[b]

                ptr["value"] = value
		self.ip_cnt = self.ip_cnt + 1
	
	def byte2bin(self, dec):
                result = []
                for i in range(8):
                        result.append(0)

                for i in range(8):
                        result[i] = dec % 2
                        dec = dec / 2

                result.reverse()
                return result

        def pfx2bin(self, pfx, msk):
                bin = []
                list = pfx.split('.')

		for i in range(len(list)):
                        if(msk <= 0):
                                break
                        bits = (8 if msk/8 else msk%8)
                        byte =  self.byte2bin(int(list[i]))
                        bin.extend(byte[:bits])
                        msk = msk - bits

                return bin
