

hyp = open('iitdelhi_Lec32/hyp_text.txt').readlines()
outfile = open('iitdelhi_Lec32/Lec32.gl', 'w')
for line in hyp:
	txt = ' '.join(line.split()[1:])
	outfile.write(txt)
	outfile.write(' ')


