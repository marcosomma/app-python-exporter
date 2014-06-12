import xml.etree.ElementTree as ET

import os
import tempfile

import __main__ as main


def get_course_topic_xml(args):
	if args['type'] == 'course':
		xml = get_topic_course(args)
	else:
		xml = get_topic_editor(args)

	t_id = 'T%d' %args['id']

	xml.attrib['name'] = '%s - %s' %(t_id, args['topic']['name'])

	t_type = ET.SubElement(xml, 'topicType')
	t_type.text = 'Instruction'
	t_assessment = ET.SubElement(xml, 'assessments')
	t_assessment.attrib['testable_objectives'] = '1'

	# try:
	# 	if len(args['topic']['assessment'])>0:
	# 		t_assessment = ET.SubElement(xml, 'assessments')
	# 		t_assessment.attrib['testable_objectives'] = '1'
	# 	else:
	# 		t_assessment = ET.SubElement(xml, 'assessments')
	# 		t_assessment.attrib['testable_objectives'] = '1'
	# except:
	# 	pass

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

def get_lesson_xml(args):
	if args['type'] == 'course':
		xml = get_lesson_course(args)
	else:
		xml = get_lesson_editor(args)

	l_id = 'L%d' %args['id']
	xml.attrib['name'] = "%s - %s" % (l_id, args['lesson']['name'])
	xml.attrib['hasVideo'] = 'true'

	title = ET.SubElement(xml, 'lessonTitle')
	title.text =  args['lesson']['name']

	return xml

def get_topic_course(args):
	t_id = 't%d' %args['id']
	t = ET.SubElement(args['lesson_xml'], 'TopicStub')
	t.attrib['id'] = t_id
	t.attrib['file'] = '%s.xml' % t_id
	t.attrib['sourceMaterial'] = ''
	t.attrib['transcript'] = 'transcript.html'
	t.attrib['estimatedDuration'] =  "%d" %args['topic']['planned_duration']
	t.attrib['keywords'] =  args['topic']['keywords']
	t.attrib['maxMediaID'] =  '4'

	t_title = ET.SubElement(t, 'topicTitle')
	t_title.text = args['topic']['name']

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

def generate_course_xml(base, myjson, type, location):
	tree = ET.parse(base)
	tree_root = tree.getroot()
	course_duration = 0
	main.p_counter = 0

	for lesson in myjson['lessons']:
		main.p_counter += 1
		lesson_id = main.p_counter

		l = get_lesson_xml({ 'lesson': lesson, 'type': type, 'id' : lesson_id})

		for topic  in lesson['topics']:
			main.p_counter += 1
			course_duration += topic['planned_duration']
			topic_id = main.p_counter

			try:
				for assessment in topic['assessment']:
					main.p_counter += 1
			except:
				pass

			t = get_course_topic_xml({ 'lesson_xml': l, 'topic': topic, 'type': type, 'id' : topic_id})

			main.p_counter += 3

		tree_root.append(l)

 	set_course_attribs({ 'tree_root': tree_root, 'course': myjson ,'course-duration' : course_duration, 'type': type})

	temp = tempfile.NamedTemporaryFile(mode='w+b', dir=location, delete=False)
	
	
	tree.write(temp, encoding="UTF-8")
	temp.close()

	if type == 'course':
		filename = location + myjson['identifier']
	else:
		filename = location + 'editor'

	os.rename(temp.name, '%s.xml' %filename)


def set_course_attribs(args):
	root = args['tree_root']
	course = args['course']

	course_type = main.help.get_course_type(course['identifier'])

	root.attrib['courseNumber'] = course['identifier']
	# root.attrib['coursePublishedDuration'] = serialize_duration(args['course-duration'])
	root.attrib['coursePublishedDuration'] = '0.0'
	root.attrib['courseType'] = course_type
	root.attrib['id'] = course['identifier']
	root.attrib['baseID'] = '%d' %main.p_counter
	root.attrib['keywords'] = course['keywords']
	root.attrib['name'] = "%s - %s" % (course['identifier'], course['name'])
	root.attrib['sourceMaterial'] = course['source_material']
	root.attrib['transcripts'] =  'false' if course_type=='BS' else 'true'
	root.find('courseGoal').text = course['goal']
	root.find('courseTitle').text = course['name']
	root.find('courseTitle1').text = course['name']


	desc = ET.SubElement(root, 'courseDescription')
	desc.text = course['description']

	audience = ET.SubElement(root, 'courseTargetAudience')
	audience.text = course['target_audience']

	prerequisites = ET.SubElement(root, 'coursePrerequisites')
	prerequisites.text = course['prerequisites']