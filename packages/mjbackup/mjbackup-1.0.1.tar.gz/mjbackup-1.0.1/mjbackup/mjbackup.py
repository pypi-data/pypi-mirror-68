#!/usr/bin/env python

import time
import os
import smtplib
from email.message import EmailMessage
from mjbackupConfig import mjbackupConfig
from mjbackupFiles import mjbackupFiles
from mjbackupPgsql import mjbackupPgsql
from mjbackupMysql import mjbackupMysql

"""MJBackup - Morning Joe Software Linux Server Backup System.

This script is called to perform a backup and in turn calls other scripts which perform
specialized task such as back up files, MySql databases, Postgresql databases, and anything
else that this can be extended to support.

The files are archived with a time/date timestamp and multiple copies of a backup are supported.
Appending the status to the logfile /var/log/mjbackup/mjbackup.log is supported.
Automatically emailing the status of the backup/log is supported.

"""
if __name__ == "__main__":

	#print(os.path.dirname(os.path.realpath(__file__))+"/mjbackup.xml")
	#exit()
	Log="\n"+time.strftime("%Y-%m-%d %H:%M:%S") + ": Beginning backup processes\n\n"
	Status="Successful"
	verbose=mjbackupConfig.getVerboseOutput()

	#Backup the Postgresql databases.
	try:
		Pgsql=mjbackupPgsql()
		Log+=Pgsql.Log
	except Exception as e:
		if verbose:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (PostgreSQL): "+str(e))
		Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (PostgreSQL): "+str(e)+"\n"
		Status="Error"
	Log+="\n"

	#Backup the MySql databases.
	try:
		Mysql=mjbackupMysql()
		Log+=Mysql.Log
	except Exception as e:
		if verbose:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (MySQL): "+str(e))
		Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (MySQL): "+str(e)+"\n"
		Status="Error"
	Log+="\n"

	#Backup the files.
	try:
		File=mjbackupFiles()
		Log+=File.Log
	except Exception as e:
		if verbose:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (Files): "+str(e))
		Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (Files): "+str(e)+"\n"
		Status="Error"
	Log+="\n"+time.strftime("%Y-%m-%d %H:%M:%S") + ": Ending backup processes\n"

	try:
		#Check if the mjbackup log directory exists and create it if it doesn't.
		if not os.path.exists("/var/log/mjbackup/"):
			Log+='Creating /var/log/mjbackup/.'
			os.makedirs("/var/log/mjbackup/")

		#Append the log to the end of the log file.
		logfile=open("/var/log/mjbackup/mjbackup.log","a+")
		logfile.write(Log)
		logfile.close()
	except Exception as e:
		if verbose:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (Logs): "+str(e))
		Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (Logs): "+str(e)+"\n"
		Status="Error"

	try:	
		server = smtplib.SMTP('localhost')
		server.set_debuglevel(1)
		emailList=mjbackupConfig.getEmailNotifyList()
	
		#Mail the current log to whoever it is set to in the email list.
		for email in emailList:
			LogMsg = EmailMessage()
			LogMsg.set_content(Log)
			LogMsg['Subject'] = 'Backup Log '+time.strftime("%Y-%m-%d %H:%M:%S") + ' ' +Status
			LogMsg['From'] = mjbackupConfig.getEmailSource()
			LogMsg['To'] = email
			server.send_message(LogMsg)
		server.quit()
	except Exception as e:
		if verbose:
			print(time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (Email): "+str(e))
		Log+=time.strftime("%Y-%m-%d %H:%M:%S") + ": Error (Email): "+str(e)+"\n"
		Status="Error"
