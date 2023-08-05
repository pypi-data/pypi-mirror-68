"""
Welcome to aaDoc... by Dilli Babu R < dillir07@outlook.com >
aaDoc is a program or tool if you will, can generate efficient documentation for
Automation Anywhere Code.

This file contains methods that takes input from commandline and generates
documentation for Automation Anywhere code using the comments written by the developers.
This is done by using the various tags in the comments, which makes it possible
for the aaDoc

Note: Tag names are inspired by jsDoc tags at https://jsDoc.app

"""

import os
import re
import time
import argparse
from pprint import pprint as pp
from .tags_module.tags import generate_tags_for_re
from .html_helpers_module.html_helpers import get_html_for_tag, get_base_html, get_param_table_header_html
from .stylesheet_source_module import stylesheet_source

# meta details
__author__ = "Dilli Babu R"
__copyright__ = "Copyright 2020, Dilli Babu R"
__contact__ = "dillir07@outlook.com"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "dillir07@outlook.com"
__status__ = "Development"
__date__ = "2020-05-06"

# used a global variable, as it doesn't make sense to compile regex each time in loop
tag_re = None


def process_file(file_path: str, output_folder_path:str) -> dict:
    """
    Processes given input file by reading the file data
    and then filtering the comments and calling parse_comment_line method
    for each comment. Once all comments are parsed the comment_data will be
    used to create documentation by calling write_html method.
    :param file_path: text file path which needs to be processed
    :param output_folder_path: destination to store the generated documentation output file.
    """

    tags_with_comment_values = []  # init list

    global tag_re  # global variable to avoid re-compiling regex

    with open(file_path, 'r') as txt_file:
        input_file_path_with_extension = txt_file.name
        all_data = txt_file.readlines()

    tags_re_pattern = generate_tags_for_re()  # getting the list of tags
    tag_re = re.compile(tags_re_pattern)

    comments_data = [line for line in all_data if 'Comment:' in line]

    # parsing each comment line
    for comment in comments_data:
        parsed_data_for_current_comment_line = parse_comment_line(comment)
        # adding to tags_with_comment_values if it has value
        if parsed_data_for_current_comment_line is not None:
            tags_with_comment_values.append(
                parsed_data_for_current_comment_line)
    
    # tags_with_comment_values should not be sorted because line_number based sort order won't be in correct order. 1,11,12 like that.
    # tags_with_comment_values = sorted(tags_with_comment_values, key=lambda comment_line: comment_line['line_number'])

    input_file_name = os.path.split(input_file_path_with_extension)[1].lower()
    output_file_path = output_folder_path + "\\" + input_file_name.replace(".txt", ".html")
    write_html(output_file_path, input_file_name.replace(".txt", ""), tags_with_comment_values)
    return {'file_path':file_path, 'file_name':input_file_name, 'no_of_lines':len(all_data), 'no_of_comment_lines':len(comments_data)}


def parse_comment_line(comment_line: str) -> dict:
    """
    Parses one given comment line, identifies line_number, tag and tag value example: 25 Comment: @author Dilli Babu
    R <dillir07@outlook.com> here 25 is line_number, tag is @author, value is Dilli Babu R <dillir07@outlook.com>
    these will be added to comment_data and the same is returned, if comment is empty returns None :param
    comment_line: :return: A dictionary like {'line_number': 25, 'tag': '@author', 'value': 'Dilli Babu R
    <dillir07@outlook.com>'} :raises: TypeError when given comment/input doesn't contain 'Comment:'. Every Automation
    Anywhere Comment will have 'Comment:' in it.
    """
    tags_with_values = []
    if 'Comment:' not in comment_line:
        raise TypeError('Not a comment line')
    else:
        line_number = comment_line.split('\t')[0]
        comment = comment_line.split('\t')[1]

        if '@' in comment:
            matched_tags = tag_re.findall(comment)
            for _ in range(len(matched_tags)):
                match_result = tag_re.search(comment)
                tags_with_values.append({'line_number': line_number, 'tag': match_result.group(),
                                         'value': comment[match_result.end():].strip()})
            return tags_with_values[0]  # returning first matched tag, expecting one tag per line (block level tags)


def write_html(html_file_path: str, filename: str, tags_with_comment_values: list) -> None:
    """
    Loops over the given list of dictionaries and calls appropriate methods of html_helpers.py
    and writes the received html mark up to output file using file operations.
    Output file will be over written if already present, if not new file will be created.
    :param html_file_path: output file path, should be fully qualified file path
    :param filename: filename of the output file which is same as input file name, used in html title tag
    :param tags_with_comment_values: a list of dictionaries with keys line_number, tag, value
    :return: None
    """
    working_on_param_tag = False
    written_param_count = 0
    with open(html_file_path, 'w') as html:
        html.write(get_base_html(title=filename))
        # looping over list of comments data
        for comment_data in tags_with_comment_values:
            # we are checking this conditions to group the param tags in sequence to write in same table.
            if comment_data['tag'] == '@param':
                written_param_count += 1
                if working_on_param_tag:
                    # no need to write table headers as we already working on param
                    # i.e., table headers will be already written
                    pass
                else:
                    # we just encountered first param, so writing param table headers
                    html.write(get_param_table_header_html())
                    working_on_param_tag = True
            else:  # some other tag, check if we were working on param table and end table if needed
                working_on_param_tag = False
                if written_param_count > 0:
                    # means we were working on param so need to close it
                    html.write('</table></div>')
                    written_param_count = 0  # reset counter
            html.write(get_html_for_tag(comment_data))
        html.write('</body></html>')


