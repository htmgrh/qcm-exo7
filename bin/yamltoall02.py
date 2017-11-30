#!/usr/bin/env python3

# Convert a yaml file to LaTeX file
# Usage : 'python3 yamltoall.py toto.yaml'
# Output : create a file toto.tex
# Other format 'python3 yamltoall -f amc toto.yaml' to convert it to 'amc' format


import argparse
import yaml
import sys
import os
import string
import random
import re
import html
import base64


#--------------------------------------------------
#--------------------------------------------------
# Arguments 

parser = argparse.ArgumentParser(description='Conversion of mutliple choice questions from yaml to other format (LaTeX by default).')
parser.add_argument('-f', '--format', nargs='?', default='tex', help='output format file')
parser.add_argument('inputfile', help='input yaml filename')
parser.add_argument('outputfile', nargs='?', help='output filename')

options = parser.parse_args()

#print(options.inputfile)
#print(options.outputfile)
#print(options.format)

yaml_file = options.inputfile
output = options.outputfile
output_format = options.format


# OLD Get argument : a yaml file
#yaml_file = sys.argv[1]

 
#--------------------------------------------------
#--------------------------------------------------
# Input file / output file

# Input file name
file_name, file_extension = os.path.splitext(yaml_file) 

# Output file name 
if output:
    output_file = output    # Name given by user
else:
    if output_format == 'tex':
        output_file = file_name+'.tex' # Convert to .tex extension
    if output_format == 'amc':
        output_file = file_name+'.amc' # Convert to .amc extension
    if output_format == 'moodle':  
        output_file =  file_name+'.moodle' # Convert to a xml file with a.moodle extension
    if output_format == 'f2s':
        output_file =  file_name # Convert to a xml file with a quiz extension, but inside the "file_name" directory !

# Read all data
stream = open(yaml_file, 'r', encoding='utf-8')
my_data = yaml.load_all(stream)
all_data = list(my_data)



#--------------------------------------------------
#--------------------------------------------------
# Screen output
#for data in all_data:
#    print(data['question'])
#    for answers in data['answers']:
#        print(answers['value'])
#        correct = answers['correct']
#        if correct == True:
#             print("It's true\n")
#        else:    
#             print("It's false\n")  
 
 
#--------------------------------------------------
#--------------------------------------------------
#                   TEX
# Write data to a LaTeX file in our standardized format 
if output_format == 'tex':
  with open(output_file, 'w', encoding='utf-8') as out:
    for data in all_data:
        if 'title' in data.keys():
            out.write('\n\n\\begin{question}['+data['title']+']\n')
        else:
            out.write('\n\n\\begin{question}\n')

        if 'id' in data.keys():
            out.write('\qid{'+str(data['id'])+'}\n')

        if 'author' in data.keys():
            out.write('\qauthor{'+data['author']+'}\n')

        if 'classification' in data.keys():
            out.write('\qclassification{'+data['classification']+'}\n')

        if 'tags' in data.keys():
            out.write('\qtags{'+data['tags']+'}\n')

        if 'type' in data.keys():
            out.write('\qtype{'+data['type']+'}\n')

        if 'keeporder' in data.keys():
            if data['keeporder']:
                out.write('\qkeeporder\n')

        if 'oneline' in data.keys():
            if data['oneline']:
                out.write('\qoneline\n')

        if 'idontknow' in data.keys():
            if data['idontknow']:
                out.write('\qidontknow\n')


        out.write('\n'+data['question']+'\n')

        # if 'image' in data.keys():
        #     dataimage = data['image'][0] 
        #     #print(dataimage)
        #     if 'options' in dataimage.keys():
        #         out.write('\\qimage['+dataimage['options']+']{'+dataimage['file']+'}\n\n')
        #     else:
        #         out.write('\\qimage{'+dataimage['file']+'}\n\n')     


        out.write('\\begin{answers}\n')    

        for answer in data['answers']:
            value = answer['value']
            value = value.rstrip()  #re.sub('[\s]*$','',text,flags=re.MULTILINE) # Delete potential space at the end
            correct = answer['correct']

            if 'feedback' in answer:
                feedback = answer['feedback']
                feedback = feedback.rstrip()
                value = value + '\n    \\feedback{' + feedback + '}\n    '

            if correct == True:
                out.write('    \\good{'+value+'}\n')
            else:    
                out.write('    \\bad{'+value+'}\n')

     
        out.write('\\end{answers}\n') 

        if 'explanations' in data.keys():
            out.write('\\begin{explanations}\n'+data['explanations']+'\\end{explanations}\n')

        out.write('\\end{question}\n')

