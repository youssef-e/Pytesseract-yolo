from Classes.Fields import Fields
from datetime import datetime

class Birthday(Fields):

	def extract(self, line):
		result="-1"
		#since the line containing the birthday tend to not be read correctly
		#it first look for the line containing the first name, then try
		#to locate the birthday in the line below it
		line = Fields.clean_alphanum(line, " ")
		words = line.split(" ")
		clean_line=[]
		for value in words:
			if value !="":
				clean_line.append(value)
		#it then can extract the date
		try:
			result = clean_line[len(clean_line)-3]+" "+clean_line[len(clean_line)-2]+" "+clean_line[len(clean_line)-1]
		except IndexError:
			result="-1"
		else:
			for i,c in enumerate(result):
				if((c <'0' or c>'9') and (c!=" ")):
					result=result[:i]+result[i+1:]
			if len(result)!= 10:
				result ="-1"
		#however if the image is too small, they may not be any lines below the firstname, it then sends an error
		return self.set_field(result)

	def word_to_mrz (self):
		date = self.field.replace('/',' ')
		date = date.split(" ")
		return date[2][2:]+date[1]+date[0]

	def synthax_check(self):
		if len(self) != 10 or self.field == "-1":
			print("Warning: Incorrect data")
			return False
		return True

	def mrz_to_word(self):
		word=""
		now = datetime.now() # current date and time
		actual_year = [int(now.strftime("%Y")[:2]),int(now.strftime("%Y")[2:])]
		year = int(self.field[:2])
		if year > actual_year[1]:
			year = (actual_year[0]-1)*100 + year
		else:
			year = actual_year[0]*100 + year
		month = self.field[2:4]
		day = self.field[4:]
		word = day+"/"+month+"/"+str(year)
		return word