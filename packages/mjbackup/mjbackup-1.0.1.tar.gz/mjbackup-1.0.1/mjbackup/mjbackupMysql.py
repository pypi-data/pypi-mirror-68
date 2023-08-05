#!/usr/bin/env python

import configparser
import glob, os
import subprocess
import time
import grp
import pwd
import sys
from mjbackupConfig import mjbackupConfig

"""MJBackup - Morning Joe Software Linux Server MySql Backup Module.

Returns:
	string -- The log documenting the status of all the database backups.
"""
class mjbackupMysql:

	def __init__(self):
	
		self.Log=time.strftime("%Y-%m-%d %H:%M:%S") + ": " +"Begin backup of MySql databases\n"	
		self.verbose=mjbackupConfig.getVerboseOutput()	
		self.readConfig()	
		
		#check if the backup directory exists and 
		#create it if it doesn't.
		if not os.path.exists(self.backupdir ):
			self.appendLog('Creating '+self.backupdir +'.')
			os.makedirs(self.backupdir)

		# Get a list of databases with :
		database_list_command="export MYSQL_PWD=%s; mysql -u %s -h %s --silent -N -e 'show databases'" % (self.password, self.username, self.hostname)
		database_list = subprocess.Popen(database_list_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()
		
		#Make a backup of every database on the list that isn't a system database.
		for database_name in database_list:

			database_name = database_name.decode('utf8').strip()
			#Ignore system database names.
			if database_name == 'information_schema':
				continue
			if database_name == 'performance_schema':
				continue

			file_name = self.backupdir+"%s%s.sql" % (database_name, self.filestamp)
			backup_command="export MYSQL_PWD=%s; mysqldump -u %s -h %s -e --opt -c %s | gzip -9 > %s.gz" % (self.password, self.username, self.hostname, database_name, file_name)
			
			try:			
				subprocess.call(backup_command,shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			except Exception as e:
				self.appendLog("Error: "+str(e))

			self.appendLog("%s successful backup." % database_name)
			self.cleanBackupdir(self.backupdir, database_name)
		
		#Now that we are done, set the permissions to a normal user.
		self.setUIDGID(self.backupdir)
		self.appendLog("MySql Backup job complete.")

	"""Reads configuration data from config file for this database.

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
	"""	
	def readConfig(self):
		# Set configfile to the path of the configuration file.
		try:
			self.configfile = '/etc/mjbackup/mjbackupMysql.conf'
			self.config = configparser.ConfigParser()
			self.config.read(self.configfile)
			self.username = self.config.get('config', 'username')
			self.password = self.config.get('config', 'password')
			self.hostname =  self.config.get('config', 'hostname')
			self.backupdir = self.config.get('config', 'backupdir')
			self.filestamp = time.strftime(".%Y-%m-%d_%H%M%S")
		except:	
			self.configfile = os.path.dirname(os.path.realpath(__file__))+'/conf/mjbackupMysql.conf'
			self.config = configparser.ConfigParser()
			self.config.read(self.configfile)
			self.username = self.config.get('config', 'username')
			self.password = self.config.get('config', 'password')
			self.hostname =  self.config.get('config', 'hostname')
			self.backupdir = self.config.get('config', 'backupdir')
			self.filestamp = time.strftime(".%Y-%m-%d_%H%M%S")
	
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
		bkarchives=glob.glob(bktarget+".*.sql.gz")
		files = sorted(bkarchives)
		while(len(files)>keepCopies):
			self.appendLog("Removing File: "+files[0])
			os.remove(files[0])
			bkarchives=glob.glob(bktarget+".*.sql.gz")
			files = sorted(bkarchives)
		
		os.chdir(dirpath)

	"""Sets the backup directory to the permissions of the parent directory.
		
		This helps since backups are done as root and the backup files
		do not need to have superuser permissions.

	Args:
    	self (mjbackupFiles): Reference to the instance of this object.
		bkdir (str): Name of the directory put the backup archives into.	
	"""
	def setUIDGID(self, bkdir):

		dirpath = os.getcwd()
		stat_info = os.stat(bkdir+'..')
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

	"""Appends the log string.  Records times and errors.	

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
		string (str): string to append to the log.
	"""	
	def appendLog(self, string):

		if self.verbose==True:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": " + str(string))
		self.Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": " + str(string)+"\n"
	
