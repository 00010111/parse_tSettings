#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: twitter: @b00010111

import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
import os

version_string = "0.1000" 

#
# Function to parse a settings.xml file 
# Parameter file File object to be read & parsed
#
def parseSettings(file):
	print("STARTING processing of file: \"" +file.name + "\"")
	tree = ET.parse(file)
	root = tree.getroot()
	if root.tag == "{http://www.siemens.com/Automation/2009/SettingsData}Settings":
		print("\tKnown root settings entry. Erything is fine, will continue parsing. Just want to let you know smooth processing expected.")
	else:
		print("\tUnknown root settings entry.\nResults may not be correct.\nPlease file an issue on github and submit sample data for tool improvement.\nAnonymized Sample Data is fine.")

	# get node lastprojects
	for general in root.findall('{http://www.siemens.com/Automation/2009/SettingsData}SettingNode/{http://www.siemens.com/Automation/2009/SettingsData}Setting[@name="LastProjects"]'):
		#print(general.tag)
		#print(general.attrib)

	#START Section to print the last opend projects	
		print("\t" + general.get('name'))
		for child in general:
			for c in child:
				#THIS gets the values of the strings
				print("\t\t" + c.text)

	#END Section to print the last opend projects

	# Section to print LastOpenedProject LRUProjectStorageLocation LRUProjectArchiveStorageLocation
	for application in root.findall('{http://www.siemens.com/Automation/2009/SettingsData}SettingNode/{http://www.siemens.com/Automation/2009/SettingsData}SettingNode[@name="Application"]'):	
		#itterate all childs of appication to find the settings note with the name LastOpendProject
		for child in application:
				if child.attrib.get('name') == "LastOpenedProject":
					print("\n\t" + child.attrib.get('name'))
					for c in child:
							print("\t\t" + c.text)
				elif child.attrib.get('name') == "LRUProjectStorageLocation":
					print("\n\t" + child.attrib.get('name'))
					for c in child:
							print("\t\t" + c.text)
				elif child.attrib.get('name') == "LRUProjectArchiveStorageLocation":
					print("\n\t" + child.attrib.get('name'))
					for c in child:
							print("\t\t" + c.text)
				else:
					continue

	# End Section to print LastOpenedProject LRUProjectStorageLocation LRUProjectArchiveStorageLocation

	# section printing <SettingNode name="ConnectionService"> information.
	# we need to check if a project hast controller configuration set, if so communication to a PLC has been done
	print('\n\tConnectionService')
	for cs in root.findall('{http://www.siemens.com/Automation/2009/SettingsData}SettingNode[@name="ConnectionService"]'):
		for child in cs:
			#entering level of connections Services, more than one observed when host was remamed?
			creationTime = ''
			print("\t\t" + child.attrib.get('name'))
			for c in child:
				#print(c.attrib.get('name'))
				for b in c:
					controllerConfig_dict = {}
					# on this level we get the creation time of the project file in UTC & the Node <SettingNode> with the name ControllerConfigurations
					if b.attrib.get('name','') == 'CreationTime':
						creationTime = b[0].text
						#break
					if b.attrib.get('name','') == 'ControllerConfigurations':
						# below this is another setting node, the childs of this settingnode are Setting entries, interesting can be name == BoardName,OamName,OamAddress
						# only IF a ControllerConfiguration is present, communication to the PLC has been done (go online, download project files),
						#OAMAddress shows the IP Address of the PLC that communication has been observed with
						#reset controllerConfig_dict
						controllerConfig_dict = {}
						for cb in b:
							#at this level we need to run through the childs to get OamName etc
							controllerConfig_dict = {cb.attrib.get('name'):{}}
							#DEV_DEBUG: At this level we need an dict with key cb.attrib.name, and a value with a dict, in which we will add ccb_name + ccb[0].text,
							# at the print section below we print the results.
							BoardName = OamName = OamAddress = ''
							for ccb in cb:
								#BoardName = OamName = OamAddress = ''
								ccb_name = ccb.attrib.get('name','')
								if ccb_name == 'BoardName':
								#	print(ccb[0].text)
									BoardName = ccb[0].text
								elif ccb_name == 'OamName':
								#	print(ccb[0].text)
									OamName = ccb[0].text
								elif ccb_name == 'OamAddress':
								#	print(ccb[0].text)
									OamAddress = ccb[0].text
								#print("BoardName " + BoardName)
								#print("OamName " + OamName)
								controllerConfig_dict.update({cb.attrib.get('name'):{"BoardName":BoardName,"OamName":OamName,"OamAddress":OamAddress}})
								
				# only SettingNode entries with a child of type setting and name of creation time are project entires
				if len(creationTime) > 0:
					print("\t\tFound project:\n\t\t\tProject Path")
					print("\t\t\t\t" + c.attrib.get('name'))
					print("\t\t\tCreation Time of Project in UTC:")
					print("\t\t\t\t" + creationTime)
					#print(controllerConfig_dict)
					for k, v in controllerConfig_dict.items():
						print("\t\t\tControllerConfigurations found for project:")
						print("\t\t\t\t" + k)
						print("\t\t\t\tBoardName: " + v.get('BoardName'))
						print("\t\t\t\tOamName: " + v.get('OamName'))
						print("\t\t\t\tOamAddress: " + v.get('OamAddress'))
					creationTime = ''
					#break

			creationTime = ''
	# End section printing <SettingNode name="ConnectionService"> information.

	# section printing <SettingNode name="LoadService"> information
	print('\n\tLoadService')
	for cs in root.findall('{http://www.siemens.com/Automation/2009/SettingsData}SettingNode[@name="LoadService"]'):
		for child in cs:
			#entering level of load services
			print("\t\t" + child.attrib.get('name'))
			for c in child:
				print("\t\t\t" + c.attrib.get('name'))
				#on this level project name is printed, this means the project was uploaded at least once
	# End section printing <SettingNode name="LoadService"> information
	print("\nEND processing of file: \"" + file.name + "\"\n\n")

