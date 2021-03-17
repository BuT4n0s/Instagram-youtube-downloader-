import tkinter as Tkinter
from tkinter import simpledialog
from tkinter.font import Font
from tkinter import filedialog

import  threading 
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import requests
import os


is_checked=0
numberToGo=0


urls=[]
saveLocationFile=r"choose   files save lovation"
saveLocationName=""
bool_progrss=False
progressSaveLocationFile=r'choose  progress file save lovation  '
bool_choose_video=False
bool_choose_audio=False
bool_choose_audio_video=True


executable_path = r'driver\chromedriver.exe'
driver_path=r"load-extension="


driver_path+=r"driver\adblockk"

def page4():
	global text_load
	global text_load_num
	global msg_font
	global numberToGo 
	numberToGo = 0
	msg_font = Font(family="Helvetica",size=70)
	text_load =Tkinter.Label(top, bg="grey",bd=0,height=1,font="msg_font",text=" pls wait for the downlod to end ")
	text_load.place(relx = 0.5, rely = 0.5,anchor='center')
	text_load_num =Tkinter.Text(top, bg="grey",bd=0,height=1,width=30,font="msg_font")
	text_load_num.place(relx = 0.5, rely = 0.8,anchor='center')
	text_load_num.insert(Tkinter.END,str(numberToGo)+" / "+str(len(urls))+"  items  downloaded" )


	print("ok")
	x = threading.Thread(target=choose_download)
	x.setDaemon(True)
	x.start()




def download_insta(url,save_location,Name,num):

	s=requests.Session()
	f = s.get(url)
	htmlSource = f.text
	
	imgURL=re.findall(r'property="og:video"\scontent="(.*)"\s/>',f.text)
	try:
		testt=imgURL[0]
		
		fileName='video'+str(save_location)+str(Name)+"(a)("+num+").mp4"
		r=s.get(imgURL[0] )
		z=open(fileName,"wb")
		for chunk in r.iter_content(chunk_size=500):
			z.write(chunk)
		
	except :
		
		imgURL=re.findall(r'property="og:image"\scontent="(.*)"\s/>',f.text)
		fileName=str(save_location)+str(Name)+"(a)("+num+").jpg"
		r=s.get(imgURL[0] )
		z=open(fileName,"wb")
		z.write(r.content)




def get_urls(vido_url,executable_path,driver_path):

	caps = DesiredCapabilities.CHROME
	caps['goog:loggingPrefs'] = {'performance': 'ALL'}

	
	os.environ["webdriver.chrome.driver"] = executable_path

	chrome_options = Options()
	chrome_options.add_argument( driver_path )
	chrome_options.add_argument('--headless')

	driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options,desired_capabilities=caps)
	driver.get(vido_url)
	video=[]
	while len(video) <= 3:
		
	
		time.sleep(2)
		network=json.dumps(driver.get_log('performance'))
		video=re.findall(r'"url\\":\\"(https://r.[^\.]*.googlevideo.com/videoplayback[^}"]*)',network)
	driver.quit()

	for i in video :
		if "audio" in i:
			audio_url = i
			break

	for i in video :
		if "video" in i:
			video_url = i
			break

	audio_url=re.sub(r'&range=[^&]*&', '&', audio_url)
	video_url=re.sub(r'&range=[^&]*&', '&', video_url)
	return audio_url,video_url


def get_video(video_url,save_location):
	s=requests.Session() 
	r=s.get(video_url)

	video_file = open(save_location+"vid.mp4","wb")
	for chunk in r.iter_content(chunk_size=500):	
		video_file.write(chunk)

def get_audio(audio_url,save_location):

	s=requests.Session() 
	r=s.get(audio_url)
	audio_file = open(save_location+"audio.weba","wb")
	for chunk in r.iter_content(chunk_size=500):		
		audio_file.write(chunk)


def convert_audio(save_location,Name,num):
	ffmpeg="ffmpeg -i "+str(save_location)+"audio.weba "+str(save_location)+str(Name)+"(a)("+num+").mp3" 
	os.system(ffmpeg)

def convert_video(save_location,Name,num):
	ffmpeg="ffmpeg -y -i "+str(save_location)+"vid.mp4 -pix_fmt yuv420p -crf 18 "+str(save_location)+str(Name)+"(a)("+num+").mp4"
	os.system(ffmpeg)
