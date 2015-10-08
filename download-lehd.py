'''
    Author: Clayton
    Date: Oct 7, 2015
    
    usage:
    python download-test.py <url-to-data-files> <sftp creds>
    
    details:
    program get's a full list of "...".gz files from an input URL contained in any <a href=""> html element, then iterates through the list to:
        a) download the .gz file,
        b) upload file to sftp site (given in <sftp creds> argument), and
        c) removes file from local directory
        
    Note: for sftp credentals (<sftp creds>), can either a) link to a saved JSON file with line 45 or b) paste/type in JSON string directly to command line using line 46
'''
import os
import sys
import requests
from bs4 import BeautifulSoup
import pysftp
import json
# http://lehd.ces.census.gov/data/lodes/LODES7/ny/rac/

def get_all_files(url):
    soup = BeautifulSoup(requests.get(url).text)
    url_list = []
    for a in soup.find_all('a'):
        href = a['href']
        if href.split('.')[-1]=='gz':
            url_list.append(files_url + href)
    return url_list

def download_file(url, fname):
    print 'starting data download...'
    ### a) save, 
    fname = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(fname, 'wb') as fd:
        for chunk in r.iter_content(1000):
            fd.write(chunk)
    print 'file written to local'
    # b) call sftp transfer function and c) delete local file

def upload_to_sftp(localFile):
    # creds = json.load(sys.argv[2])
    creds = json.loads(sys.argv[2])
    # Create SFTP connection
    sftp = pysftp.Connection(host=creds['host'], username=creds['username'], password=creds['password'])
    with sftp.cd('upload'):
	    print 'pre-existing files on sftp: ', sftp.listdir()
	    sftp.put(localFile)
	    print 'now existing files: ', sftp.listdir()
    print 'upload file: ', localFile
    
def remove_local_file(localFile):
    try:
        os.remove(localFile)
    except OSError:
        raise # raise if error
    print 'done removing file: ', localFile

if __name__=='__main__':
    files_url = sys.argv[1] # input "http://path/to/data/" at command line
    # get all file names
    all_files = get_all_files(files_url)
    print 'Files found: ', len(all_files)
    
    #for file_url in all_files:
    #    print file_url
    # parse first file name for function dev
    fileName = all_files[1].split('/')[-1]
    # separate out steps into own functions
    download_file(all_files[1], fileName)
    upload_to_sftp(fileName)
    remove_local_file(fileName)
    
    print 'finished.'
    
