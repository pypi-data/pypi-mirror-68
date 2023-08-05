#!/usr/bin/env python

import time
import os
import subprocess
import configparser


"""MJBackup - Morning Joe Software Linux Server Backup System Remote Sync.

This script is called to perform an rsync from a remote backup location and clean up 
extra old backup files that collect there.


"""

"""Recursivly retrives filnames from a directory tree and appends to a 
   file list.

	Args:
		dpath (str): directory to get a list of files from.
		flist (str[]): string list to append to. 
"""
def getFilesFromDir(dpath, flist):
        for f0 in os.listdir(dpath):
            f0=os.path.join(dpath, f0)
            
            if os.path.isfile(f0):
                flist.append(f0)
            else:
                getFilesFromDir(f0, flist)

			
if __name__ == "__main__":
    
    # Set configfile to the path of the configuration file.
    try:
        configfile = '/etc/mjbackup/mjsync.conf'
        config = configparser.ConfigParser()
        config.read(configfile)
        username = config.get('config', 'username')
        hostname =  config.get('config', 'hostname')
        remote_backupdir = config.get('config', 'remote_backupdir')
        local_backupdir = config.get('config', 'local_backupdir')
        days_to_keep = config.get('config', 'days_to_keep')
        verbose = config.get('config', 'verbose')
        
    except:
        configfile = os.path.dirname(os.path.realpath(__file__))+'/conf/mjsync.conf'
        config = configparser.ConfigParser()
        config.read(configfile)
        username = config.get('config', 'username')
        hostname =  config.get('config', 'hostname')
        remote_backupdir = config.get('config', 'remote_backupdir')
        local_backupdir = config.get('config', 'local_backupdir')
        days_to_keep = config.get('config', 'days_to_keep')
        verbose = config.get('config', 'verbose')   
    
    sync_command="rsync -avzh %s@%s:%s %s" % (username, hostname, remote_backupdir, local_backupdir)
    if verbose.upper()=='TRUE':
        print('Executing '+sync_command)
    try:
        #subprocess.call(sync_command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('synced')
    except Exception as e:
        print("Error: "+str(e))
        exit()

    now = time.time()
    filelist=[]

    #Get all the files in the local backups we just synced to.
    for f in os.listdir(local_backupdir):
        f=os.path.join(local_backupdir, f)
        
        if os.path.isfile(f):
            filelist.append(f)
        else:
            getFilesFromDir(f, filelist)             
                
    #Go through the file list and delete all the file that are past the
    #expiration date.
    for filepath in filelist:
        if os.stat(filepath).st_mtime < now - int(days_to_keep) * 86400:
            if verbose.upper()=='TRUE':
                print('Removing '+filepath)
            os.remove(filepath)
    