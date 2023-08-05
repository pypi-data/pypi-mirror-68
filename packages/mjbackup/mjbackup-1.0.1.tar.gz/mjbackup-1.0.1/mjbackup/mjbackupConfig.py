#!/usr/bin/env python

import configparser
import glob, os
import xml.etree.ElementTree as ET
import time
import grp
import pwd

"""MJBackup - Morning Joe Software Linux Server File Backup Module.

Returns:
	string -- The log documenting the status of all the backup archives listed in
			  in mjbackupconfig.xml.
"""
class mjbackupConfig:

	def __init__(self):
		self=self

	"""Read a list of backup configs for each archive.

	Returns:
	list -- list of backup configs with name, path, and note.
	"""

	@staticmethod
	def getBackupConfs():

		# create element tree object
		try:
			tree = ET.parse("/etc/mjbackup/mjbackupConfig.xml")
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+"/conf/mjbackupConfig.xml")

		# get root element
		root = tree.getroot()

		# create empty list for backup directories
		bkconfs = []

		# iterate news items
		for item in root.findall('./BackupList'):

			# empty backup dictionary
			bkconf = ''

			# iterate child elements of item
			for child in item:

				bkconf = child.text

				# append bkconf dictionary to bkconfs items list
				bkconfs.append(bkconf)

		# return bkdirs items list
		return bkconfs

	"""Read a list of email addresses to notifiy the status of the backup.

	Returns:
	list -- list of email addresses to notifiy the status of the backup.
	"""

	@staticmethod
	def getEmailNotifyList():

		# create element tree object
		try:
			tree = ET.parse("/etc/mjbackup/mjbackupConfig.xml")
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+"/conf/mjbackupConfig.xml")

		# get root element
		root = tree.getroot()

		# create empty list for backup directories
		enotifys = []

		# iterate news items
		for item in root.findall('./EmailNotifyList'):

			# empty backup dictionary
			enotify = ''

			# iterate child elements of item
			for child in item:
				enotify = child.text
				# append bkconf dictionary to bkconfs items list
				enotifys.append(enotify)

		# return bkdirs items list
		return enotifys

	
	"""Read the source email to send emails from mjbackupConfig.xml

	Returns:
	string -- source email to send emails from.
	"""
	@staticmethod
	def getEmailSource():

		# create element tree object
		try:
			tree = ET.parse("/etc/mjbackup/mjbackupConfig.xml")
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+"/conf/mjbackupConfig.xml")

		# get root element
		root = tree.getroot()

		if len(root.findall('./EmailSource'))==0:
			return 'default@default.com'
		# iterate news items
		return root.findall('./EmailSource')[0].text
	
	"""Read the number of copies of backups to keep

	Returns:
	string -- number of copies of backups to keep as a string.
	"""
	@staticmethod
	def getLimitCopies():

		# create element tree object
		try:
			tree = ET.parse("/etc/mjbackup/mjbackupConfig.xml")
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+"/conf/mjbackupConfig.xml")

		# get root element
		root = tree.getroot()

		if len(root.findall('./LimitCopies'))==0:
			return '3'
		# iterate news items
		return root.findall('./LimitCopies')[0].text	

	"""Read the verbose flag to determine to print log to console.

	Returns:
	boolean -- True if the logs will print to console, False if not. 
	"""
	@staticmethod
	def getVerboseOutput():
		
		# create element tree object
		try:
			tree = ET.parse("/etc/mjbackup/mjbackupConfig.xml")
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+"/conf/mjbackupConfig.xml")

		# get root element
		root = tree.getroot()

		if len(root.findall('./Verbose'))==0:
			return False
		verbose=root.findall('./Verbose')[0].text;
		
		if verbose=='1' or verbose.lower()=='true':
			return True
		return False	
