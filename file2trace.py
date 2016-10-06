import sys
import re

def is_notation_caida(line):
	return line.split('\t')[2][0] == "#"
	
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

def output_lg_trace(target_ip, trace_list):
	if target_ip == trace_list[-1]:
		is_replied = "R"
	else:
		is_replied = "N"
	sys.stdout.write("lg\t"+is_replied+"\t"+target_ip)
	for h in trace_list:
		sys.stdout.write("\t"+h)
	print
	trace_list[:] = []

def build_lg():
	sys.stderr.write("started parsing lg ...\n")
	trace_list = []
	target_ip = ""
	try:
		while True:
			line=raw_input()
			is_delimiter = False
			if line.split('\t')[2].split(' ')[0] == "from":
				target_ip = line.split(' ')[2]
				is_delimiter = True
			elif line.split('\t')[2][0] == "-":
				continue
			else:
				trace_list.append(line.split(':')[1].strip('\n'))
			
			if is_delimiter and len(trace_list) != 0:
				output_lg_trace(target_ip, trace_list)
			
	except:
		output_lg_trace(target_ip, trace_list)
		sys.stderr.write("finished parsing lg.\n")
		return

def usage():
	sys.stderr.write("./file2trace.py caida/iplane/lg\n")

def main(argv):
	if (len(argv) < 2):
		usage()
		exit()
	source = argv[1]
	if source == "caida":
		build_caida()
	elif source == "lg":
		build_lg()

if __name__ == "__main__":
	main(sys.argv)