def printExplanation():
	lastps_string = """LastProjects:\n\tLast project opened in the TIA Portal. This list is in chronological order. 
	Observations: 
		If you delete a project from the recent project lists via tha TIA Portal it will be removed from this list. Although the rest of the entries stay in chronological order.
		Not affected if the TIA Portal is opened and closed without opening a project."""
	lastp_string = """LastProject:\n\tLast project opened in the TIA Portal.
	Observations: 
		If you open the TIA Portal and close it without openind a project, the value is cleared and will be empty in the Settings.xml file.
		The value is not affected if a project is removed from the recently used projects in the TIA Portal."""
	LRUps_string = """LRUProjectStorageLocation:\n\tLocation of the project folder of the last opened project.
	Observations: 
		Not affected if the TIA Portal is opened and closed without opening a project.
		The value is not affected if a project is removed from the recently used projects in the TIA Portal."""
	LRUA_string = """LRUProjectArchiveStorageLocation:\n\tMost recent location a project file was archived to via the archive function of the TIA Portal.
	Observations:
		The value is overwritten if a different location is chosen while archiving a project.
		Unless the archive function is used, the node is not present in the “Settings.xml” file."""
	cs_string = """ConnectionServices:\n\tList of projects that where worked on within the TIA Portal. Can reveal creation time of the project in UTC and connection information for configured PLCs.
	Observations:
		Not affected if the TIA Portal is opened and closed without opening a project.
		The value is not affected if a project is removed from the recently used projects in the TIA Portal.
		An entry for a project is not added directly after an empty project is created, neither is it added when an empty project is re-open again.
		A entry, including the project creation timestamp in UTC, is added when you start to configure the project, for example by adding a PLC to it.
		The creation timestamp is taken from within the project. It is NOT the time of creating the entry in the Settings.xml file.
		If communication with a configured PLC has been performed, the connection information (ControllerConfiguration) is added. Beforehand the corresponding xml structure in not present for the given project.
		If a PLC is removed from a project, the corresponding xml structure is not removed.
		Names of the xml child notes containing the connection information do SEEM to be not randomly renerated, the same PLC used in different projects seems to get the same name."""
	ls_string = """LoadServices:\n\tList of projects that where worked on within the TIA Portal.
	Observations:
		Not affected if the TIA Portal is opened and closed without opening a project.
		The value is not affected if a project is removed from the recently used projects in the TIA Portal.
		A project is listed here if a PLC is added to it and configuration is done to communicate with the PLC, like setting an IP-Address to its interface.
		Names of the xml child notes per PLC do SEEM to be not randomly renerated, the same PLC used in different projects seems to get the same name.
		Names per PLC does NOT match the names assigend in the ConnectionServices section.
		If a PLC is removed from a project, the corresponding xml structure is not removed.
		If a complete project, with PLCs configured, is copied to a different location on the same machine, opened and an interaction to the PLC is initiated with the “go online” function, 
			no additional entry in the “LoadService” section for the copied project is created. 
			If the IP-Address configuration for the PLC is changed in the project, an entry will be created though.
			Theory could be that the configuration of the IP-Address creates the entry and the first interaction with the PLC just updates the entry if it exists. 
			If it does not find a matching entry nothing is done."""
	generic_string = """Settings.xml 
	File path: C:\\Users\\$USERNAME\\AppData\\Roaming\\Siemens\\Portal $VERSION\\Settings\\Settings.xml
	Observations:
		Example path: C:\\Users\\testUser\\AppData\\Roaming\\Siemens\\Portal V15_1\\Settings\\Settings.xml
		The file belongs to the user, so no additional permissions are needed to change or delete the file.
		If the settings.xml file is deleted and the Siemens TIA Portal is started afterwards, it will silently create a fresh new settings file."""
	explanation_header = """
	############################################################################################################################
	####################### Below find explanation and notes on observations of the specific data fields #######################
	############################################################################################################################"""
	print(explanation_header)
	print(generic_string)
	print(lastp_string)
	print(lastps_string)
	print(LRUps_string)
	print(LRUA_string)
	print(cs_string)
	print(ls_string)
	