def convert_video_audio (save_location,Name,num):
	ffmpeg="ffmpeg -y -i "+str(save_location)+"vid.mp4  -i "+str(save_location)+"audio.weba -crf 18 -pix_fmt yuv420p -c:a aac -strict experimental "+str(save_location)+str(Name)+"(v,a)("+num+").mp4"
	os.system(ffmpeg)

def remove_files(save_location):
	try:
		os.remove(save_location+"vid.mp4")
	except:
		x=1
	try:
		os.remove(save_location+"audio.weba")
	except:
		x=2


def choose_download():
	global urls
	global saveLocationFile
	global saveLocationName
	global bool_progrss
	global progressSaveLocationFile
	global bool_choose_video
	global bool_choose_audio
	global bool_choose_audio_video

	global executable_path
	global driver_path

	global numberToGo
	numberToGo=0
	saveLocationFile=saveLocationFile.rstrip("\n")
	saveLocationFile=re.sub(r'/', r'\\', saveLocationFile)
	saveLocationFile+="\\"
	num =0
	for url in urls :		
		num += 1
		if "youtube" in url:
			audio_url,video_url=get_urls(url,executable_path,driver_path)
			if bool_choose_audio_video or bool_choose_video and bool_choose_audio :
				get_video(video_url,saveLocationFile)
				get_audio(audio_url,saveLocationFile)
			elif bool_choose_video :
				get_video(video_url,saveLocationFile)
			elif bool_choose_audio:
				get_audio(audio_url,saveLocationFile)


			if bool_choose_video:
				convert_video(saveLocationFile,saveLocationName,str(num))
			if bool_choose_audio:
				convert_audio(saveLocationFile,saveLocationName,str(num))
			if bool_choose_audio_video:
				convert_video_audio (saveLocationFile,saveLocationName,str(num))
		elif "instagram" in url:
			download_insta(url,saveLocationFile,saveLocationName,str(num))

		remove_files(saveLocationFile)
		numberToGo+=1
		text_load_num.delete('1.0', Tkinter.END)
		text_load_num.insert(Tkinter.END,str(numberToGo)+"/"+str(len(urls))+"items to download" )



				











def switchButtonState(button): 
	if (button['state'] == 'normal'):
		button['state'] = 'disabled' 
	else: 
		button['state'] ='normal'
def switchTextState1(text): 
	if (text['fg'] == 'black'):
		text['fg'] = 'grey' 
	else: 
		text['fg'] ='black'
def switchTextState2(text): 
	if (text['fg'] == 'black'):
		text['fg'] = 'white' 
	else: 
		text['fg'] ='black'

def error_pop(msg):
	global top
	global label_error

	label_error = Tkinter.Label(top,bg="grey",bd=0,fg='white',text=msg)
	label_error.pack()
	label_error.place(relx = 0.5, rely = 0.9,anchor='center')

def del_error_pop():
	global label_error
	try:
		label_error.destroy()
	except:
		x=1

def check_choose_video_def():
	global bool_choose_video


	if bool_choose_video==False:
		bool_choose_video=True
	else:
		bool_choose_video=False

def check_choose_audio_def():
	global bool_choose_audio

	if bool_choose_audio==False:
		bool_choose_audio=True
	else:
		bool_choose_audio=False

def check_choose_audio_video_def():
	global bool_choose_audio_video

	if bool_choose_audio_video==False:
		bool_choose_audio_video=True
	else:
		bool_choose_audio_video=False


def check_progress_creat_def():
	global check_progress_creat
	global button_progress_Save_Location
	global text_progress_Save_Location1
	global text_progress_Save_Location2

	global bool_progrss

	del_error_pop()

	if bool_progrss==0:
		switchTextState1(text_progress_Save_Location1)
		switchTextState2(text_progress_Save_Location2)
		switchButtonState(button_progress_Save_Location)
		bool_progrss=True
	else:
		switchTextState1(text_progress_Save_Location1)
		switchTextState2(text_progress_Save_Location2)
		switchButtonState(button_progress_Save_Location)	
		bool_progrss=False
def Progress_Save_Location_Browse():
	text_progress_Save_Location1.configure(state='normal')
	progressSaveLocation = filedialog.askdirectory()

	text_progress_Save_Location1.delete('1.0', Tkinter.END)
	text_progress_Save_Location1.insert(Tkinter.END, progressSaveLocation)	
	text_progress_Save_Location1.configure(state='disabled')

