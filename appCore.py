from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import askyesno, showerror 

import json
import os
import re 
import shutil
import sys
import tempfile

import __main__ as main

locsave = None

def open_file_system():
	global locsave
	disabled_btn()
	main.label_response.pack_forget()

	selectfile = askopenfilename(title='Select an export file', filetypes=[('json','*.json')])
	
	if not selectfile:
		activate_btn() 
		return

	locsave = askdirectory(title='Select a destination folder')

	if not locsave: 
		activate_btn()
		return

	show_response({'label_text' : "Processing...", 'label_background' : "#ffba00"})

	src = (os.getcwd() + '/data/course/')
	new = tempfile.mkdtemp()
	copytree(src,new)
	
	myfile=open(selectfile)
	myjson = json.load(myfile)
	myfile.close()

	temp = tempfile.NamedTemporaryFile(mode='w+b', dir=new, delete=False)
	temp.write('%s.crs' %myjson['identifier'])
	temp.close()
	os.rename(temp.name, '%s/%s.crs' %(new, myjson['identifier']))

	create_package(myjson, new)	

def copytree(src, new, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(new, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

def copyfile(src, dest, name):
	shutil.copy2(src, dest)

def create_package(myjson, new):
	newlocation = new + '/output/'
	if not create_course_xml(newlocation, myjson): return

	file_save(new, myjson['identifier'] )

def file_save(new, name):
	global locsave

	directory = locsave + '/%s/' %name

	try:
		if os.path.exists(directory):
			question = askyesno(title='Alert',message='This folder "%s" already exists in target location. Do you want to overwrite?' %name) 

			if not question: 
				label_response.pack_forget()
				activate_btn()
				return

			shutil.rmtree(locsave + '/%s/' %name)
			os.makedirs(locsave + '/%s/' %name)
		else:
			os.makedirs(locsave + '/%s/' %name)
		
		copytree(new, directory)
		show_response({'label_text' : "Successfully exported", 'label_background' : "#03db09"}, False, True)
	except:
		show_response({'label_text' : "Error", 'label_background' : "#db0303", 'error_text' : 'Impossible to replace this folder "%s". Already in use from another program.' %name}, True, True)


def create_course_xml(newlocation, myjson):
	course = (os.getcwd() + '/data/xml/base_c.xml')
	editor = (os.getcwd() + '/data/xml/base_c_editor.xml')
	topic = (os.getcwd() + '/data/xml/base_t.xml')
	t_editor = (os.getcwd() + '/data/xml/base_t_editor.xml')
	try:
		main.CG.generate_course_xml(course, myjson, 'course', newlocation)
		main.CG.generate_course_xml(editor, myjson, 'editor', newlocation)
		main.TG.generate_topics_xml(topic, myjson, 'topic', newlocation)
		main.TG.generate_topics_xml(t_editor, myjson, 't_editor', newlocation)
	except Exception as e:
		print e
		show_response({'label_text' : "Error", 'label_background' : "#db0303", 'error_text' : 'The export file is not correct!'}, True, True)
		return False
	
	return True

def activate_btn():
	main.exit_btn.config(state='normal')
	main.open_btn.config(state='normal')

def disabled_btn():
	main.exit_btn.config(state='disabled')
	main.open_btn.config(state='disabled')

def exit():
	sys.exit(0)		
	
def show_response(args, error=False, activate=False):
	main.label_response.config( text=args['label_text'], width = 100, foreground="#fcfcfc", background=args['label_background'])
	main.label_response.pack( side ='bottom')

	Tk.update(main.root)

	if error == True:
		showerror(title='Error',message=args['error_text']) 

	if activate == True:
		activate_btn()
