import xml.etree.ElementTree as ET

import re

def get_answer_mamc(id, type, layout, answer):
	content_category = 'answer_container,right_container,multiple_choice_container' if layout == 'wide' else 'answer_container,question_container,top_container,multiple_choice_container,left_container'
	content_id = "cont_ans,cont_right,cont_mc" if layout == 'wide' else 'cont_ans,cont_quest,cont_top,cont_mc,cont_left'
	
	attrib_answer = {
		'visible' : 'true',
		'id' : 'ansi',
		'tagName' : 'answer_item',
		'category' : 'standardText',
		'contCategory' : content_category,
		'contID' : content_id,
		'allowMultiple' :  'true',
		'allowMultiplesLimit' : '0',
		'component_id' : id,
		'min' : '2',
	}

	try:
		if answer['correct'] : attrib_answer['isCorrect'] = 'true'
	except:
		pass

	return ET.Element(type, attrib_answer)

def get_audio_attrib(audio_name, audio_number, type):
	number = "0%d" %audio_number if audio_number < 10 else "%d" %audio_number
	audio_file = "%s_aud_00%s.spx" %(audio_name, number) 

	audio_attrib = {
		'visible': "true",
		'id': "audioi",
		'category': "",
		'contCategory': "",
		'contID': "",
		'allowMultiple': "true",
		'allowMultiplesLimit': "0",
		'component_id': "audioi_01",
		'characterSelected': "false",
		'file': audio_file
	}

	if type=='editor' : audio_attrib['tagName'] = 'audio_item'

	return audio_attrib

def get_course_type(identifier):
	r_exp_dt = re.compile('^.+_dt_enus$')
	r_exp_bs = re.compile('^.+_bs_enus$')

	if (r_exp_dt.match(identifier)) :
		c_type = 'DT'

	elif (r_exp_bs.match(identifier)) :
		c_type = 'BS'

	else:
		c_type = 'IT'

	return c_type

def get_input_attrib():
	attrib_input = {
		'visible':"true",
		'id':"codetii",
		'tagName':"text_input_item",
		'category':"action_code",
		'contCategory':"answer2_container,answer2_container,top_container,shortanswer_container",
		'contID':"cont_an2,cont_an3,cont_top,cont_sa",
		'allowMultiple':"false",
		'allowMultiplesLimit':"9",
		'component_id':"codetii_01",
		'min':"1"
	}

	return attrib_input
	
def get_match_letter(number):
	letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
	position = number - 1

	return letters[position]

def get_page_attrib(name, id, type, layout = None):
	if type == 'mamc':
		strategy = "Multiple Choice"
		config_id = "multiple_choice_wide" if layout == 'wide' else "multiple_choice_standard"
		template_name = "Multiple Choice Wide" if layout == 'wide' else "Multiple Choice Standard"
		template_file = "multiple_choice_wide.xml" if layout == 'wide' else "multiple_choice_standard.xml"
		template_type = "9" if layout == 'wide' else "2" 
		style_category = "widePageStyle" if layout == 'wide' else "standard"
	elif type == 'matching_text':
		strategy = "Matching"
		config_id = "matching_standard_text"
		template_name = "Matching Standard Text"
		template_file = "matching_standard.xml"
		template_type = "11"
		style_category = "standard"
	elif type == 'rank_sequence':
		strategy = "Matching"
		config_id = "rank_sequence"
		template_name = "Rank/Sequence"
		template_file = "matching_standard.xml"
		template_type = "18"
		style_category = "standard"
	elif type == 'shortanswer_text':
		strategy = "Short Answer"
		config_id = "short_answer_text"
		template_name = "Short Answer Text"
		template_file = "short_answer_text.xml"
		template_type = "8"
		style_category = "standard"

	page_attrib = {
		'mode' : "Test Question",
		'strategy' : strategy,
		'name' : name,
		'templateConfigID' : config_id,
		'templateName' : template_name,
		'templateFileName' : template_file,
		'publishTemplateFileName' : template_file,
		'templateType' : template_type,
		'version' : "1",
		'templateCategory' : "question",
		'isChildPage' : "false",
		'tcNodeStatus' : "false",
		'commentStatus' : "None",
		'id' : id ,
		'styleCategory' : style_category ,
	}

	return page_attrib

def get_stemp_attrib(type, layout = None):
	if type == 'mamc':
		cont_category = "left_container,multiple_choice_container" if layout == 'wide' else "question_container,top_container,multiple_choice_container,left_container" 
		content_id = "cont_left,cont_mc" if layout == 'wide' else "cont_quest,cont_top,cont_mc,cont_left"
		multiple_limit = "0"
	elif type == 'matching_text' or type == 'rank_sequence':
		cont_category = "left_container,matching_container"
		content_id = "cont_left,cont_match"
		multiple_limit = "6"
	elif type == 'shortanswer_text':
		cont_category = "top_container,shortanswer_container"
		content_id = "cont_top,cont_sa"
		multiple_limit = "9"

	stem_attrib = {
		'visible' : "true",
		'id' : "ti",
		'tagName' : "text_item",
		'category' : "stem",
		'label' : "stem",
		'contCategory' : cont_category,
		'contID' : content_id,
		'allowMultiple' : "false",
		'allowMultiplesLimit' : multiple_limit,
		'component_id' : "ti_01",
		'min' : "1",
	}

	if type == 'shortanswer_text': 
		stem_attrib['x']='0'
		stem_attrib['y']='0'

	return stem_attrib

def get_style(type):
	font = "Monospaced" if type=='code' else "Helvetica"
	attrib_style = {
		'textItem.font.family':font,
		'textItem.font.size':"12",
		'item.paintBackground':"true",
		'item.background.default':"false",
		'item.background.color':"ffffff"
	}

	if type == 'syntax':
		attrib_style['x']='-398'
		attrib_style['y']='-216'

	return attrib_style

def serialize_duration(minutes):
	return "%.1f" % (minutes / 60.0)

def serialize_htmlText(text):
	text = text.replace('<i>', ' |i ')
	text = text.replace('<b>', ' |b ')
	text = text.replace('<u>', ' |u ')
	text = text.replace('</i>', ' |p ')
	text = text.replace('</b>', ' |p ')
	text = text.replace('</u>', ' |p ')
	text = text.replace('<u style="font-weight: bold;">', ' |u  |b ')
	text = text.replace('<font face=\"Courier New\">', ' |f Monospaced ')
	text = text.replace('<font face=\"Arial\">', ' |f Helvetica ')
	text = text.replace('</font>', ' |p ')
	text = text.replace('<br>', ' |n ')
	text = text.replace('<div>', ' |n ')
	text = text.replace('</div>', '')
	text = text.replace('&nbsp;', ' ')
	return text