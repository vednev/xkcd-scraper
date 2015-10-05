from bs4 import BeautifulSoup as bs
import urllib as ulib
import os
import io
import sys
import signal

base_url = 'http://xkcd.com/'
folder_name = 'comics'

userhome = os.path.expanduser('~')
desktop = userhome + '/Desktop/'
os.chdir(desktop)
if not os.path.isdir('comics'):
  os.makedirs('comics')
os.chdir('comics')

def run_program():
  global page_number
  bam = True
  while bam:
    a = ulib.urlopen(base_url+str(page_number)).getcode()
    while a != 404:
      r = ulib.urlopen(base_url+str(page_number))
      html = r.read()
      onion = bs(html)
      comic_div = onion.find('div', {'id': 'comic'})
      comic_img = comic_div.find('img')
      comic_url = comic_img['src']
      temp_filename = comic_url.split('/')[-1]
      comic_url = 'http:' + comic_url

      #print comic_url # for debugging
      #print temp_filename # for debugging
      if os.path.isfile(temp_filename):
        print temp_filename + " exists. Continuing..."
        # we're doing this to make sure the next page exists
        temp = ulib.urlopen(base_url+str(page_number+1)).getcode()
        if temp == 404:
          break
        page_number = page_number + 1
        continue
      ulib.urlretrieve(comic_url, temp_filename)
      print "Downloaded image " + str(page_number) + ": " + temp_filename
      page_number = page_number + 1

    with open('../xkcd_scraper.py', 'r') as script:
      data = script.readlines()
    data[70] = '  page_number = ' + str(page_number) + '\n'

    with open('../xkcd_scraper.py', 'w') as script:
      script.writelines(data)
    print "\nAll done!"
    bam = False

def exit(signum, q):
  global page_number
  signal.signal(signal.SIGINT, original_sigint)

  with open('../xkcd_scraper.py', 'r') as script:
    data = script.readlines()
  data[70] = '  page_number = ' + str(page_number) + '\n'

  with open('../xkcd_scraper.py', 'w') as script:
    script.writelines(data)
  sys.exit(1)
  signal.signal(signal.SIGINT, exit)

if __name__ == '__main__':
  original_sigint = signal.getsignal(signal.SIGINT)
  page_number = 1
  signal.signal(signal.SIGINT, exit)
  run_program()