def Save_Location_Browse():
	
	text_Save_Location1.configure(state='normal')
	saveLocation = filedialog.askdirectory()

	text_Save_Location1.delete('1.0', Tkinter.END)
	text_Save_Location1.insert(Tkinter.END, saveLocation)
	text_Save_Location1.configure(state='disabled')


def next_page3():
	global top
	global button_next3
	global button_previous3
	global button_Save_Location
	global text_Save_Location1
	global text_Save_Location2
	global entry_Save_Name
	global text_Save_Name2
	global check_progress_creat
	global button_progress_Save_Location
	global text_progress_Save_Location1
	global text_progress_Save_Location2
	global check_choose_video
	global check_choose_audio
	global check_choose_audio_video

	global saveLocationFile
	global saveLocationName
	global progressSaveLocationFile
	global bool_choose_video
	global bool_choose_audio
	global bool_choose_audio_video

	del_error_pop()

	text_Save_Location1.configure(state='normal')
	text_progress_Save_Location1.configure(state='normal')

	saveLocationFile=text_Save_Location1.get("1.0","end")
	saveLocationName=entry_Save_Name.get()
	progressSaveLocationFile=text_progress_Save_Location1.get("1.0","end")



	
	button_next3.destroy()
	button_previous3.destroy()
	button_Save_Location.destroy()
	text_Save_Location1.destroy()
	text_Save_Location2.destroy()
	entry_Save_Name.destroy()
	text_Save_Name2.destroy()
	check_progress_creat.destroy()
	button_progress_Save_Location.destroy()
	text_progress_Save_Location1.destroy()
	text_progress_Save_Location2.destroy()
	check_choose_video.destroy()
	check_choose_audio.destroy()
	check_choose_audio_video.destroy()

	

	if "save lovation" not in saveLocationFile:
		if saveLocationName !="":
			

				
			page4()		

		else:
			error_pop("you must choose a name for your files")
			page3()
			

	else:
		error_pop("you must choose a save lovation")
		page3()





	
	
def previous_page3():
	global top
	global button_next3
	global button_previous3
	global button_Save_Location
	global text_Save_Location1
	global text_Save_Location2
	global entry_Save_Name
	global text_Save_Name2
	global check_progress_creat
	global button_progress_Save_Location
	global text_progress_Save_Location1
	global text_progress_Save_Location2
	global check_choose_video
	global check_choose_audio
	global check_choose_audio_video

	global saveLocationFile
	global saveLocationName
	global progressSaveLocationFile
	global bool_choose_video
	global bool_choose_audio
	global bool_choose_audio_video

	del_error_pop()

	text_Save_Location1.configure(state='normal')
	text_progress_Save_Location1.configure(state='normal')

	saveLocationFile=text_Save_Location1.get("1.0","end")
	saveLocationName=entry_Save_Name.get()
	progressSaveLocationFile=text_progress_Save_Location1.get("1.0","end")



	
	button_next3.destroy()
	button_previous3.destroy()
	button_Save_Location.destroy()
	text_Save_Location1.destroy()
	text_Save_Location2.destroy()
	entry_Save_Name.destroy()
	text_Save_Name2.destroy()
	check_progress_creat.destroy()
	button_progress_Save_Location.destroy()
	text_progress_Save_Location1.destroy()
	text_progress_Save_Location2.destroy()
	check_choose_video.destroy()
	check_choose_audio.destroy()
	check_choose_audio_video.destroy()

	page2()
	

