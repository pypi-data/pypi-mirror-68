# MJBackup - Morning Joe Software Linux Server Backup System.

This script is called to perform a backup and in turn calls other scripts which perform
specialized task such as back up files, MySql databases, Postgresql databases, and anything
else that this can be extended to support.

There is also a script that can be used to rsync the backup files to the remote location.  The length
these remote copies can be retained can be set by days.

Both scripts are meant to be used with crontab in a single linux server environment with database servers running locally.

## Requirements
* Linux server (Geared more towards standalone web server)
* Python 3.6+ installed
* Mysql installed (optional)
* PostgreSql installed (optional)
* rsync installed (optional)
## Features
* supports backing up files into a tar.gz archive
* supports full database backup dumps of PosgreSql and MySql databases.
* all backups are timestamped in the file name.
* file backups can be grouped into different target archives and locations.  
* databases backup location can be set.
* limits on the backup copies retained on the server.
* logging is supported.
* backup status/errors can be emailed to a list of email addresses.
* rsync based script to help with coping the backups to a remote location.
* support for clearing old backups after a set amount of days on the remote location.

## TODO
* more database support such as Mongo DB, SQL Server
* database backups from multiple configs much like the file archives.
* better logging and error reporting

## Installation (Server)
Run the following command on the server:
```console
user@linux:~$ mkdir mjbackup
user@linux:~$ cd mjbackup
user@linux:~$ pip install mjbackup -t .
user@linux:~$ cd mjbackup
```

There should be the following files for the server part:
* mjbackup.py 
* mjbackupConfig.py 
* mjbackupFiles.py 
* mjbackupPgsql.py 
* mjbackupMysql.py

There should be the following files for the remote location:
* mjsync.py


Copy the files for the server part to a location such as /opt/mjbackup/
```console
user@linux:~$ sudo mkdir /opt/mjbackup
user@linux:~$ sudo cp mjbackup* /opt/mjbackup
user@linux:~$ sudo chown root /opt/mjbackup -R
user@linux:~$ sudo chgrp root /opt/mjbackup -R
user@linux:~$ sudo chmod 700 /opt/mjbackup -R
```
**Make sure this location is only accessible to the superuser.**

Make the configuration directory: 
```console
user@linux:~$ sudo mkdir /etc/mjbackup 
```
## Configuration (Server)

First add this job to crontab. This will perform the backup every Sunday at 3AM.
```console
user@linux:~$ sudo crontab -e

add:
0 3 * * 0 python3 /opt/mjbackup/mjbackup.py
```
Go to the directory where you downloaded the package from pip and go to the "conf" subdirecotry.
There should be many sample configuration files.  These need to be editied for your system.

### mjbackupConfig.xml
```<?xml version="1.0" encoding="UTF-8"?>
<MJBackupConfig>
<BackupList>
	<Path>backup1.xml</Path>
	<Path>backup2.xml</Path>
	<Path>backup3.xml</Path>
</BackupList>
<EmailNotifyList>
	<Email>remote_email1@dont_use_this.com</Email>
	<Email>remote_email2@dont_use_this.com</Email>
	<Email>remote_email3@dont_use_this.com/Email>
</EmailNotifyList>
<EmailSource>example_email@dont_use_this.com</EmailSource>
<LimitCopies>3</LimitCopies>
<Verbose>1</Verbose>
</MJBackupConfig>
```

**BackupList** - List of paths to configuration files for each indivisual archive.

**EmailNotifyList** - List of emails to send a copy of the log every time a backup is done.

**EmailSource** - This is the "From" field when emails are sent out.

**LimitCopies** - Limit to how many backup copies are kept on the server.  Default is 3.

**Verbose** - If set, information will be printed to the console.  For testing.
### backup(X).xml
```<?xml version="1.0" encoding="UTF-8"?>
<BackupList name="examplebackup1" target="example1" targetdir="/targetdir/backups1">
  <Backup>
    <Name>user1</Name>
    <Path>/home/user1</Path>
    <Note>user1 backup</Note>
  </Backup>
  <Backup>
    <Name>user2</Name>
    <Path>/home/user2</Path>
    <Note>user2 backup</Note>
  </Backup>
  </BackupList>
```
Configuration for an individual archive.  Backuplist has three attributes:

