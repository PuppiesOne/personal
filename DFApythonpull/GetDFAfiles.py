#import subprocess
#import dfa_helper
import dfa_helper_v4 as dfa_helper

import string
import sys
import argparse
import datetime
import os 
import shutil

gsutil = '\\PSCETLP00103.ad.insidemedia.net\MECAnalytics\Client\DFA\gsutil\gsutil.py'  #'C:\gsutil\gsutil.py'
python = '\\PSCETLP00103.ad.insidemedia.net\MECAnalytics\Client\DFA\PortablePython2.7.6.1\App\python.exe' #'C:\Python27\python.exe'

#boto_source_path = r'\\PSCETLP00103.ad.insidemedia.net\MECAnalytics\Client\DFA\DFA Download\boto\.boto'

#boto_dest_path = 'C:%s\.boto' % os.getenv('HOMEPATH')

#def check_boto():
#    shutil.copy(boto_source_path, boto_dest_path)

def parse_params():
    yesterday = datetime.datetime.today() - datetime.timedelta(days = 1)
    yesterday = yesterday.strftime('%m-%d-%Y')

    parser = argparse.ArgumentParser(prog='GetDFAfiles')

    parser.add_argument('--client','-c', help="REQUIRED - Client to pull data for", required = True)
    parser.add_argument('--folder','-f', help="REQUIRED - Folder where downloaded files will be saved", required = True)

    parser.add_argument("--startdate","-s", help="Start date of data pull. If excluded, start date will be yesterday.", default = yesterday)
    parser.add_argument("--enddate","-e", help="End date of data pull. If excluded, end date will be yesterday.", default = yesterday)
    parser.add_argument("--searchpattern","-p", help="Filename search pattern", default = 'Network*%s*')
    parser.add_argument("--bucket","-b", help="The DFA bucket or locker in which the data lives")
    parser.add_argument("--filelist", help="Flag to export a txt file with a list of files matching your search pattern. Will not download the data. ", action='store_true')
    parser.add_argument("--nodata", help="Flag to turn off data pull. ", action='store_true')
    parser.add_argument("--dev","-d", help="Turns on development mode", action='store_true')


    args = parser.parse_args()
    params = args.__dict__
   
    if not os.path.exists(params['folder']):
        os.makedirs(params['folder'])

    return params

if __name__ == "__main__":
   # params = None

    #check_boto()

   # params = {'startdate': '07-01-2014', 'enddate': '07-01-2014', 'bucket': None, 'client': 'michelin', 'searchpattern': 'Network*%s*', 'folder': 'C:\\Users\\daniel.massarsky\\Desktop\\dfa\\michelin', 'nodata': True}

    #if os.path.isfile(boto_dest_path):
    try:
        params = parse_params()
        isDev = params['dev']
        del params['dev']

        if isDev:
            dfa = dfa_helper.Download_DFA_Files(**params)
            locker = dfa_helper.Locker(dfa)
        else:
            dfa = dfa_helper.Download_DFA_Files(**params)
            locker = dfa_helper.Locker(dfa)

            #dfa = dfa_helper.Download_DFA_Files(**params)
            #locker = dfa_helper.Locker(dfa)

        dfa.date_list = dfa.create_date_list()
            
        print
        print 'Client:         ',dfa.client
        print 'Start Date:     ',str(dfa.startdate).partition(' ')[0]
        print 'End Date:       ',str(dfa.enddate).partition(' ')[0]
        print 'Folder:         ',dfa.folder
        print 'Search Pattern: ',dfa.searchpattern
        print

        if not dfa.filelist and dfa.searchpattern.count('%s')==0:
            print 'Search pattern must include "%s" as a placeholder for the date'
        elif not dfa.nodata and locker.exists:
            dfa.run_process()
        else:
            pass
    except:
        pass   
    #else:
    #    print boto_dest_path
 
