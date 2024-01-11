#!/usr/bin/env python3

# M Shaafi Jahangir
# V00960196

import sys
import re
import datetime


class process_cal:
	def __init__(self,fname):
		self.fname=fname
		self.listOfEvents = []			#list of event dictionaries
		self.tempDict = {}				#temp dictionary to push into list
		self.rEvent = {}				#rrule events in dictionary to be pushed in list


	def parseAndStore(self, date):			#parses each line in the file and stores
		rruleDict = False					#them accordingly in the temporary dictionary
		added_to_list= False				#which is then pushed into our list of events
	
		with open(self.fname,'r') as f:
			for line in f:
				line = line.strip('\n')
				lineContent = re.search(r"((.*):(.*))", line)

				#when BEGIN:VEVENT is seen, initialize the dictionary
				if lineContent.group(1) == "BEGIN:VEVENT":
					self.tempDict['DTSTART']=''
					self.tempDict['DTSTARTtime'] = ''
					self.tempDict['DTEND']=''
					self.tempDict['DTENDtime'] = ''
					self.tempDict['LOCATION']=''
					self.tempDict['SUMMARY']=''
					self.tempDict['RRULE']=''

				#storing event's start date when seen DTSTART line
				elif lineContent.group(2) == "DTSTART":
					temp = lineContent.group(3)
					self.tempDict['DTSTART'] = datetime.datetime(int(temp[:4]), int(temp[4:6]), int(temp[6:8]))
					self.tempDict['DTSTARTtime'] = datetime.datetime(1,1,1, int(temp[9:11]), int(temp[11:13]), int(temp[13:15]))

				#storing event's end date when seen DTEND line
				elif lineContent.group(2) == "DTEND":
					temp = lineContent.group(3)
					self.tempDict['DTEND'] = datetime.datetime(int(temp[:4]), int(temp[4:6]), int(temp[6:8]), int(temp[9:11]), int(temp[11:13]), int(temp[13:15]))
					self.tempDict['DTENDtime'] = datetime.datetime(1,1,1, int(temp[9:11]), int(temp[11:13]), int(temp[13:15]))

				#storing location when seen LOCATION
				elif lineContent.group(2) == "LOCATION":
					self.tempDict['LOCATION']=lineContent.group(3)

				#storing summary when seen SUMMARY
				elif lineContent.group(2) == "SUMMARY":
					self.tempDict['SUMMARY']=lineContent.group(3)

				#storing rrule line when seen RRULE using another re.search
				elif lineContent.group(2) == "RRULE":
					rruleDict = True
					tempLine = re.search(r".*UNTIL=(.*);.*", line)
					temp = tempLine.group(1)
					self.tempDict['RRULE'] = datetime.datetime(int(temp[:4]), int(temp[4:6]), int(temp[6:8]))
					
				#inserting populated temp dictionary into our list as an event
				elif lineContent.group(1) == "END:VEVENT":
					if(date == self.tempDict['DTSTART']):
						#insertion happening here
						self.listOfEvents.insert(0, self.tempDict)
						added_to_list = True

					#populates rruleDict with rrule events to then push into the main list
					if(self.tempDict['RRULE'] and rruleDict == True):
						incSt = self.tempDict['DTSTART']
						incE = self.tempDict['DTEND']

						while incSt <= self.tempDict['RRULE']:
							incSt = incSt + datetime.timedelta(days=7)
							incE = incE + datetime.timedelta(days=7)
							if incSt <= self.tempDict['RRULE']:
								self.rEvent['DTSTART'] = incSt
								self.rEvent['DTEND'] = incE
								self.rEvent['DTSTARTtime'] = self.tempDict['DTSTARTtime']
								self.rEvent['DTENDtime'] = self.tempDict['DTENDtime']
								self.rEvent['LOCATION'] = self.tempDict['LOCATION']
								self.rEvent['SUMMARY'] = self.tempDict['SUMMARY']

								#appended to list here
								self.listOfEvents.append(self.rEvent)
								added_to_list = True

								#re-initializing dict when appended
								self.rEvent = {}
					self.tempDict = {}

				#exiting code when END:VCALENDER read in line
				elif lineContent.group(1) == "END:VCALENDAR":
					break

		#when all the events are appended to list, we return the list to be used to print
		if added_to_list == True:

			# sortedList = sorted(self.list_of_events, key=lambda d: d['DTSTART'])
			return self.listOfEvents
		else:
			return None
		

	#formatting the int time into proper formatted time used in the printing
	def timeFormatter(self, TF):
		h = TF.strftime("%I")
		if int(h) < 10:
			return TF.strftime(" %-I:%M %p")
		else:
			return TF.strftime("%-I:%M %p") 


	#formatting the int date into proper formatted date used in the printing
	def dateFormatter(self, DS):
		return DS.strftime("%B %d, %Y (%a)")

	#incremented date print (normal print)
	def get_events_for_day(self, date):
		self.parseAndStore(date)
		output =''

		for i in self.listOfEvents:
			if(date == i['DTSTART']):
				formattedDT= str(self.dateFormatter(i['DTSTART'])) + '\n'
				dashLine= str('-'*len(self.dateFormatter(i['DTSTART'])))+"\n"
				formattedEv= str(self.timeFormatter(i['DTSTARTtime']))+" to "+str(self.timeFormatter(i['DTENDtime']))+": "+str(i['SUMMARY'])+" {{"+str(i['LOCATION'])+"}}"
				formattedEv = str(formattedEv)

				#concatted strings to be printed in the command line
				output = formattedDT+dashLine+formattedEv
		return output