def page3 ():
	global top
	global button_next3
	global button_previous3
	global button_Save_Location
	global text_Save_Location1
	global text_Save_Location2
	global entry_Save_Name
	global text_Save_Name2
	global check_progress_creat
	global button_progress_Save_Location
	global text_progress_Save_Location1
	global text_progress_Save_Location2
	global check_choose_video
	global check_choose_audio
	global check_choose_audio_video

	global saveLocationFile
	global saveLocationName
	global progressSaveLocationFile
	global bool_choose_video
	global bool_choose_audio
	global bool_choose_audio_video

	

	button_Save_Location = Tkinter.Button(text="Browse",command=Save_Location_Browse)
	button_Save_Location.place(x=560,y=80,height=20,width=50)

	text_Save_Location1 =Tkinter.Text(top, bg="white",height=1,width=50)
	text_Save_Location1.place(x=140,y=80)
	text_Save_Location1.insert(Tkinter.END, saveLocationFile)
	text_Save_Location1.configure(state='disabled')

	text_Save_Location2 =Tkinter.Text(top, bg="grey",bd=0,height=1,width=14)
	text_Save_Location2.place(x=10,y=80)
	text_Save_Location2.insert(Tkinter.END, " Save location:")
	text_Save_Location2.configure(state='disabled')


	entry_Save_Name =Tkinter.Entry(top, bg="white")
	entry_Save_Name.place(x=140,y=150)
	entry_Save_Name.insert(0,saveLocationName)
	

	text_Save_Name2 =Tkinter.Text(top, bg="grey",bd=0,height=1,width=14)
	text_Save_Name2.place(x=10,y=150)
	text_Save_Name2.insert(Tkinter.END, " Save name:")
	text_Save_Name2.configure(state='disabled')

	check_progress_creat = Tkinter.Checkbutton(top,text ="continue with a  progress file ",font="button_font",background='grey',command =check_progress_creat_def )
	check_progress_creat.pack()
	check_progress_creat.place(x=15,y=200)
	if (bool_progrss == False):
		check_progress_creat.deselect()
	else: 
		check_progress_creat.select()



	button_progress_Save_Location = Tkinter.Button(text="Browse",command=Progress_Save_Location_Browse)
	button_progress_Save_Location.place(x=560,y=250,height=20,width=50)
	if (bool_progrss == False):
		button_progress_Save_Location['state'] = 'disabled' 
		
	else: 
		button_progress_Save_Location['state'] ='normal'
		


	text_progress_Save_Location1 =Tkinter.Text(top,bg="white",height=1,width=50)
	text_progress_Save_Location1.place(x=140,y=250)
	text_progress_Save_Location1.insert(Tkinter.END, progressSaveLocationFile)
	if (bool_progrss == False):
		text_progress_Save_Location1['fg'] = 'grey' 
	else: 
		text_progress_Save_Location1['fg'] ='black'
	text_progress_Save_Location1.configure(state='disabled')

	text_progress_Save_Location2 =Tkinter.Text(top,bg="grey",bd=0,height=1,width=14)
	text_progress_Save_Location2.place(x=10,y=250)
	text_progress_Save_Location2.insert(Tkinter.END, "prog location:")
	if (bool_progrss == False):
		text_progress_Save_Location2['fg'] = 'white' 
	else: 
		text_progress_Save_Location2['fg'] ='black'

	text_progress_Save_Location2.configure(state='disabled')

	check_choose_video = Tkinter.Checkbutton(top,text ="create vido file",font="button_font",background='grey',command =check_choose_video_def )
	check_choose_video.pack()
	check_choose_video.place(x=35,y=350)
	if (bool_choose_video == False):
		check_choose_video.deselect()
	else: 
		check_choose_video.select()

	check_choose_audio = Tkinter.Checkbutton(top,text ="create audio file ",font="button_font",background='grey',command =check_choose_audio_def )
	check_choose_audio.pack()
	check_choose_audio.place(x=35,y=375)
	if (bool_choose_audio == False):
		check_choose_audio.deselect()
	else: 
		check_choose_audio.select()

	check_choose_audio_video = Tkinter.Checkbutton(top,text ="create audio+video  file ",font="button_font",background='grey',command =check_choose_audio_video_def )
	check_choose_audio_video.pack()
	check_choose_audio_video.place(x=35,y=400)
	if (bool_choose_audio_video == False):
		check_choose_audio_video.deselect()
	else: 
		check_choose_audio_video.select()

	button_next3 = Tkinter.Button(top,text ="start", command = next_page3)
	button_next3.pack()
	button_next3.place(x=780,y=500,height=35,width=60)

	button_previous3 = Tkinter.Button(top,text ="previous", command = previous_page3)
	button_previous3.pack()
	button_previous3.place(x=20,y=500,height=35,width=60)
	


def add_item():

	del_error_pop()

	item = simpledialog.askstring("Input", "Enter URl:")
	if item is not None:
		if "https://"   in item:
			listbox.insert('end', item)
		else:
			error_pop("Pls insert a valit URl: https://...")
	else :
		error_pop("You didn't insert any URL.")
	    

