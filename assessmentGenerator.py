import xml.etree.ElementTree as ET

import os
import tempfile

import __main__ as main

def set_assessment(args):
	location = args['location']
	assessment_type = args['assessment']['type']
	if assessment_type == 'mamc':
	    tree = get_mamc(args)
	elif assessment_type == 'matching_text':
	    tree = get_matching_text(args)
	elif assessment_type == 'rank_sequence':
	    tree = get_rank_sequence(args)
	elif assessment_type == 'shortanswer_text':
	    tree = get_shortanswer_text(args)

	temp = tempfile.NamedTemporaryFile(mode='w+b', dir=location, delete=False)
	
	tree.write(temp, encoding="UTF-8")
	temp.close()

	filename = location + 'p%d' %main.p_counter 

	os.rename(temp.name, '%s.xml' %filename)

def get_assessment_element(assessment, topic_id, audio_number):
	assessment_type = assessment['type']
	if assessment_type == 'mamc':
	    pageElement = get_mamc_element(assessment, topic_id, audio_number, assessment_type)
	elif assessment_type == 'matching_text':
	    pageElement = get_matching_text_element(assessment, topic_id, audio_number, assessment_type)
	elif assessment_type == 'rank_sequence':
	    pageElement = get_rank_sequencet_element(assessment, topic_id, audio_number, assessment_type)
	elif assessment_type == 'shortanswer_text':
	     pageElement = get_shortanswer_text_element(assessment, topic_id, audio_number, assessment_type)

	return pageElement

def get_mamc(args):
	base = (os.getcwd() + '/data/xml/base_question_mamc.xml')
	tree = ET.parse(base)
	tree_root = tree.getroot()
	assessment = args['assessment']
	layout = assessment['layout']

	tree_root.attrib['id'] = 'P%d' %main.p_counter
	tree_root.attrib['templateFileName'] = 'multiple_choice_wide.xml' if layout == 'wide' else 'multiple_choice_standard.xml'
	tree_root.find('text_item').find('value').text = main.help.serialize_htmlText(assessment['text'])
	tree_root.find('style').attrib['category'] = 'widePageStyle' if layout == 'wide' else 'standard'

	stemBehaviorElement = ET.Element('behavior', {'id' : "playAudio", 'target' :"audioi_01"})

	tree_root.find('text_item').append(stemBehaviorElement)

	audioElement = ET.Element('audio_item', main.help.get_audio_attrib(args['topic_id'], args['audio_number'], 'question'))

	tree_root.append(audioElement)	

	q_counter = 1
	for option in assessment['options']:
		q_id = 'ansi_0%d' %q_counter

		answerElement = main.help.get_answer_mamc(q_id, 'answer_item', layout, option)

		answerText = ET.Element('value')
		answerText.text = main.help.serialize_htmlText(option['text'])

		answerElement.append(answerText)

		tree_root.append(answerElement)
		q_counter += 1

	return tree

def get_matching_text(args):
	base = (os.getcwd() + '/data/xml/base_question_match_text.xml')
	tree = ET.parse(base)
	tree_root = tree.getroot()
	assessment = args['assessment']

	tree_root.attrib['id'] = 'P%d' %main.p_counter
	tree_root.find('text_item').find('value').text = main.help.serialize_htmlText(assessment['text'])

	stemBehaviorElement = ET.Element('behavior', {'id' : "playAudio", 'target' :"audioi_01"})

	tree_root.find('text_item').append(stemBehaviorElement)

	audioElement = ET.Element('audio_item', main.help.get_audio_attrib(args['topic_id'], args['audio_number'], 'question'))

	tree_root.append(audioElement)	

	q_counter = 1
	for option in assessment['options']:
		q_id = 'moi_0%d' %q_counter

		textElement = ET.Element('text_item', {'id':'moi', 'component_id':q_id, 'visible':'true'})

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(option['text'])

		textElement.append(valueText)

		tree_root.append(textElement)
		q_counter += 1

	q_counter = 1
	for target in assessment['targets']:
		q_id = 'ansi_0%d' %q_counter
		correct = 'moi_0%d' %target['option']

		answerElement = ET.Element('answer_item', {'id':'ansi', 'component_id':q_id, 'visible':'true', 'isCorrect':correct})

		answerText = ET.Element('value')
		answerText.text = main.help.serialize_htmlText(target['text'])

		answerElement.append(answerText)

		tree_root.append(answerElement)
		q_counter += 1

	return tree

