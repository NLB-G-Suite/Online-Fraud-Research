temp=''
# with open ('datafraud.txt','r') as file2:
# 	for line in file2:
# 		temp+=line
# print temp
with open ('benigncategories.txt','r') as f:
	for line in f:
		if line[0]=='T':
			f_title=line[7:]
			# print f_title

			with open ('benign.txt','r') as file:
				for l in file:
					if f_title==l[3:]:
						try:
							video_properties=''
							next_line=f.next()
							while next_line!='\n':
								video_properties+=next_line
								next_line=f.next()
							f_title=l[0]+': '+f_title+video_properties
							temp+=f_title+'\n'
							# next1=f.next()
							# next2=f.next()

							# if next1[0]!='T' and next2[0]!='T':
							# 	f_title=l[0]+': '+f_title+next1+next2
							# 	print f_title
							# 	temp+=f_title+'\n'
						except:
							print 'error'

with open ('benign_categorisation.txt','w') as f:
	f.write(temp)
	
