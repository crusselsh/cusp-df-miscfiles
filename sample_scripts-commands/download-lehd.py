'''
    Author: Clayton
    Date: Oct 7, 2015
    
    usage:
    python download-test.py <url-to-data-files>
    
    details:
    program get's a full list of "...".gz files from an input URL contained in any <a href=""> html element, then iterates through the list to download and save the .gz file
'''
import sys
import requests
from bs4 import BeautifulSoup

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
    # download then locally write file
    r = requests.get(url, stream=True)
    with open(fname, 'wb') as fd:
        for chunk in r.iter_content(1000):
            fd.write(chunk)

if __name__=='__main__':
    files_url = sys.argv[1] # input "http://path/to/data/" at command line
    
    # get all file names
    all_files = get_all_files(files_url)
    print 'Files found: ', len(all_files)
    
    for i, file_url in enumerate(all_files[0:3]):
        fileName = file_url.split('/')[-1]
        print 'starting download of', fileName
        download_file(file_url, fileName)
        print 'completed download and save of', fileName
        print 'now {0:.2f}% complete'.format((i+1)*100./len(all_files))
    
    print 'finished. saved %s files' % (i)

