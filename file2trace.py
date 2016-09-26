import sys

def is_notation_caida(line):
	return line.split('\t')[1][0] == "#"
	
def build_caida():
	sys.stderr.write("started parsing caida ...\n")
	try:
		while True:
			line=raw_input()
			if (not is_notation_caida(line)):
				sections = line.strip('\n').split('\t')

				sys.stdout.write(sections[0]+'\t'+sections[7]+'\t'+sections[3])
				for i in range(14,len(sections)):
					if sections[i] == "q":
						continue
					sys.stdout.write('\t'+sections[i].split(';')[0])
				print
	except Exception, ex:
		sys.stderr.write("finished parsing caida.\n")
		return

if __name__ == "__main__":
	build_caida()
