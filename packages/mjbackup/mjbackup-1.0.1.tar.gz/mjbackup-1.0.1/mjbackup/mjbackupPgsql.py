#!/usr/bin/env python

import configparser
import glob, os
import subprocess
import time
import grp
import pwd
import sys
from mjbackupConfig import mjbackupConfig

"""MJBackup - Morning Joe Software Linux Server PostgreSQL Backup Module.

Returns:
	string -- The log documenting the status of all the database backups.
"""
class mjbackupPgsql:
	
	def __init__(self):
		
		self.Log=time.strftime("%Y-%m-%d %H:%M:%S") + ": " +"Begin backup of PosgreSQL databases\n"	
		self.verbose=mjbackupConfig.getVerboseOutput()	
		self.readConfig()                

		database_list_command="export PGPASSWORD=%s; echo 'select datname from pg_database' | psql -t -U %s -h %s template1" % (self.password, self.username, self.hostname)
		database_list = subprocess.Popen(database_list_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()	

		#check if the backup directory exists and 
		#create it if it doesn't.
		if not os.path.exists(self.backupdir):
			self.appendLog('Creating '+self.backupdir +'.')
			os.makedirs(self.backupdir)

		#Make a backup of every database on the list that isn't a system database.
		for database_name in database_list:

			database_name=database_name.decode('utf8').strip()
			#Ignore system database names.
			if database_name == '':
				continue
			if database_name == 'template0':
				continue
			if database_name == 'template1':
				continue

			file_name = self.backupdir+"%s%s.sql.pgdump" % (database_name, self.filestamp)
			#Run the backup command.
			backup_command = "export PGPASSWORD=%s; /usr/bin/pg_dump -U %s -h %s -Z 9 -f %s -F c %s" % (self.password, self.username,  self.hostname, file_name, database_name)
			try:			
				subprocess.call(backup_command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			except Exception as e:
				self.appendLog("Error: "+str(e))

			self.appendLog("%s successful backup." % database_name)
			self.cleanBackupdir(self.backupdir, database_name)
		
		#Now that we are done, set the permissions to a normal user.
		self.setUIDGID(self.backupdir)
		self.appendLog("PostgreSQL Backup job complete.")

	"""Reads configuration data from config file for this database.

	Args:
		self (mjbackupFiles): Reference to the instance of this object.
	"""	
	def readConfig(self):
		# Set configfile to the path of the configuration file.
		try:
			self.configfile = '/etc/mjbackup/mjbackupPgsql.conf'
			self.config = configparser.ConfigParser()
			self.config.read(self.configfile)
			self.username = self.config.get('config', 'username')
			self.password = self.config.get('config', 'password')
			self.hostname =  self.config.get('config', 'hostname')
			self.backupdir = self.config.get('config', 'backupdir')
		except:	
			self.configfile = os.path.dirname(os.path.realpath(__file__))+'/conf/mjbackupPgsql.conf'
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
		bkarchives=glob.glob(bktarget+".*sql.pgdump")
		files = sorted(bkarchives)
		while(len(files)>keepCopies):
			self.appendLog("Removing File: "+files[0])
			os.remove(files[0])
			bkarchives=glob.glob(bktarget+".*.sql.pgdump")
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
	
