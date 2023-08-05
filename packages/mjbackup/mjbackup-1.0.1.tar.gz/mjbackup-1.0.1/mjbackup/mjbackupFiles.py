#!/usr/bin/env python

import glob, os
from os import path
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET 
import gzip
import tarfile
import grp
import pwd
import sys
from mjbackupConfig import mjbackupConfig

"""MJBackup - Morning Joe Software Linux Server File Backup Module.

Returns:
	string -- The log documenting the status of all the backup archives listed in
			  in mjbackupconfig.xml.
"""
class mjbackupFiles:

	def __init__(self):
		self.Log=time.strftime("%Y-%m-%d %H:%M:%S") + ": " +"Begin backup of Files\n"
		bklists=mjbackupConfig.getBackupConfs()
		self.verbose=mjbackupConfig.getVerboseOutput()
		self.filestamp = time.strftime(".%Y-%m-%d_%H%M%S")

		for path in bklists:
			self.executeBackup(path)
		self.Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": " +"End backup of Files\n"
	

	"""Sets the backup directory to the permissions of the parent directory.
		
		This helps since backups are done as root and the backup files
		do not need to have superuser permissions.

	Args:
    	self (mjbackupFiles): Reference to the instance of this object.
		bkdir (str): Name of the directory put the backup archives into.	
	"""
	def setUIDGID(self, bkdir):

		dirpath = os.getcwd()
		stat_info = os.stat(bkdir+'/..')
		self.uid = stat_info.st_uid
		self.gid = stat_info.st_gid
		
		self.user = pwd.getpwuid(self.uid)[0]
		self.group = grp.getgrgid(self.gid)[0]
		os.chown(bkdir, self.uid, self.gid)

		os.chdir(bkdir)
		bkarchives=glob.glob("*")

		for file in bkarchives:
			os.chown(file, self.uid, self.gid)
		os.chdir(dirpath)
	
	"""Read a list of file directories for a single archive
	 
	Args:
    	self (mjbackupFiles): Reference to the instance of this object.
		xmlfile (str): Name of the xml file to read.
	
	Returns:
		list -- list of backup directories for an archive.
	"""
	def getBackupDirs(self, xmlfile):

		# create element tree object
		try:
			tree = ET.parse('/etc/mjbackup/'+xmlfile)
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+'/conf/'+xmlfile)
		
		# get root element
		root = tree.getroot()
	
		# create empty list for backup directories
		bkdirs = []
	
		# iterate news items
		for item in root.findall('./Backup'):
		
			# empty news dictionary 
			bkdir = {}
		
			# iterate child elements of item
			for child in item:
			
				bkdir[child.tag] = child.text
  
	        # append bkdir dictionary to bkdirs items list
			bkdirs.append(bkdir) 
      
		# return bkdirs items list
		return bkdirs 

	"""Get the internal name of a backup archive
	
	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		xmlfile (str): Name of the xml file to read.

	Returns:
		string -- Name of this Backup.
	"""
	def getBackupName(self, xmlfile):
		# create element tree object
		try:
			tree = ET.parse('/etc/mjbackup/'+xmlfile)
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+'/conf/'+xmlfile)
	
		# get root element
		root = tree.getroot()
		return root.attrib['name']

	"""Get the target filename for the backup archive.

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		xmlfile (str): Name of the xml file to read.

	Returns:
		string -- Name of the target file of this backup archive.
	"""
	def getBackupTarget(self, xmlfile):
		# create element tree object
		try:
			tree = ET.parse('/etc/mjbackup/'+xmlfile)
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+'/conf/'+xmlfile)
	
		# get root element
		root = tree.getroot()
		return root.attrib['target']

	"""Get the backup directory for all archives

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		xmlfile (str): Name of the xml file to read.

	Returns:
		string -- The path of the backup directory for all archives.
	"""
	def getBackupDir(self, xmlfile):
		# create element tree object
		try:
			tree = ET.parse('/etc/mjbackup/'+xmlfile)
		except:	
			tree = ET.parse(os.path.dirname(os.path.realpath(__file__))+'/conf/'+xmlfile)
	
		# get root element
		root = tree.getroot()
		return root.attrib['targetdir']

	"""Removes old copies.  How many is set, but defaults to 3.

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		bkdir (str): path to the location where backups are stored for this archive.
		bktarget (str): name of the archive without file extensions and timestamp.
	"""	
	def cleanBackupdir(self, bkdir, bktarget):
		keepCopies=3
		try:
			keepCopies=int(mjbackupConfig.getLimitCopies())
		except Exception as e:
			self.appendLog("Error Reading Backup Limit Config: {0}".format(str(e)))
			keepCopies=3

		dirpath = os.getcwd()
		os.chdir(bkdir)
		bkarchives=glob.glob(bktarget+".*.tar.gz")
		files = sorted(bkarchives)
		while(len(files)>keepCopies):
			self.appendLog("Removing File: "+files[0])
			os.remove(files[0])
			bkarchives=glob.glob(bktarget+".*.tar.gz")
			files = sorted(bkarchives)
		os.chdir(dirpath)
	
	"""Appends the log string.  Records times and errors.	

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		string (str): string to append to the log.
	"""	
	def appendLog(self, string):

		if self.verbose==True:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": " + str(string))
		self.Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": " + str(string)+"\n"

	#
	"""Execute the backup for tar.gz archive.

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		xmlfile (str): Name of the xml file to read.
	"""	
	def executeBackup(self, xmlfile): 
		
		#Get the configuration of this archive
		bkname=self.getBackupName(xmlfile)
		bktarget=self.getBackupTarget(xmlfile)
		bkdir=self.getBackupDir(xmlfile)
		
		self.appendLog("Beginning backup %s." % bkname)

		#check if the backup directory exists and 
		#create it if it doesn't.
		if not os.path.exists(bkdir):
			self.appendLog('Creating '+bkdir+'.')
			os.makedirs(self.getBackupDir(xmlfile))
		
		#tar all directories to be backedup.
		tar = tarfile.open(bktarget+".tar", "w")
		for name in self.getBackupDirs(xmlfile):
			self.appendLog('Adding '+name['Name']+': '+name['Path'])
			try:
				tar.add(str(name['Path']))
			except Exception as e:
				self.appendLog("Error Adding {0}: {1}".format(str(name['Path']), str(e)))
		tar.close()
	
	
		#gzip the created tar file with timestamp.
		with open(bktarget+'.tar', 'rb') as f_in:
			with gzip.open(bkdir+'/'+bktarget+self.filestamp+'.tar.gz', 'wb', 9) as f_out:
				shutil.copyfileobj(f_in, f_out)
		
		#cleanup tar and backup dir
		os.remove(bktarget+'.tar')

		self.appendLog("%s successful backup." % bkname)
		self.cleanBackupdir(bkdir, bktarget)
		self.setUIDGID(bkdir)

	