def delete_item():
	del_error_pop()

	try:
	    index = listbox.curselection()
	    listbox.delete(index)
	except:
		error_pop("No item selected to delete.")
	

def add_list():
	del_error_pop()

	filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =(("Text File", "*.txt"),) )
	try:
		file = open(filename,"r")
		list_urls=file.readlines()
		file.close()
		for url in list_urls:
			if "https://"   in url:
				listbox.insert('end', url)
			else:
				error_pop("Pls insert a valit URl: https://...")
	except:
		error_pop("You didn't select any file.")
	

def check_progress_def():
	global is_checked
	global button_add_progress_list
	global button_add_all_list

	del_error_pop()

	if is_checked==0:
		is_checked=1
		switchButtonState(button_add_progress_list)
		switchButtonState(button_add_all_list)
	else:
		is_checked=0
		switchButtonState(button_add_progress_list)
		switchButtonState(button_add_all_list)		
	

def add_progress_list():
	global done_url
	global all_urls

	del_error_pop()

	done_url=[]
	filename = filedialog.askopenfilename(initialdir =  "/", title = "Select the progress file", filetype =(("Text File", "*.txt"),) )
	try:
		file = open(filename,"r")
		done_urls=file.readlines()
		file.close()

		for url in done_urls:
			if "https://"   in url:
				done_url.append(url)
			else:
				error_pop("Pls insert a valit URl: https://...")
	except:
		error_pop("You didn't select any file.")

	try:
		for url1 in all_url:
			if url1 not in done_url:
				listbox.insert('end', url1)
	except:
		error_pop("You need to add an list.")
	
def add_all_list():	
	global all_url
	global done_url

	del_error_pop()

	all_url=[]
	filename = filedialog.askopenfilename(initialdir =  "/", title = "Select the list ", filetype =(("Text File", "*.txt"),) )
	try:
		file = open(filename,"r")
		all_urls=file.readlines()
		file.close()
		for url in all_urls:
			if "https://"   in url:
				all_url.append(url)
			else:
				error_pop("Pls insert a valit URl: https://...")
		for url1 in all_url:
			if url1 not in done_url:
				listbox.insert('end', url1)
					
	except:
		error_pop("You didn't select any file.")

	try:
		for url1 in all_url:
			if url1 not in done_url:
				listbox.insert('end', url1)
	except:
		error_pop("You need to add an progress list.")
	
def next_page2():
	global button_next2
	global button_previous2
	global button_add_item
	global button_delete_item
	global button_add_list
	global listbox
	global check_progress
	global button_add_progress_list
	global button_add_all_list
	global urls

	del_error_pop()

	urls=[]
	for i in range (0,listbox.size()):
		urls.append(listbox.get(i) )
	if len(urls)!=0:
		button_add_item.destroy()
		button_delete_item.destroy()
		button_add_list.destroy()
		listbox.destroy()
		check_progress.destroy()
		button_add_progress_list.destroy()
		button_add_all_list.destroy()

		button_next2.destroy()
		button_previous2.destroy()

		page3()
	else:
		error_pop("pls choose at least one item to download")
	


def previous_page2():
	global button_next2
	global button_previous2
	global button_add_item
	global button_delete_item
	global button_add_list
	global listbox
	global check_progress
	global button_add_progress_list
	global button_add_all_list
	global urls

	del_error_pop()

	urls=[]
	for i in range (0,listbox.size()):
		urls.append(listbox.get(i) )

	button_add_item.destroy()
	button_delete_item.destroy()
	button_add_list.destroy()
	listbox.destroy()
	check_progress.destroy()
	button_add_progress_list.destroy()
	button_add_all_list.destroy()

	button_next2.destroy()
	button_previous2.destroy()

	page1()
	