def get_rank_sequence(args):
	base = (os.getcwd() + '/data/xml/base_question_rank_seq.xml')
	tree = ET.parse(base)
	tree_root = tree.getroot()
	assessment = args['assessment']

	tree_root.attrib['id'] = 'P%d' %main.p_counter
	tree_root.find('text_item').find('value').text = main.help.serialize_htmlText(assessment['text'])

	stemBehaviorElement = ET.Element('behavior', {'id' : "playAudio", 'target' :"audioi_01"})

	tree_root.find('text_item').append(stemBehaviorElement)

	audioElement = ET.Element('audio_item', main.help.get_audio_attrib(args['topic_id'], args['audio_number'], 'question'))

	tree_root.append(audioElement)	

	q_counter = 1
	for option in assessment['options']:
		q_id = 'ansi_0%d' %q_counter
		correct = 'moi_0%d' %q_counter

		answerElement = ET.Element('answer_item', {'id':'ansi', 'component_id':q_id, 'visible':'true', 'isCorrect':correct})
		tree_root.append(answerElement)

		textElement = ET.Element('text_item', {'id':'moi', 'component_id':q_id, 'visible':'true'})

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(option['text'])

		textElement.append(valueText)

		tree_root.append(textElement)
		q_counter += 1

	return tree

def get_shortanswer_text(args):
	base = (os.getcwd() + '/data/xml/base_question_short_answer_text.xml')
	tree = ET.parse(base)
	tree_root = tree.getroot()
	assessment = args['assessment']

	tree_root.attrib['id'] = 'P%d' %main.p_counter
	tree_root.find('text_item').find('value').text = main.help.serialize_htmlText(assessment['text'])

	stemBehaviorElement = ET.Element('behavior', {'id' : "playAudio", 'target' :"audioi_01"})

	tree_root.find('text_item').append(stemBehaviorElement)

	audioElement = ET.Element('audio_item', main.help.get_audio_attrib(args['topic_id'], args['audio_number'], 'question'))
	tree_root.append(audioElement)	

	inputElement = ET.Element('text_input_item', {'id':"codetii", 'component_id':"codetii_01", 'mneumonic_id':""})
	tree_root.append(inputElement)	

	q_counter = 1
	for option in assessment['options']:
		q_id = 'ansi_0%d' %q_counter
		correct = 'true' if option['correct'] == True else 'false'

		answerElement = ET.Element('answer_item', {'id':'ansi', 'component_id':q_id, 'visible':'true', 'isCorrect':correct})

		if q_counter == 1 : answerElement.attrib['preferred_answer'] = "true"

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(option['text'])

		answerElement.append(valueText)

		tree_root.append(answerElement)
		q_counter += 1

	codeElement = ET.Element('text_item', {'id':'codeti', 'component_id':'codeti_02', 'visible':'true', 'codeGrows':'false'})
	codeValue = ET.Element('value')
	codeValue.text = " |s 12 %s |p " %main.help.serialize_htmlText(assessment['code'])
	codeStyle = ET.Element('style', main.help.get_style('code'))
	codeElement.append(codeValue)
	codeElement.append(codeStyle)
	tree_root.append(codeElement)

	syntaxElement = ET.Element('text_item', {'id':'syntaxti', 'component_id':'syntaxti_01', 'visible':'true'})
	syntaxValue = ET.Element('value')
	syntaxValue.text = " |s 12 %s |p " %main.help.serialize_htmlText(assessment['syntax'])
	syntaxAttrib = {
		'x':"0",
		'y':"0",
		'textItem.font.family':"Helvetica",
		'textItem.font.size':"12",
		'item.paintBackground':"true",
		'item.background.default':"false",
		'item.background.color':"ffffff"
	}
	syntaxStyle = ET.Element('style', main.help.get_style('syntax'))
	syntaxElement.append(syntaxValue)
	syntaxElement.append(syntaxStyle)
	tree_root.append(syntaxElement)

	return tree


