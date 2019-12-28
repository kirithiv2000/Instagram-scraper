from os import path
from selenium import webdriver
from bs4 import BeautifulSoup
from getpass import getpass #To hide password while entering
import json,time,pprint,os
##########################
username = input('Enter your username: ')
password = getpass('Enter your password: ') # we are hiding password using getpass while entering
###############################################
def insta():
	global dic
	dic={}
	driver = webdriver.ChromeOptions() # initializing driver
	prefs = {"profile.default_content_setting_values.notifications" : 2} # to hide browser notifications
	driver.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(chrome_options=driver)
	driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')#TO SEARCH THIS URL
	time.sleep(3) 
	try: # To try with our entered password and user name
		driver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(2) > div > label > input').send_keys(username) #sending instagram id username
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(password) #sending instagram id passwoed
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click() #clicking on the login button
		time.sleep(5)# waiting for 5 seconds so that we can load the home page for the data that we want
		driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a').click()
	except: # If the password or the username we entered is wrong we except the errors 
		print('Username or password may be wrong or we are facing some issue of network issue')
		driver.quit() # to exit the chromium browser
		return '' # we return some value so we can stop the code from run further
	###################################################

	time.sleep(5)
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click() #clicking on the followers button
	global name
	name=driver.title.split()[0].strip()
	print('your name is '+name)
	time.sleep(5)
	###################################################
	# from here onwords. I'm starting to scroll 
	value=0.1
	# Get scroll height
	last_height=driver.execute_script('return document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollHeight')  
	while 1: # starting scrolling slowly so the suggesions will disappear from the page
		driver.execute_script('document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollTo(0,document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP > ul > div > li:nth-child(12)").scrollHeight/{});'.format(value)) # scroll the page upto some value	
		# Wait to load page 
		time.sleep(5)
		#Get new scroll height after loading 
		new_height=driver.execute_script('return document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollHeight')
		if last_height==new_height:
			break
		last_height=new_height
		value+=0.1
	
	while 1: # starting scrolling fastly to load all the data we want 
		last_height=driver.execute_script('return document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollHeight')# Get scroll height
		driver.execute_script('document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollTo(0,document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollHeight)')# scroll down the page to it's height 
		time.sleep(5)# Wait to load page 
		new_height=driver.execute_script('return document.querySelector("body > div.RnEpo.Yx5HN > div > div.isgrP").scrollHeight')
		if new_height==last_height:
			break 
	#################################################
	time.sleep(5)
	driver1=driver.execute_script('return document.documentElement.outerHTML')
	driver.quit()
	# from here, I am starting the parsing of the followers data, so that we could get all the followers name and their count
	soup=BeautifulSoup(driver1,'html.parser').find('div',class_='PZuss').find_all('li')
	followers=soup
	global followerslist
	followerslist=[]
	for i in range(len(followers)):
		followerslist.append(followers[i].find('a',class_='FPmhX notranslate _0imsa ').text)# It will print all the names of the followers after scrolling and loading the whole page 
	count=len(followerslist)


	dic['name'] = name # name of the owner of the facebook id
	dic['followers'] = followerslist # friendslist of the owner person in a list
	dic['total'] = count # total number of followers
	print ('\nYour Followers-List is: ')

	
insta()
if dic:
	pprint.pprint(dic)
	# caching of the data in the local json file
	exists = path.exists(os.getcwd() + '/insta.json') # to get into the present directory where this json file locates
	if not exists:
	    with open (os.getcwd() + '/insta.json', 'w') as file:
	        file.write(json.dumps([]))
	with open(os.getcwd() + '/insta.json', 'r+') as content:
	    data=json.loads(content.read())
	    for i in data:
	    	if i['name']==name:
	    		i['followers']=followerslist
	    		break
	    else:
	    	data.append(dic)
	with open(os.getcwd()+'/insta.json','w') as files:
		files.write(json.dumps(data,indent=4,sort_keys=False))

	print('Total friends are: ', dic['total']) # It will tell you how many friends do you have. May differ with those that have been shown there. But it counts the original total one.






