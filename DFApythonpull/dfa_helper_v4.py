import datetime
from dateutil import parser
import string
#import subprocess
import os
import shutil
import sqlite3
import argparse
import httplib2
import sys
import fnmatch
import requests
import time
import random

import json
#import pymongo

from apiclient.http import MediaIoBaseDownload
from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.file import Storage as CredentialStorage
from oauth2client import client
from oauth2client import tools

# Retry transport and file IO errors.
RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)

# Number of times to retry failed downloads.
NUM_RETRIES = 7

# Number of bytes to send/receive in each request.
CHUNKSIZE = 2 * 1024 * 1024

# Mimetype to use if one can't be guessed from the file extension.
DEFAULT_MIMETYPE = 'application/octet-stream'

def handle_progressless_iter(error, progressless_iters):
  if progressless_iters > NUM_RETRIES:
    print 'Failed to make progress for too many consecutive iterations.'
    raise error

  sleeptime = random.random() * (2**progressless_iters)
  print ('Caught exception (%s). Sleeping for %s seconds before retry #%d.'
         % (str(error), sleeptime, progressless_iters))
  time.sleep(sleeptime)

def print_with_carriage_return(s):
  sys.stdout.write('\r' + s)
  sys.stdout.flush()

class Locker(object):

    def __init__(self, cls):
        self.client = cls.client
        self.bucket = cls.bucket
        self.conn = sqlite3.connect(r'\\PSCETLP00103.ad.insidemedia.net\MECAnalytics\Client\DFA\DFA Locker\dfa_locker.db')
        self.c = self.conn.cursor()
        self.cls = cls

        self.get_client()

    def get_client(self):

        self.results = self.c.execute("SELECT * FROM lockers WHERE client='%s'" % self.client)
        self.results_list = self.results.fetchall()
        self.results_count = len(self.results_list)
        self.exists = True

        if self.results_count == 0 and self.bucket != None:

            self.c.execute("INSERT INTO lockers VALUES ('%s','%s',NULL)" % (self.client, self.bucket))
            self.conn.commit()
            self.cls.bucket = self.bucket
            print
            print '###  DFA details for %s have been saved!' % self.client
            print

        elif self.results_count > 0:
            self.cls.bucket = self.results_list[0][1]

            if self.bucket != None:
                if self.cls.bucket != self.bucket:
                    self.c.execute("UPDATE 'lockers' SET bucket='%s' WHERE client='%s'" % (self.bucket,self.client))
                    self.conn.commit()
                    self.cls.bucket = self.bucket
                    print
                    print '###  DFA bucket for %s has been updated!' % self.client
                    print
        else:
            self.exists = False
            print
            print "###  Client doesn't exist, the call must be made with the bucket location added:"
            print "###  i.e      --bucket dfa_-9dc9dee08c29be3"
            print