#--------------------------------------------------
#--------------------------------------------------
# Replace custom LaTeX macro for non-LaTeX export
def replace_latex_macros(text):

    # Replace \Rr to \mathbf{R} ...
    text = re.sub("\\\\Nn(?=[^a-zA-Z])","\mathbf{N}",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("\\\\Zz(?=[^a-zA-Z])","\mathbf{Z}",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("\\\\Qq(?=[^a-zA-Z])","\mathbf{Q}",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("\\\\Rr(?=[^a-zA-Z])","\mathbf{R}",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("\\\\Cc(?=[^a-zA-Z])","\mathbf{C}",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("\\\\Kk(?=[^a-zA-Z])","\mathbf{K}",text, flags=re.MULTILINE|re.DOTALL)

    # Replace '<' (resp. '>'') by ' < ' (resp. ' > ') to avoid html mixed up (note the spaces)
    text = re.sub("<"," < ",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub(">"," > ",text, flags=re.MULTILINE|re.DOTALL)

    return text

# Test
# text = "Soit $f : \\Nn \\to \\Rr$ et $b<a$ \\Nnon et $\\Nn7$"
# print(text)
# text = replace_latex_macros(text)
# print(text)

# Delete the code from the section title 
# Example "My Section | Easy | 123.45" -> "My Section | Easy"
def delete_exo7_category(text):
    text = re.sub("\s\|\s[0-9.,\s]+","",text, flags=re.MULTILINE|re.DOTALL)

    return text

# Test
# text = "Logique | Facile | 100.01, 100.02"
# print(text)
# text = delete_exo7_category(text)
# print(text)

# text = "Logique -- Raisonnement | 100"
# print(text)
# text = delete_exo7_category(text)
# print(text)



#--------------------------------------------------
#--------------------------------------------------
# Random word generator (from stackoverflow)
def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


#--------------------------------------------------
#--------------------------------------------------
#                      AMC
# Write data to a LaTeX file in the format 'amc'
if output_format == 'amc':
  with open(output_file, 'w', encoding='utf-8') as out:
    for data in all_data:
        
        if 'id' in data.keys():
            myid = str(data['id'])
        else:
            myid = id_generator()

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            out.write('\n\n\\begin{question}{'+myid+'}\n\n')
        else:
            out.write('\n\n\\begin{questionmult}{'+myid+'}\n\n')

        if 'author' in data.keys():
            out.write('%Author: '+data['author']+'\n\n')

        if 'classification' in data.keys():
            out.write('%Classification: '+data['classification']+'\n\n')

        if 'tags' in data.keys():
            out.write('%\\tags{'+data['tags']+'.}\n\n')

        if 'title' in data.keys():
            thetitle = replace_latex_macros(data['title'])
            out.write('\\textbf{'+ thetitle +'.} ')

        thequestion = replace_latex_macros(data['question'])
        thequestion = re.sub("\\\\qimage","\includegraphics",thequestion, flags=re.MULTILINE|re.DOTALL)
        out.write(thequestion+'\n')



        # if 'image' in data.keys():
        #     dataimage = data['image'][0] 
        #     out.write('\\begin{center}\n')
        #     if 'options' in dataimage.keys():
        #         out.write('\\includegraphics['+dataimage['options']+']{'+dataimage['file']+'}')
        #     else:
        #         out.write('\\includegraphics{'+dataimage['file']+'}')     
        #     out.write('\n\\end{center}\n\n')

        if 'oneline' in data.keys() and data['oneline']:
            out.write('\\begin{choiceshoriz}')
        else:
            out.write('\\begin{choices}')

        if 'keeporder' in data.keys() and data['keeporder']:
            out.write('[o]\n')
        else:
            out.write('\n')  

        for answers in data['answers']:
            value = answers['value']
            value = replace_latex_macros(value.rstrip())  #re.sub('[\s]*$','',text,flags=re.MULTILINE) # Delete potential space at the end
            value = re.sub("\\\\qimage","\includegraphics",value, flags=re.MULTILINE|re.DOTALL)

            correct = answers['correct']

            if correct == True:
                out.write('    \\correctchoice{'+value+'}\n')
            else:    
                out.write('    \\wrongchoice{'+value+'}\n')

        if 'oneline' in data.keys() and data['oneline']:
            out.write('\\end{choiceshoriz}\n')
        else:
            out.write('\\end{choices}\n')     

        if 'explanations' in data.keys():
            theexplanations = replace_latex_macros(data['explanations'])
            theexplanations = re.sub("\\\\qimage","\includegraphics",theexplanations, flags=re.MULTILINE|re.DOTALL)

            out.write('\explain{'+ theexplanations +'}\n')

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            out.write('\\end{question}\n')
        else:
            out.write('\\end{questionmult}\n')


 
#--------------------------------------------------
#--------------------------------------------------
#                   MOODLE
# Write data to a xml file in a moodle format 

# Encode an image to be included in xml
def encode_image(filename):
    filename =  filename + '.png'
    with open(filename, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('ascii')
    data = '</p><p>\n<img src="data:image/png;base64,'+encoded+'"/>\n'
    return data

# Replace all input of images by their encoding
def replace_images(data):

    # the image without options : idem
    theimage = re.search('\\\\qimage',data, flags=re.MULTILINE|re.DOTALL)

    while theimage is not None:
        # the image without options
        theimage = re.search('(?<=\\\\qimage\{)(.*?)(?=\})',data, flags=re.MULTILINE|re.DOTALL)
        if theimage:
            image_name = theimage.group(0)
            # print("sans option",image_name)
            new_image = encode_image(image_name)
            data = re.sub("\\\\qimage\{(.*?)\}",new_image,data, flags=re.MULTILINE|re.DOTALL)
        else:
        # the image with options
            theimage = re.search('(?<=\\\\qimage\[)(.*?)(?=\]\{)(.*?)(?=\})',data, flags=re.MULTILINE|re.DOTALL)
            image_name = theimage.group(2)[2:]
            image_options = theimage.group(1)
            # print("avec option",image_name,image_options)
            new_image = encode_image(image_name)
            data = re.sub("\\\\qimage\[(.*?)\]\{(.*?)\}",new_image,data, flags=re.MULTILINE|re.DOTALL)

        # Next image?
        theimage = re.search('\\\\qimage',data, flags=re.MULTILINE|re.DOTALL)

    return data

    



beginmoodle = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
endmoodle = '\n\n</quiz>\n'

if output_format == 'moodle':
  with open(output_file, 'w', encoding='utf-8') as out:

    out.write(beginmoodle)

    for data in all_data:

        if 'section' in data.keys():
            thesection = delete_exo7_category(data['section'])

            if 'subsection' in data.keys():           
                thesubsection = '/' + delete_exo7_category(data['subsection'])
            else:
                thesubsection = ''

            course_name = 'Défaut pour LISCINUM2017/'

            out.write('\n\n<question type="category">\n<category>\n<text>\n$course$/'+course_name
                +thesection+thesubsection+'</text>\n</category>\n</question>\n\n')

#        if 'id' in data.keys():
#            myid = str(data['id'])

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            out.write('\n\n<question type="multichoice">\n')
        else:
            out.write('\n\n<question type="multichoice">\n')


        if 'num' in data.keys():
            thenum = 'qcm-exo7-'+str(data['num']).zfill(4)
            out.write('<name><text>'+ thenum +'</text></name>\n')
        else: 
            out.write('<name><text> </text></name>\n')

        # question
        thequestion = replace_latex_macros(data['question'])
        thequestion = replace_images(thequestion)
        out.write('<questiontext format="html">\n')
        out.write('<text><![CDATA[<p>\n')
        out.write(thequestion)
        
        # #image in the question
        # if 'image' in data.keys():
        #     dataimage = data['image'][0]
        #     image_file =  dataimage['file']+'.png'
        #     with open(image_file, "rb") as image_file:
        #         encoded = base64.b64encode(image_file.read()).decode('ascii')
        #     #print(encoded)
        #     out.write('</p><p>\n<img src="data:image/png;base64,')            
        #     out.write(encoded)
        #     out.write('"/>\n')

        # end of the question
        out.write('</p>]]></text>\n')
        out.write('</questiontext>\n<defaultgrade>1.0</defaultgrade>\n')

        if 'explanations' in data.keys():
            theexplanations = replace_latex_macros(data['explanations'])
            theexplanations = replace_images(theexplanations)
            out.write('<generalfeedback format="html"><text><![CDATA[<p>\n')
            out.write(theexplanations)
            out.write('</p>]]></text></generalfeedback>\n')

        if 'keeporder' in data.keys() and data['keeporder']:
            out.write('<shuffleanswers>0</shuffleanswers>\n')
        else:
            out.write('<shuffleanswers>1</shuffleanswers>\n') 

        out.write('<answernumbering>abc</answernumbering>\n')



        nbans = 0
        nbgood = 0
        nbbad = 0
        for answers in data['answers']:
            correct = answers['correct']
            nbans += 1
            if correct:
                nbgood += 1
            else:
                nbbad += 1

        if nbgood > 0:
            goodratio = str("%.5f" % float(100/nbgood))
        else: 
            goodratio = "0"
        if nbbad > 0: 
            badratio = str("%.5f" % float(100/nbbad))
        else:
            badratio = "0"

        for answer in data['answers']:
            if answer['correct']:
                out.write('<answer fraction="'+goodratio+'" format="html"><text><![CDATA[<p>\n')
            else:
                out.write('<answer fraction="-'+badratio+'" format="html"><text><![CDATA[<p>\n')
            thevalue = replace_latex_macros(answer['value'])
            thevalue = replace_images(thevalue)

            out.write(thevalue)
            out.write('</p>]]></text>\n')

            if 'feedback' in answer:
                feedback = replace_latex_macros(answer['feedback'])
                feedback = replace_images(feedback)
                feedback = feedback.rstrip()
                out.write('<feedback><text><![CDATA[<p>' + feedback + '</p>]]></text></feedback>\n')
            
            out.write('</answer>\n')


#            value = 
#            value = value.rstrip()  #re.sub('[\s]*$','',text,re.MULTILINE) # Delete potential space at the end
#            correct = 
#              correct == True:
#                out.write('    \\correctchoice{'+value+'}\n')
#            else:    
#                out.write('    \\wrongchoice{'+value+'}\n')
        out.write('<single>false</single>\n')  
        out.write('</question>')

    out.write(endmoodle)


#--------------------------------------------------
#--------------------------------------------------
#                 FAQ2SCIENCES (f2s)
# Write data to a xml file in a Scenari / faq2sciences format


def f2sxmlcleanup(data):
    data = html.escape(data)
    data = re.sub('\$(.*?)\$', '<sc:textLeaf role="mathtex">\\1</sc:textLeaf>', data)
    data = re.sub('\\\\\[(.*?)\\\\\]', '<sc:textLeaf role="mathtex">\\1</sc:textLeaf>', data)
    data = re.sub('\\\\\((.*?)\\\\\)', '<sc:textLeaf role="mathtex">\\1</sc:textLeaf>', data)
    data = re.sub('\\\\textbf\{(.*?)\}', '<sc:inlineStyle role="emp">\\1</sc:inlineStyle>', data)
    return data

beginf2s = '<?xml version="1.0" encoding="UTF-8"?>\n<sc:item xmlns:sc="http://www.utc.fr/ics/scenari/v3/core">\n'
endf2s = '\n</sc:item>\n'

if output_format == 'f2s':
    os.mkdir(output_file)

    for data in all_data:
        if 'id' in data.keys():
            file_id = str(data['id'])
        else:
            file_id = id_generator()
        out = open(os.path.join(output_file, file_id+'.quiz'), 'w', encoding='utf-8')
        out.write(beginf2s)

        single = False

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            single = True
            out.write('\n\n<op:mcqSur xmlns:op="utc.fr:ics/opale3" xmlns:sp="http://www.utc.fr/ics/scenari/v3/primitive">\n')
        else:
            out.write('\n\n<op:mcqMur xmlns:op="utc.fr:ics/opale3" xmlns:sp="http://www.utc.fr/ics/scenari/v3/primitive">\n')

        if 'title' in data.keys():
            thetitle = replace_latex_macros(data['title'])
            out.write('<op:exeM><sp:title>'+ thetitle +'</sp:title></op:exeM>\n')
        else: 
            out.write('<op:exeM></op:exeM>\n')

        thequestion = replace_latex_macros(data['question'])
        out.write('<sc:question><op:res><sp:txt><op:txt><sc:para xml:space="preserve">\n')
        out.write(f2sxmlcleanup(thequestion))
        out.write('</sc:para></op:txt></sp:txt></op:res></sc:question>\n')


#        if 'image' in data.keys():
#            dataimage = data['image'][0] 
#            out.write('\\begin{center}\n')
#            if 'options' in dataimage.keys():
#                out.write('\\includegraphics['+dataimage['options']+']{'+dataimage['file']+'}')
#            else:
#                out.write('\\includegraphics{'+dataimage['file']+'}')     
#            out.write('\n\\end{center}\n\n')

        good = 1
        out.write('<sc:choices>\n')
        for answer in data['answers']:

            checkstate = ''
            if not (single):
                if answer['correct']:
                    checkstate = ' solution="checked"'
                else:
                    checkstate = ' solution="unchecked"'
            out.write('<sc:choice'+checkstate+'><sc:choiceLabel><op:txt><sc:para xml:space="preserve">\n')
            thevalue = replace_latex_macros(answer['value'])
            out.write(f2sxmlcleanup(thevalue))
            out.write('</sc:para></op:txt></sc:choiceLabel>')

            if 'feedback' in answer:
                feedback = replace_latex_macros(answer['feedback'])
                feedback = f2sxmlcleanup(feedback)
                feedback = feedback.rstrip()
                out.write('<sc:choiceExplanation><op:txt><sc:para xml:space="preserve">\n' + feedback +'</sc:para></op:txt></sc:choiceExplanation>\n')

            out.write('</sc:choice>\n')
            good+=1

        out.write('</sc:choices>')
        if single:
            out.write('<sc:solution choice="'+str(good)+'"/>')
        if 'explanations' in data.keys():
            theexplanations = replace_latex_macros(data['explanations'])
            out.write('<sc:globalExplanation><op:res><sp:txt><op:txt><sc:para xml:space="preserve">\n')
            out.write(f2sxmlcleanup(theexplanations))
            out.write('</sc:para></op:txt></sp:txt></op:res></sc:globalExplanation>\n')

        if single:
            out.write('\n\n</op:mcqSur>\n')
        else:
            out.write('\n\n</op:mcqMur>\n')

        out.write(endf2s)
