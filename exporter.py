from Tkinter import *           
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import askyesno, showinfo

import xml.etree.ElementTree as ET

import json
import os
import shutil
import tempfile
import sys

p_counter = 0

def open_file_system():
	selectfile = askopenfilename(title='Select an export file', filetypes=[('json','*.json')])
	if selectfile:
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
	else:
		return


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
	locsave = askdirectory(title='Select a destination folder')
	directory = locsave + '/%s/' %name

	if os.path.exists(directory):
		question = askyesno(title='Alert',message='This folder "%s" already exists in target location. Do you want to overwrite?' %name) 

		if not question: return

		shutil.rmtree(locsave + '/%s/' %name)
		os.makedirs(locsave + '/%s/' %name)
	else:
		os.makedirs(locsave + '/%s/' %name)
	
	try:
		copytree(new, directory)
		showinfo(title='Message',message='Done!') 
	except:
		showinfo(title='Error',message='Impossible to replace this folder "%s". Already in use from another program.' %name) 
		

def get_lesson_xml(args):
	if args['type'] == 'course':
		xml = get_lesson_course(args)
	else:
		xml = get_lesson_editor(args)

	l_id = 'L%d' %args['id']
	xml.attrib['name'] = "%s - %s" % (l_id, args['lesson']['name'])

	title = ET.SubElement(xml, 'lessonTitle')
	title.text =  args['lesson']['name']

	return xml


def get_lesson_course(args):
	l = ET.Element('Lesson')
	l.attrib['id'] = 'L%d' %args['id']

	return l


def get_lesson_editor(args):
	l = ET.Element('LessonObject')
	l.attrib['id'] = 'L%d' %args['id']
	l.attrib['tcNodeStatus'] = 'False'
	l.attrib['commentStatus'] = 'None'

	return l


def get_course_topic_xml(args):
	if args['type'] == 'course':
		xml = get_topic_course(args)
	else:
		xml = get_topic_editor(args)

	t_id = 'T%d' %args['id']

	xml.attrib['name'] = '%s - %s' %(t_id, args['topic']['name'])
	xml.attrib['estimatedDuration'] = str(args['topic']['planned_duration'])
	xml.attrib['keywords'] =  args['topic']['keywords']

	t_type = ET.SubElement(xml, 'topicType')
	t_type.text = 'Instruction'

	t_title = ET.SubElement(xml, 'topicTitle')
	t_title.text = args['topic']['name']

	return xml


def get_topic_course(args):
	t_id = 't%d' %args['id']
	t = ET.SubElement(args['lesson_xml'], 'TopicStub')
	t.attrib['id'] = t_id
	t.attrib['file'] = '%s.xml' % t_id
	t.attrib['topicApproxDuration'] = "%s" %args['topic']['planned_duration']
	t.attrib['sourceMaterial'] = ''
	t.attrib['transcript'] = 'transcript.html'

	return t


def get_topic_editor(args):
	t = ET.SubElement(args['lesson_xml'], 'TopicObject')
	t.attrib['id'] = 'T%d' %args['id']
	t.attrib['file'] = 'editor.xml'
	t.attrib['tcNodeStatus'] = 'False'
	t.attrib['descNodeTcStatus'] = 'False'
	t.attrib['commentStatus'] = 'None'
	t.attrib['hasVideo'] = 'true'

	return t


def set_topic_xml(args):
	if args['type'] == 'topic':
		xml = set_topic(args)
		set_learning_page(args)
	else:
	 	xml = set_t_editor(args)


	xml.find('topicTitle').text = args['topic']['name']
	xml.attrib['topicApproxDuration'] =args['topic']['planned_duration']
	xml.attrib['estimatedDuration'] =args['topic']['planned_duration']
	xml.attrib['keywords'] = args['topic']['keywords']
	xml.attrib['name'] =  "T%d - %s" % (args['id'], args['topic']['name'])