def page2():
	global top
	global button_next2
	global button_previous2
	global button_add_item
	global button_delete_item
	global button_add_list
	global listbox
	global check_progress
	global button_add_progress_list
	global button_add_all_list

	global is_checked
	global urls
	

	list_font = Font(family="Helvetica",size=20)
	button_font = Font(family="Helvetica",size=20)

	listbox = Tkinter.Listbox(top,bg="white",bd=3,font="list_font")
	listbox.pack()
	listbox.place(x=20,y=30,height=400,width=350)
	for url in urls:
		listbox.insert('end', url)

	button_add_item = Tkinter.Button(top,text ="add item",font="button_font", command = add_item)
	button_add_item.pack()
	button_add_item.place(x=600,y=75,height=50,width=100)

	button_delete_item = Tkinter.Button(top,text ="delete item",font="button_font", command = delete_item)
	button_delete_item.pack()
	button_delete_item.place(x=600,y=150,height=50,width=100)

	button_add_list = Tkinter.Button(top,text ="add list",font="button_font", command = add_list)
	button_add_list.pack()
	button_add_list.place(x=600,y=225,height=50,width=100)


	check_progress = Tkinter.Checkbutton(top,text ="continue with a  progress file ",font="button_font",background='grey',command =check_progress_def )
	check_progress.pack()
	check_progress.place(x=600,y=300)
	if (is_checked == 0):
		check_progress.deselect()
	else: 
		check_progress.select()

	button_add_progress_list = Tkinter.Button(top,text ="progress list", command = add_progress_list)
	button_add_progress_list.pack()
	button_add_progress_list.place(x=550,y=350,height=40,width=75)	
	if (is_checked == 0):
		button_add_progress_list['state'] = 'disabled' 
	else: 
		button_add_progress_list['state'] ='normal'

	button_add_all_list = Tkinter.Button(top,text ="list", command = add_all_list)
	button_add_all_list.pack()
	button_add_all_list.place(x=650,y=350,height=40,width=75)
	if (is_checked == 0):
		button_add_all_list['state'] = 'disabled' 
	else: 
		button_add_all_list['state'] ='normal'


	button_next2 = Tkinter.Button(top,text ="next", command = next_page2)
	button_next2.pack()
	button_next2.place(x=780,y=500,height=35,width=60)

	button_previous2 = Tkinter.Button(top,text ="previous", command = previous_page2)
	button_previous2.pack()
	button_previous2.place(x=20,y=500,height=35,width=60)



def next_page1():
	global Welcome_text
	global button_next1

	del_error_pop()

	Welcome_text.destroy()
	button_next1.destroy()

	page2()
	

def page1():
	global Welcome_text
	global button_next1
	global top




	Welcome_text =Tkinter.Text(top, bg="grey",height=30,width=90)
	Welcome_text.pack()
	Welcome_text.insert(Tkinter.END, "\n\n\n")
	Welcome_text.insert(Tkinter.END,"                    _         _           \n                   | |       | |          \n  _   _  ___  _   _| |_ _   _| |__   ___  \n | | | |/ _ \| | | | __| | | | '_ \ / _ \ \n | |_| | (_) | |_| | |_| |_| | |_) |  __/ \n  \__, |\___/ \__,_|\__|\__,_|_.__/ \___| \n   __/ |                                  \n  |___/                                   \n")
	Welcome_text.insert(Tkinter.END,"                 _           _                                  \n                (_)         | |                                 \n                 _ _ __  ___| |_ __ _  __ _ _ __ __ _ _ __ ___  \n                | | '_ \/ __| __/ _` |/ _` | '__/ _` | '_ ` _ \ \n                | | | | \__ \ || (_| | (_| | | | (_| | | | | | |\n                |_|_| |_|___/\__\__,_|\__, |_|  \__,_|_| |_| |_|\n                                       __/ |                    \n                                      |___/                     \n")	
	Welcome_text.insert(Tkinter.END,"                                  _                     _                 _           \n                                 | |                   | |               | |          \n                               __| | _____      ___ __ | | ___   __ _  __| | ___ _ __ \n                              / _` |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|\n                             | (_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   \n                              \__,_|\___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   \n")
	Welcome_text.insert(Tkinter.END, "\n\n\n                                                                              Bou tanos")

	button_next1 = Tkinter.Button(top,text ="next", command = next_page1)
	button_next1.pack()
	button_next1.place(x=780,y=500,height=35,width=60)

	top.mainloop()


def start():
	global top

	top = Tkinter.Tk()
	top.geometry("850x550")
	top.configure(background='grey')
	page1()

start()

print(urls,saveLocationFile,saveLocationName,bool_progrss,progressSaveLocationFile,bool_choose_video,bool_choose_audio,bool_choose_audio_video)
