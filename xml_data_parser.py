#-*-coding:utf-8-*-
"""
Created on Sat Feb 24 2018
@author: Li, Supeng

Tokenize the text data in xml and transform into BOI format
"""

from xml.etree import cElementTree

def xml_data_parser(input_file_name, split_character_set):

    # read the train data, the data is in a xml format
    raw_doc = cElementTree.ElementTree(file=input_file_name)

    # get the root element, all sentences
    sentences = raw_doc.getroot()

    # output will be written in a outside file
    outfile = open(input_file_name.split('.')[0] + '.txt', 'w')

    # iterate all sentences
    for sentence in sentences:
        # list to store position information
        from_to = []

        # iterate all elements within a sentence
        for element in sentence:
            # get all characters within text
            if element.tag == 'text':
                text_character = list(element.text.lower().replace('-', ' '))

            # get the index of all aspect terms
            if element.tag == 'aspectTerms':
                for aspect_term in element:
                    from_to.append([int(aspect_term.attrib['from']), int(aspect_term.attrib['to'])])


        # initialize position information
        is_target = [False] * len(text_character)
        # update position information
        for item in from_to:
            is_target[item[0]:item[1]] = [True] * (item[1] - item[0])

        # buffer used when tokenize
        character_buffer = ''
        # flag indicate whether last space within an aspect term
        is_last_space_inside = False
        for i in range(len(text_character)):

            # throw away space
            if text_character[i] != ' ':
                character_buffer += text_character[i]

                # append character buffer to word list when current character is the at the end of the sentence
                if i == len(text_character) - 1:
                    outfile.write(character_buffer + '\t')
                    character_buffer = ''
                    if is_target[i]:
                        if is_last_space_inside:
                            outfile.write('I\n')
                        else:
                            outfile.write('B\n')
                    else:
                        outfile.write('O\n')

                # not append only when both current character and next character not in the given character set
                elif not ((text_character[i] not in split_character_set) and (text_character[i+1] not in split_character_set)):
                    outfile.write(character_buffer + '\t')
                    character_buffer = ''
                    if is_target[i]:
                        if is_last_space_inside:
                            outfile.write('I\n')
                        else:
                            outfile.write('B\n')
                    else:
                        outfile.write('O\n')
                # if current character and next character not in the given character set
                else:
                    pass

            # update information for space
            if text_character[i] == ' ':
                is_last_space_inside = is_target[i]
        # use '\n' to indicate the end of sentence
        outfile.write('\n')
    outfile.close()