def get_mamc_element(assessment, topic_id, audio_number, type):
	layout = assessment['layout']
	id = "P%d" %main.p_counter
	style = 'Multiple Choice Wide' if layout == 'wide' else 'Multiple Choice Standard'
	name = "%s - %s" %(id,style)

	stemElement = ET.Element('StemModelItem', main.help.get_stemp_attrib(type, layout))

	stempText = ET.Element('value')
	stempText.text = main.help.serialize_htmlText(assessment['text'])
	stemElement.append(stempText)

	stemBehaviorItem = ET.Element('BehaviorItem', {'id' : "playAudio", 'target' :"audioi_01"})
	stemElement.append(stemBehaviorItem)
	
	pageElement = ET.Element('PageItem', main.help.get_page_attrib(name, id, type, layout))
	pageElement.append(stemElement)

	audioElement = ET.Element('AudioModelItem', main.help.get_audio_attrib(topic_id, audio_number, 'editor'))
	pageElement.append(audioElement)


	q_counter = 1
	for option in assessment['options']:
		q_id = 'ansi_0%d' %q_counter

		answerElement = main.help.get_answer_mamc(q_id, 'AnswerModelItem', layout, option)

		answerText = ET.Element('value')
		answerText.text = main.help.serialize_htmlText(option['text'])
		answerElement.append(answerText)

		pageElement.append(answerElement)

		q_counter += 1

	return pageElement

def get_matching_text_element(assessment, topic_id, audio_number, type):
	id = "P%d" %main.p_counter
	name = "%s - Matching Standard Text" %id

	stemElement = ET.Element('StemModelItem', main.help.get_stemp_attrib(type))

	stempText = ET.Element('value')
	stempText.text = main.help.serialize_htmlText(assessment['text'])
	stemElement.append(stempText)

	stemBehaviorItem = ET.Element('BehaviorItem', {'id' : "playAudio", 'target' :"audioi_01"})
	stemElement.append(stemBehaviorItem)
	
	pageElement = ET.Element('PageItem', main.help.get_page_attrib(name, id, type))
	pageElement.append(stemElement)

	audioElement = ET.Element('AudioModelItem', main.help.get_audio_attrib(topic_id, audio_number, 'editor'))
	pageElement.append(audioElement)

	q_counter = 1
	for option in assessment['options']:
		q_id = 'moi_0%d' %q_counter

		option_opt_attrib = {
			'visible': "true",
			'id': "moi",
			'tagName': "text_item",
			'category': "option_matching",
			'contCategory': "option_container,right_container,matching_container",
			'contID' : "cont_opt,cont_right,cont_match",
			'allowMultiple': "true",
			'allowMultiplesLimit': "6",
			'component_id': q_id,
			'min': "2"
		}
		
		matchElement = ET.Element('MatchingOptionModelItem', option_opt_attrib)

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(option['text'])

		matchElement.append(valueText)

		pageElement.append(matchElement)
		q_counter += 1

	q_counter = 1
	for target in assessment['targets']:
		val = main.help.get_match_letter(target['option'])
		q_id = 'ansi_0%d' %q_counter
		correct = '%s,moi_0%d' %(val,target['option'])

		target_opt_attrib = {
			'visible': "true",
			'id': "ansi",
			'tagName': "answer_item",
			'category': "matchingText",
			'contCategory': "answer_container,right_container,matching_container",
			'contID' : "cont_ans,cont_right,cont_match",
			'allowMultiple': "true",
			'allowMultiplesLimit': "6",
			'component_id': q_id,
			'min': "2",
			'match1' : correct,
			'match2' : '',
			'match3' : '',
		}
		
		targetElement = ET.Element('MatchingTargetModelItem', target_opt_attrib)

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(target['text'])

		targetElement.append(valueText)

		pageElement.append(targetElement)
		q_counter += 1

	return pageElement

def get_rank_sequencet_element(assessment, topic_id, audio_number, type):
	id = "P%d" %main.p_counter
	name = "%s - Rank/Sequence" %id

	stemElement = ET.Element('StemModelItem', main.help.get_stemp_attrib(type))

	stempText = ET.Element('value')
	stempText.text = main.help.serialize_htmlText(assessment['text'])
	stemElement.append(stempText)

	stemBehaviorItem = ET.Element('BehaviorItem', {'id' : "playAudio", 'target' :"audioi_01"})
	stemElement.append(stemBehaviorItem)
	
	pageElement = ET.Element('PageItem', main.help.get_page_attrib(name, id, type))
	pageElement.append(stemElement)

	audioElement = ET.Element('AudioModelItem', main.help.get_audio_attrib(topic_id, audio_number, 'editor'))
	pageElement.append(audioElement)

	q_counter = 1
	for option in assessment['options']:
		q_id = 'ansi_0%d' %q_counter
		sequence = '%s' %q_counter
		alt_text = option['alt']
		rank_opt_attrib = {
			'visible': "true",
			'id': "ansi",
			'tagName': "answer_item",
			'category': "matchingText",
			'contCategory': "answer_container,right_container,matching_container",
			'contID' : "cont_ans,cont_right,cont_match",
			'allowMultiple': "true",
			'allowMultiplesLimit': "6",
			'component_id': q_id,
			'min': "2",
			'sequence': sequence,
			'altText': alt_text,
		}
		
		rankElement = ET.Element('RankingModelItem', rank_opt_attrib)

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(option['text'])

		rankElement.append(valueText)

		pageElement.append(rankElement)
		q_counter += 1

	return pageElement