parser = argparse.ArgumentParser(description='Process Siemens TIA portal setings files and extract data about open projects and indicators if a interaction with a PLC has been performed.')
group = parser.add_mutually_exclusive_group()
parser.add_argument("-v", "--verbose", help="Increase output verbosity and include explanations about the different data fields and observations on their behaviour",action="store_true")
parser.add_argument("-b", "--bulk", help="When -d (--directory) is specified and more than one Settings.xml files should be parsed specify this argument",action="store_true")
group.add_argument("-f","--file", type=argparse.FileType('r'), help="Path (relative or absolute) to the file to parse. Example: C:\Data\Settings.xml")
group.add_argument("-d","--directory", type=lambda p: Path(p).absolute(), help="Path (relative or absolute) to directory that should be search recursivley for a file named settings.xml. First found file will be processed.")

args = parser.parse_args()

if args.verbose:
	print("parse_tSettings Version: " + version_string)

#directory and file are mutally exlusive, both are note accepted by argparser
# if we get a directory, we can search for a path to settings.xml and set this as args.file (needs to be file object then
if args.directory:
	#directory given
	if not args.directory.is_dir():
	#if not os.path.isdir(args.directory):
		print("Given path \"" + str(args.directory) + "\" is not a valid directory. Exiting.")
		exit(1)
	#searching the given directory for Settings.xml
	result = []
	for root, dirs, files in os.walk(args.directory):
		if "Settings.xml" in files:
			result.append(os.path.join(root, "Settings.xml"))
	if len(result) == 1:
		args.file = open(result[0],'r')
		parseSettings(args.file)
	elif len(result) > 1 and not args.bulk:
		print("More then one Settings.xml file found. Please specifiy -b (--bulk) if you want to process more than one Settings.xml files. Exiting.")
		exit(1)
	elif len(result) > 1 and args.bulk:
		for f in result:
			parseSettings(open(f,'r'))
	elif len(result) == 0:
		print("No Settings.xml files found within given path\" " + str(args.directory) + "\" Exiting.")
		exit(0)
	#print(len(result))
			
elif args.file:
	parseSettings(args.file)		

if args.verbose:
	printExplanation()