def set_topic(args):
	global p_counter 

	p_counter += 1
	t = args['tree_root']

	t.attrib['id'] = 't%d' %args['id']
	t_objective = t.find('Objective')
	t_objective.attrib['id'] = 'o%d' %p_counter
	t_objective.find('text').text = args['topic']['learning_objective']
	p_counter += 1
	
	t_learning_point = t.find('LearningPoint')
	t_learning_point.attrib['id']= 'lp%d' %p_counter
	p_counter += 1

	t_page_sub = t_learning_point.find('PageStub')
	t_page_sub.attrib['id']= 'p%d' %p_counter
	t_page_sub.attrib['file']= 'p%d.xml' %p_counter

	return t


def set_t_editor(args):
	global p_counter 
	
	p_counter += 1
	t = args['tree_root']	

	t.attrib['id'] = 'T%d' %args['id']
	t_objective = t.find('ObjectivesObject').find('ObjectiveItem')
	t_objective.attrib['id'] = 'O%d' %p_counter
	t_objective.find('text').text = args['topic']['learning_objective']
	p_counter += 1
	
	t_learning_point_item = t.find('LearningPointObject').find('LearningPointItem')
	t_learning_point_item.attrib['id']= 'LP%d' %p_counter
	p_counter += 1

	t_page_item = t_learning_point_item.find('PageObject').find('PageItem')
	t_page_item.attrib['id']= 'P%d' %p_counter
	t_page_item.attrib['name']= 'P%d - Video Standard Caption' %p_counter

	t_video = t_page_item.find('VideoModelItem').find('PlatformContainerModelItem').find('PlatformModelItem')
	t_video.attrib['filename']= args['topic']['book_id']

	t_audio = t_page_item.find('AudioModelItem')
	t_audio.attrib['file'] = '%s.spx' %args['topic']['book_id']

	return t

def set_learning_page(args):
	global p_counter 
	base = (os.getcwd() + '/data/xml/base_p.xml')
	tree = ET.parse(base)
	tree_root = tree.getroot()
	location = args['location']

	tree_root.attrib['id'] = 'P%d' %p_counter

	audio_item = tree_root.find('audio_item')
	audio_item.attrib['file'] = '%s.spx' %args['topic']['book_id']

	for video in tree_root.iter('video'):
		if video.attrib['type'] == 'mp4':
			video.attrib['file'] = '/media/video/%s.mp4' %args['topic']['book_id']
		else:
			video.attrib['file'] = '/media/video/%s.flv' %args['topic']['book_id']

	temp = tempfile.NamedTemporaryFile(mode='w+b', dir=location, delete=False)
	
	tree.write(temp, encoding="UTF-8")
	temp.close()

	filename = location + 'p%d' %p_counter

	os.rename(temp.name, '%s.xml' %filename)


def serialize_duration(minutes):
    return "%.1f" % (minutes / 60)


def set_course_attribs(args):
	root = args['tree_root']
	course = args['course']

	root.attrib['name'] = "%s - %s" % (course['identifier'], course['name'])
	root.attrib['courseNumber'] = course['identifier']
	root.attrib['sourceMaterial'] = course['source_material']
	root.attrib['keywords'] = course['keywords']
	root.attrib['coursePublishedDuration'] = serialize_duration(course['duration'])
	root.find('courseTitle').text = course['name']
	root.find('courseTitle1').text = course['name']
	root.find('courseGoal').text = course['goal']
	
	if args['type'] == 'course':
		root.attrib['id'] = course['identifier']

	desc = ET.SubElement(root, 'courseDescription')
	desc.text = course['description']

	audience = ET.SubElement(root, 'courseTargetAudience')
	audience.text = course['target_audience']

	prerequisites = ET.SubElement(root, 'coursePrerequisites')
	prerequisites.text = course['prerequisites']