def get_shortanswer_text_element(assessment, topic_id, audio_number, type):
	id = "P%d" %main.p_counter
	name = "%s - Short Answer Tex" %id

	stemElement = ET.Element('StemModelItem', main.help.get_stemp_attrib(type))

	stempText = ET.Element('value')
	stempText.text = main.help.serialize_htmlText(assessment['text'])
	stemElement.append(stempText)

	audioBehaviorItem = ET.Element('BehaviorItem', {'id' : "playAudio", 'target' :"audioi_01"})
	codeBehaviorItem = ET.Element('BehaviorItem', {'id' : "showCode", 'target' :"codeti_02"})
	syntaxBehaviorItem = ET.Element('BehaviorItem', {'id' : "showSyntax", 'target' :"syntaxti_01"})
	stemElement.append(audioBehaviorItem)
	stemElement.append(codeBehaviorItem)
	stemElement.append(syntaxBehaviorItem)
	
	pageElement = ET.Element('PageItem', main.help.get_page_attrib(name, id, type))
	pageElement.append(stemElement)

	audioElement = ET.Element('AudioModelItem', main.help.get_audio_attrib(topic_id, audio_number, 'editor'))
	inputElement = ET.Element('TextInputModelItem', main.help.get_input_attrib())
	pageElement.append(audioElement)
	pageElement.append(inputElement)

	q_counter = 1
	for option in assessment['options']:
		q_id = 'ansi_0%d' %q_counter
		correct = 'true' if option['correct'] == True else 'false'

		short_answer_attrib = {
			'visible':"false",
			'isCorrect':correct,
			'id':"ansi",
			'tagName':"answer_item",
			'category':"short_answer",
			'contCategory':"answer2_container,answer2_container,top_container,shortanswer_container",
			'contID':"cont_an4,cont_an3,cont_top,cont_sa",
			'allowMultiple':"true",
			'allowMultiplesLimit':"9",
			'component_id':q_id,
			'min':"1"
		}
		
		shortAnswerElement = ET.Element('ShortAnswerModelItem', short_answer_attrib)

		valueText = ET.Element('value')
		valueText.text = main.help.serialize_htmlText(option['text'])

		shortAnswerElement.append(valueText)

		pageElement.append(shortAnswerElement)
		q_counter += 1


	codeAttrib = { 
		'visible':"true",
		'enabled':"true",
		'selected':"true",
		'active':"true",
		'id':"codeti",
		'tagName':"text_item",
		'category':"code",
		'contCategory':"",
		'contID':"",
		'allowMultiple':"true",
		'allowMultiplesLimit':"9",
		'component_id':"codeti_02",
		'backgroundMode':"White",
		'fontName':"Monospaced",
		'fontSize':"12",
		'codeGrows':"false"
	}
	codeElement = ET.Element('CodeModelItem', codeAttrib)
	codeValue = ET.Element('value')
	codeValue.text = " |s 12 %s |p " %main.help.serialize_htmlText(assessment['code'])
	codeElement.append(codeValue)
	pageElement.append(codeElement)

	syntaxAttrib = {
		'visible':"false",
		'enabled':"true",
		'selected':"false",
		'active':"true",
		'tagName':"text_item",
		'id':"syntaxti",
		'category':"syntax",
		'x':"-398",
		'y':"-216",
		'component_id':"syntaxti_01",
		'backgroundMode':"White",
		'fontName':"Helvetica",
		'fontSize':"12"
	}
	syntaxElement = ET.Element('SyntaxModelItem', syntaxAttrib)
	syntaxValue = ET.Element('value')
	syntaxValue.text = " |s 12 %s |p " %main.help.serialize_htmlText(assessment['syntax'])
	syntaxElement.append(syntaxValue)
	pageElement.append(syntaxElement)

	return pageElement