def create_index_page(project_name: str, index_html_file_path: str, files_info: list) -> None:
    """
    Creates a index page or (home page) which contains links to other documentation files.
    also contains created date. (this date is documentation created date and is not part of other documentation files)
    :param index_html_file_path: fully qualified file_path to create index file
    :param files_info: list of file info dictionaries 
            {'file_path':file_path, 'file_name':input_file_name, 'no_of_lines':len(all_data), 'no_of_comment_lines':len(comments_data)}
    :return: None
    """
    
    with open(index_html_file_path, "w") as html:
        html.write(get_base_html(project_name))
        html.write(
            '<div><span class="header">' + project_name + ' - Documentation</span></div>')
        # writing creation date
        html.write('<div><span class="label">Created on: </><span>' +
                   str(time.strftime("%b %d, %Y")) + '</span></div>')
        html.write('<div><span class="file">Files:</span></div>')
        for file_info in files_info:
            file_name = file_info['file_name'].lower().replace(".txt", "")
            html.write(
                f'<div><span class="file-link">'
                f'<a href="{file_name}.html" target="_blank" rel="noreferrer">{file_name.capitalize()}</a></span></div>')
            html.write('<br>')
            html.write(f'<div><table><tr><th><span class="label">File Path:</span></th><td><span><a href="file:///{file_info["file_path"]}" target="_blank" rel="noreferrer">{file_info["file_path"]}</a></span></td></tr></table></div>')
            html.write(f'<div><table><tr><th><span class="label">No of Comment lines:</span></th><td><span>{file_info["no_of_comment_lines"]}</span></td></tr></table></div>')
            html.write(f'<div><table><tr><th><span class="label">Total Number of lines:</span></th><td><span>{file_info["no_of_lines"]}</span></td></tr></table></div>')
            html.write('<br><br>')
        html.write('<div class="footer"><p class="footer-content">Documentation auto generated by <a href="https://dillir07.github.io/aadoc/" target="_blank" style="text-decoration:none"><span id="doc"><span id="aa">AA</span>Doc</span></a> tool, by <a class="author" href="mailto:dillir07@outlook.com">Dilli Babu R</a></p></div>')
        html.write('</body></html>')


def create_style_sheet(css_file_path: str) -> None:
    """
    Creates a stylesheet file (.css) which contains style rules for elements used in documentation.
    :param css_file_path: fully qualified path.
    :return: None
    """
    css_source = stylesheet_source.stylesheet_source_data
    with open(css_file_path, 'w') as css:
        css.write(css_source)


def process_inputs(project_name, code_folder_path: str, output_folder_path: str) -> None:
    """
    This function takes input_folder_path which is code_folder_path and output_folder_path which is destination folder
    path for writing output html.
    Then reads the list of text files in the folder and calls process_file method iteratively. Once all the files are
    processed then creates index page by calling create_index_page method and then creates stylesheet by calling
    create_style_sheet method.
    :param code_folder_path: input folder path where .txt files are present.
    :param output_folder_path: destination folder path to write html outputs.
    :return: None
    """

    print('processing files at', code_folder_path)
    files = os.listdir(code_folder_path)
    files_info = []
    text_files = [file for file in files if file.lower().endswith('.txt')]
    if len(text_files) <= 0:
        print('No text files are available in the given folder to process')
        return  # no files to process

    if output_folder_path == '':
        output_folder_path = code_folder_path + "\\" + "output"
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for text_file in text_files:
        print('processing', text_file)
        file_info = process_file(code_folder_path + '\\' + text_file, output_folder_path)
        files_info.append(file_info)
    create_index_page(project_name, output_folder_path + '\\' + "index.html", files_info)
    create_style_sheet(output_folder_path + '\\' + "styles.css")


def aa_doc() -> None:
    """
    This method bootstraps the arg_parse module and verifies the inputs given by the user via CLI.
    Then calls process_input() method.
    :return: None
    """
    arg_parser = argparse.ArgumentParser(
        description='A tool that generates documentation from Automation Anywhere comments inside code (.txt) files, '
                    'text files can be '
                    'created in Automation Anywhere Client, by going to "File" menu and then selecting "Save as text '
                    'file".',
        epilog='If you require any help, please reach out to me at dillir07@outlook.com')

    arg_parser.add_argument('input_folder_path', metavar=r'"C:\..\code files\input"',
                            type=str, help='folder path in which Automation Anywhere code .txt files are present')
    arg_parser.add_argument('output_folder_path', metavar=r'"C:\..\output"', type=str, nargs='?', default='',
                            help='Destination to store generated documentation files, if not provided an output folder '
                                 'will be created inside input folder.')
    args = arg_parser.parse_args()

    interactive = False

    if interactive:
        project_name = input('Please enter project name')
    else:
        project_name = 'Project'
    
    if project_name.strip() == '':
        project_name = 'Project'
    process_inputs(project_name, args.input_folder_path, args.output_folder_path)


# program execution starts here
# if __name__ == "__main__":
#     aa_doc()