**name** - Name of backup group to display in logs/emails.

**target** - Name of the archive.  A date/time stamp and the extension tar.gz will be appended to this in the file name e.g. backup.2020-04-20_050006.tar.gz

**targetdir** - The directory to put this archive into.  Use absolute path such as /home/archive/backups.

Each Backup is a directory or file to add to the archive.

**Name** - Name of backup to display in logs/emails.

**Path** - Absolute path of directory or file to backup.

**Note** - Extra field to put more information about this backup.

### mjbackupMysql.conf
```
[config]
username = mysql-login
password = mysql-password
hostname =  localhost 
backupdir = backups-mysql/
```
**username** - MySql admin login name

**Password** - MySql admin password.

**hostname** - hostname MySql server resides on.

**backupdir** - The directory to put this archive into.  Use absolute path.

### mjbackupPgsql.conf
```
[config]
username = postgres
password = postgres-password
hostname =  localhost 
backupdir = backups-pgsql/

```
**username** - PostgreSql admin login name

**Password** - PostgreSql admin password.

**hostname** - hostname MySql server resides on.

**backupdir** - The directory to put this archive into.  Use absolute path.

### After configuration

Copy all .xml and .conf files to /etc/mjbackup and make sure this directory is only accessible by the superuser.

```console
user@linux:~$ sudo cp *.xml /etc/mjbackup 
user@linux:~$ sudo cp *.conf /etc/mjbackup 
```
Test it to see if it works correctly.  If Verbose is set, you can see the output.

```console
user@linux:~$ sudo python3 /opt/mjbackup/mjbackup.py  
```

## Installation (Remote Sync)

**Before going further, make sure rsync is configured for passwordless login for the remote backup server.**

Copy the files for the server part to a location such as /opt/mjbackup/
```console
user@linux:~$ sudo mkdir /opt/mjbackup
user@linux:~$ sudo cp mjsync.py /opt/mjbackup
user@linux:~$ sudo chown root /opt/mjbackup -R
user@linux:~$ sudo chgrp root /opt/mjbackup -R
user@linux:~$ sudo chmod 700 /opt/mjbackup -R
user@linux:~$ sudo chmod 700 /opt/mjbackup -R
```
**Make sure this location is only accessible to the superuser.**

Make the configuration directory: 
```console
user@linux:~$ sudo mkdir /etc/mjbackup 
```

## Configuration (Remote Sync)

First add this job to crontab. This will perform the backup every Sunday at 5AM. (Give the server a few hours to do the job.)
```console
user@linux:~$ sudo crontab -e

add:
0 5 * * 0 python3 /opt/mjbackup/mjsync.py
```
Go to the directory where you downloaded the package from pip and go to the "conf" subdirecotry.
There should be many sample configuration files.  You only need mjsyn.conf.

### mjsync.conf
```
[config]
username = exampleuser
hostname =  123.123.123.123
remote_backupdir = /server/backupdir
local_backupdir = /local/backupdir
days_to_keep = 30
verbose = True
```

**username** - rsync login name for the server.

**hostname** - rsync host to rsync to.

**remote_backupdir** - The backup directory on the server. Use absolute path.

**local_backupdir** - The local directory to copy to. Use absolute path.

**days_to_keep** - the days to keep old backups downloaded.

**verbose** - Show the status or not.  For testing.

Copy all  mjsync.conf files to /etc/mjbackup and make sure this directory is only accessible by the superuser.

```console
user@linux:~$ sudo cp *.conf /etc/mjbackup 
```
Test it to see if it works correctly.  If Verbose is set, you can see the output.

```console
user@linux:~$ sudo python3 /opt/mjbackup/mjsync.py
```