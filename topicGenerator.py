import xml.etree.ElementTree as ET

import os
import tempfile

import __main__ as main

media_count = 0

def generate_topics_xml(base, myjson, type, location):
	main.p_counter = 0
	for lesson in myjson['lessons']:
		main.p_counter += 1
		for topic  in lesson['topics']:
			main.p_counter += 1
			tree = ET.parse(base)
			tree_root = tree.getroot()
			topic_id = main.p_counter
			tdir = location + '/t%d/' %topic_id

			if type == 'topic':
				os.makedirs(location + '/t%d/' %topic_id)
				src = (os.getcwd() + '/data/t/')
				main.Core.copytree(src, tdir)

			set_topic_xml({ 'tree_root': tree_root, 'topic': topic, 'type': type, 'location' : tdir, 'id' : topic_id})


			temp = tempfile.NamedTemporaryFile(mode='w+b', dir=tdir, delete=False)

			tree.write(temp, encoding="UTF-8")
			temp.close()

			if type == 'topic':
				filename = tdir + 't%d' %topic_id
			else:
				filename = tdir + 'editor'

			os.rename(temp.name, '%s.xml' %filename)

def get_topic(args):
	global media_count
	medi_count = 3

	main.p_counter += 1
	t = args['tree_root']

	t_objective = t.find('Objective')
	t_learning_point = t.find('LearningPoint')
	t_page_sub = t_learning_point.find('PageStub')
	
	t.attrib['id'] = 't%d' %args['id']
	t_objective.attrib['id'] = 'o%d' %main.p_counter

	t_objective.attrib['tested'] = 'true' # if len(args['topic']['assessment']) > 0 else 'false'

	t_objective.find('text').text = args['topic']['learning_objective']
	main.p_counter += 1

	try:
		for assessment in args['topic']['assessment']:
			p = 'p%d' %main.p_counter 		
			pageElement = ET.Element('PageStub', {'file': '%s.xml' %p, 'id' : '%s' %p})
			t_objective.append(pageElement)
			main.AG.set_assessment({'location' : args['location'], 'assessment' : assessment, 'topic_id' : t.attrib['id'], 'audio_number' : medi_count})
			main.p_counter += 1
			medi_count +=1
	except:
		pass

	t_learning_point.attrib['id']= 'lp%d' %main.p_counter
	main.p_counter += 1

	t_page_sub.attrib['id']= 'p%d' %main.p_counter
	t_page_sub.attrib['file']= 'p%d.xml' %main.p_counter

	set_learning_page(args)

	return t

def get_t_editor(args):
	global media_count
	main.p_counter += 1
	audio_name = None
	video_name = None
	assessment_audio_id =  't%d' %args['id']
	media_count = 3

	t = args['tree_root']	

	t_objective = t.find('ObjectivesObject').find('ObjectiveItem')
	t_learning_point_item = t.find('LearningPointObject').find('LearningPointItem')
	t_page_item = t_learning_point_item.find('PageObject').find('PageItem')

	t.attrib['id'] = 'T%d' %args['id']
	t_objective.attrib['id'] = 'O%d' %main.p_counter


	t_objective.attrib['tested'] = 'true' # if len(args['topic']['assessment']) > 0 else 'false'

	t_objective.find('text').text = args['topic']['learning_objective']
	main.p_counter += 1

	if args['topic']['name'].lower() == 'course introduction' :
		video_name = audio_name = 'course_intro'
	else:
		audio_name = '%s_aud_0002' %args['topic']['book_id']
		video_name = '%s_vid_0001' %args['topic']['book_id']


	t_video = t_page_item.find('VideoModelItem').find('PlatformContainerModelItem').find('PlatformModelItem')
	t_video.attrib['filename']= '%s' %video_name

	t_audio = t_page_item.find('AudioModelItem')
	t_audio.attrib['file'] = '%s.spx' %audio_name

	try:
		for assessment in args['topic']['assessment']:
			targetElement = t_objective.find('ChildPages')
			pageItem = main.AG.get_assessment_element(assessment, assessment_audio_id, media_count)
			targetElement.append(pageItem)
			main.p_counter += 1
			media_count += 1
	except:
		pass

	t_learning_point_item.attrib['id']= 'LP%d' %main.p_counter
	main.p_counter += 1

	t_page_item.attrib['id']= 'P%d' %main.p_counter
	t_page_item.attrib['name']= 'P%d - Video Standard Caption' %main.p_counter

	return t

def set_learning_page(args):
	audio_name = None
	video_name = None
	base = (os.getcwd() + '/data/xml/base_p.xml')
	tree = ET.parse(base)
	tree_root = tree.getroot()
	location = args['location']

	if args['topic']['name'].lower() == 'course introduction' :
		video_name = audio_name = 'course_intro'
	else:
		audio_name = '%s_aud_0002' %args['topic']['book_id']
		video_name = '%s_vid_0001' %args['topic']['book_id']

	tree_root.attrib['id'] = 'P%d' %main.p_counter

	audio_item = tree_root.find('audio_item')
	audio_item.attrib['file'] = '%s.spx' %audio_name
	for video in tree_root.iter('video'):
		if video.attrib['type'] == 'mp4':
			video.attrib['file'] = '/media/video/%s.mp4' %video_name
		else:
			video.attrib['file'] = '/media/video/%s.flv' %video_name

	temp = tempfile.NamedTemporaryFile(mode='w+b', dir=location, delete=False)
	
	tree.write(temp, encoding="UTF-8")
	temp.close()

	filename = location + 'p%d' %main.p_counter

	os.rename(temp.name, '%s.xml' %filename)

def set_topic_xml(args):
	if args['type'] == 'topic':
		xml = get_topic(args)
	else:
	 	xml = get_t_editor(args)

	xml.find('topicTitle').text = args['topic']['name']
	xml.attrib['estimatedDuration'] = '%d' %args['topic']['planned_duration']
	xml.attrib['keywords'] = args['topic']['keywords']
	xml.attrib['name'] =  "T%d - %s" % (args['id'], args['topic']['name'])
	xml.attrib['maxMediaID'] = '%d' %(media_count)