class Download_DFA_Files(object):
        
    def __init__(self, **kwargs):

        if os.path.isfile('C:\Python27\python.exe'):
            self.python = 'C:\Python27\python.exe'
        else:
            self.python = r'\\PSCETLP00103.ad.insidemedia.net\MECAnalytics\Client\DFA\PortablePython2.7.6.1\App\python.exe'

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        print "dfa_helper_v4"

    def create_date_list(self):

        date_format = '%m-%d-%Y'

        add_1_day = datetime.timedelta(days = 1)

        self.startdate = parser.parse(self.startdate)

        if self.enddate == None:
            self.enddate = datetime.datetime.today() - add_1_day
        else:
            self.enddate = parser.parse(self.enddate)

        if self.startdate <= self.enddate:
            date_span = self.enddate - self.startdate

            date_list = []
            date_list_str = []

            for x in range(date_span.days+1):
                date = self.startdate +  datetime.timedelta(days=x)
                date_list.append(date)
                date_list_str.append(date.strftime(date_format))

            return date_list_str
        else:
            print '###  Start date has to be before the end date!'

    def download(self, service, object_name):

        export_filepath = '%s\%s' % (self.folder, object_name)
        export_file = file(export_filepath, 'wb')

        request = service.objects().get_media(bucket=self.bucket,
                                              object=object_name)

        media = MediaIoBaseDownload(export_file, request, chunksize=CHUNKSIZE)

        progressless_iters = 0

        done = False
        
        while not done:
            error = None
            try:
                progress, done = media.next_chunk()
                if progress:
                    download_message =  '   Downloading %d%% - %s                                    ' % (int(progress.progress() * 100), object_name)
                    sys.stdout.write('\r' + download_message)
                    sys.stdout.flush()
            except HttpError, err:
                error = err
                if err.resp.status < 500:
                    raise
            except RETRYABLE_ERRORS, err:
                error = err
                print 'error'

            if error:
                progressless_iters += 1
                handle_progressless_iter(error, progressless_iters)
            else:
                progressless_iters = 0
        
        #if os.path.getsize(export_filepath) == 0:
        #    try:
        #        os.remove(export_filepath)
        #    except:
        #        pass

        print

    def run_process(self):

        _API_VERSION = 'v1'

        # Parser for command-line arguments.
        argparser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        
        KEY_FILE = os.path.join(os.path.dirname(__file__), 'dfa_pk.pem')
          
        client_email = '157982836811-de3d75tocagiefhvcdp3pqnuufnerjcv@developer.gserviceaccount.com'

        with open(KEY_FILE) as f:
            private_key = f.read()

        credentials = SignedJwtAssertionCredentials(client_email, private_key,
                ['https://www.googleapis.com/auth/devstorage.full_control',
                 'https://www.googleapis.com/auth/devstorage.read_only',
                 'https://www.googleapis.com/auth/devstorage.read_write',])

        
        if credentials is None or credentials.invalid:

            storage = CredentialStorage(os.path.join(os.path.dirname(__file__), 'credentials.dat'))
            credentials = storage.get()

            if credentials is None or credentials.invalid:

                CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

                FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
                       scope=['https://www.googleapis.com/auth/devstorage.full_control',
                              'https://www.googleapis.com/auth/devstorage.read_only',
                              'https://www.googleapis.com/auth/devstorage.read_write',],
                       message=tools.message_if_missing(CLIENT_SECRETS))

                flags = argparser.parse_args([])#'--noauth_local_webserver'])
                credentials = tools.run_flow(FLOW, storage, flags)

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = discovery.build('storage', _API_VERSION, http=http)
        items = []
               
        try:

            req = service.objects().list(bucket= self.bucket, prefix=self.searchpattern.split('*')[0], fields='items/name,nextPageToken' )
            reqCount = 0

            while req is not None:

                resp = req.execute()

                if reqCount == 0 and resp=={}:
                    print 'No matching files for search pattern: %s' % self.searchpattern
                    sys.exit

                for item in resp['items']:
                    items.append(item['name'])

                reqCount += 1
                req = service.objects().list_next(req, resp)

        except client.AccessTokenRefreshError:
            print ("The credentials have been revoked or expired, please re-run"
                    "the application to re-authorize")

        if self.filelist:

            fileList_Path = r'%s\fileList.txt' % self.folder

            fileListFile = file(fileList_Path, 'w')
            fileListFile.write('FileName\n')
        
        else:
            downloadLog_Path = r'%s\downloadLog.txt' % self.folder
            log = file(downloadLog_Path, 'w')

        for date in self.date_list:

            file_search_string = self.searchpattern.replace('DONE','done').replace('%s',date)
            done_file_search_string = '*' + date + '*done' # file_search_string.split('.')[0]
            
            files_matched = fnmatch.filter(items, file_search_string)
            done_files_matched = fnmatch.filter(items, done_file_search_string )#+ '.done')
            
            if self.filelist:
            
                for _file in files_matched:
                    fileListFile.write(_file+'\n')

            else:                                 
                print
                print 'Looking for .done file for %s' % date      
                       
                if len(done_files_matched) != 0:

                    print 'Found! Downloading %s files for %s' % (self.client, date)
                    print

                    files_matched.reverse()
                
                    for object_name in files_matched:
                        try:
                            self.download(service, object_name)
                            logMessage = 'SUCCESS    %s\n' % object_name
                            log.write(logMessage)
                        except:
                            logMessage = '!!FAILED   %s\n' % object_name

## UPDATE BY BRANDON 'SEXY LEGS' NIEVES ON 04-09-2015 

                elif len(files_matched) != 0:
                    print
                    print 'Looking for zip file for %s' % date
                                                                                                                                                                                
                    print 'Found! Downloading %s files for %s' % (self.client, date)
                    print
                                                                                
                    files_matched.reverse()
                                                                                
                    for object_name in files_matched:
                        try:
                            self.download(service, object_name)
                            logMessage = 'SUCCESS    %s\n' % object_name
                            log.write(logMessage)
                        except:
                            logMessage = '!!FAILED   %s\n' % object_name

## END OF 'SEXY LEGS' UPDATE

                else:
                    print '.done file not found for %s' % date
        try:
            fileListFile.close()
            print 'File list has been exported to %s' % fileList_Path
        except:
            log.close()

