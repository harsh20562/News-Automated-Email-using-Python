import smtplib
import email.mime
import datetime
import bs4
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from requests import get
import re

now = datetime.datetime.now()
content = ''

def extract_news(url):
  print('Extracting News Stories...')
  matter = ''
  matter = matter + ('Top News of the day\n' + '<br>' + '-'*60 + '<br>')
  response = requests.get(url)
  cont = response.content
  soup = BeautifulSoup(cont,'html.parser')  
  idx = 1
  for i,tag in enumerate(soup.find_all('span',attrs={'class':'w_tle'})):
    for j,tags in enumerate(soup.find_all('a')):
      if tags.get('title')==tag.text:
        matter += (('<br>' + str(idx) + ' :: ' + tag.text + "\n" + '<br>'))
        matter += '\n You can find more at : '
        link = tags.get('href')
        if link.count('https://timesofindia.indiatimes.com')==0:
          link = 'https://timesofindia.indiatimes.com'+link
        matter += link
        matter += '\n'
        idx = idx + 1
        break
      else:
        continue
  return(matter)

matter = extract_news('https://timesofindia.indiatimes.com/india')
content = content + matter
content += ('<br>------------------------------<br>')
#print(content)

SERVER = 'smtp.gmail.com' # "your smtp server"
PORT = 587 # your port number
FROM =  '' # "your from email id"
TO = '' # "your to email ids"  # can be a list
PASS = '' # "your email id's password"

msg = MIMEMultipart()
msg['Subject'] = 'News Stories of the Day ' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