def generate_course_xml(base, myjson, type, location):
	global p_counter 
	tree = ET.parse(base)
	tree_root = tree.getroot()
	p_counter = 0

 	set_course_attribs({ 'tree_root': tree_root, 'course': myjson , 'type': type})

	for lesson in myjson['lessons']:
		p_counter += 1
		lesson_id = p_counter

		l = get_lesson_xml({ 'lesson': lesson, 'type': type, 'id' : lesson_id})

		for topic  in lesson['topics']:
			p_counter += 1
			topic_id = p_counter

			t = get_course_topic_xml({ 'lesson_xml': l, 'topic': topic, 'type': type, 'id' : topic_id})

			p_counter += 3

		tree_root.append(l)


	temp = tempfile.NamedTemporaryFile(mode='w+b', dir=location, delete=False)
	
	
	tree.write(temp, encoding="UTF-8")
	temp.close()

	if type == 'course':
		filename = location + myjson['identifier']
	else:
		filename = location + 'editor'

	os.rename(temp.name, '%s.xml' %filename)


def generate_topics_xml(base, myjson, type, location):
	global p_counter 
	tree = ET.parse(base)
	tree_root = tree.getroot()
	p_counter = 0
	for lesson in myjson['lessons']:
		p_counter += 1
		for topic  in lesson['topics']:
			p_counter += 1
			topic_id = p_counter
			tdir = location + '/t%d/' %topic_id

			if type == 'topic':
				os.makedirs(location + '/t%d/' %topic_id)
				src = (os.getcwd() + '/data/t/')
				copytree(src, tdir)

			set_topic_xml({ 'tree_root': tree_root, 'topic': topic, 'type': type, 'location' : tdir, 'id' : topic_id})


			temp = tempfile.NamedTemporaryFile(mode='w+b', dir=tdir, delete=False)

			tree.write(temp, encoding="UTF-8")
			temp.close()

			if type == 'topic':
				filename = tdir + 't%d' %topic_id
			else:
				filename = tdir + 'editor'

			os.rename(temp.name, '%s.xml' %filename)


def create_course_xml(newlocation, myjson):
	course = (os.getcwd() + '/data/xml/base_c.xml')
	editor = (os.getcwd() + '/data/xml/base_c_editor.xml')
	topic = (os.getcwd() + '/data/xml/base_t.xml')
	t_editor = (os.getcwd() + '/data/xml/base_t_editor.xml')
	try:
		type = 'course'
		generate_course_xml(course, myjson, type, newlocation)
		type = 'editor'
		generate_course_xml(editor, myjson, type, newlocation)
		type = 'topic'
		generate_topics_xml(topic, myjson, type, newlocation)
		type = 't_editor'
		generate_topics_xml(t_editor, myjson, type, newlocation)
	except:
		showinfo(title='Error',message='The export file is not correct!') 
		return False
	
	return True

def exit():
	sys.exit(0)


root = Tk()
rtitle = root.title("Bridge")
root.minsize(400,350)
root.maxsize(400,350)
root.configure(background='#fcfcfc')

label = Label(root, text="Coursify Exporter",  font="Helvetica 20 bold ", background='#0f3e62', foreground="#fcfcfc")
label.config( width = 100)
label.pack( side ='top')

img = PhotoImage(file=("data/img/background.gif"))
img_label = Label(root, background='#fcfcfc', image = img)
img_label.pack( side ='top', fill = "both", expand = "yes")

botton_lable = Label(root, background='#0f3e62')
botton_lable.config( width = 100)
botton_lable.pack( side ='bottom', fill='both',)

exit_btn = Button(botton_lable, text="Exit", font="Helvetica 10 bold", background='#fcfcfc', foreground="#0f3e62", cursor="hand2", command=exit)
exit_btn.pack(side=RIGHT, fill='both', expand=False, padx=35, pady=10)
exit_btn.config( height = 1, width = 15)

open_btn = Button(botton_lable, text="Export", font="Helvetica 10 bold", background='#fcfcfc', foreground="#0f3e62", cursor="hand2", command=open_file_system)
open_btn.pack(side=LEFT, fill='both', expand=False, padx=35, pady=10)
open_btn.config( height = 1, width = 15)

root.mainloop()