#this is code I was working on for printing multiple events on the same day
#please do not take this as I forgot to delete commented output code, but rather an effort to print
#multiple events within one day

	# def get_events_for_day(self, date):
	# 	list = self.parseAndStore(date)
	# 	time = date.strftime("%H:%M:%S")
	# 	Inside = False
	# 	MultExists = False
	# 	output =''
	# 	details = ''
	# 	templist = []
	# 	shortenedList = []
	# 	multipleEvent = []
	# 	# print(date)
	# 	# print(time)

	# 	for i in self.listOfEvents:
	# 		# if('11:15:00' == '0001-01-01 11:15:00' ):
	# 		# 	print('dtsrttime:', i['DTSTARTtime'], '\n')
			
	# 		if date == i['DTSTART'] and time != i['DTSTARTtime']:
	# 			# MultExists = True
	# 			shortenedList.append(i)
	# 		# if date == i['DTSTART'] and time == i['DTSTARTtime']:
	# 		# 	MultExists = False
	# 		# 	templist.append(i)
		
	# 	if(MultExists == True):
	# 		for j in shortenedList:
	# 			Inside = True
	# 			formattedDT= str(self.dateFormatter(j['DTSTART'])) + '\n'
	# 			dashLine= str('-'*len(self.dateFormatter(j['DTSTART'])))+"\n"
	# 			formattedEv= str(self.timeFormatter(j['DTSTARTtime']))+" to "+str(self.timeFormatter(j['DTENDtime']))+": "+str(j['SUMMARY'])+" {{"+str(j['LOCATION'])+"}}"
	# 			formattedEv = str(formattedEv)
	# 			multipleEvent.append(formattedEv)
	# 		details = '\n'.join([str(item) for item in multipleEvent])
	# 		if Inside == True:
	# 			output = formattedDT+dashLine+details
	# 	else:
	# 		for j in templist:
				
	# 			Inside = True
	# 			formattedDT= str(self.dateFormatter(j['DTSTART'])) + '\n'
	# 			dashLine= str('-'*len(self.dateFormatter(j['DTSTART'])))+"\n"
	# 			formattedEv= str(self.timeFormatter(j['DTSTARTtime']))+" to "+str(self.timeFormatter(j['DTENDtime']))+": "+str(j['SUMMARY'])+" {{"+str(j['LOCATION'])+"}}"
	# 			formattedEv = str(formattedEv)
	# 		if Inside == True:
	# 			output = formattedDT+dashLine+formattedEv
	# 	return output
