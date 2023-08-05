"""
This file is part of aaDoc project. A tool used to generate documentation from Automation Anywhere code.
This file contains code and functions that provides HTML source code to write documentation.
These methods will be called by aadoc.py when appropriate by passing the tag name to get respective html source.
CSS class names will be automatically embedded into html before returning, customization can eb done to the css rules
without making changes to class name here.

We mostly use Template class of python's string module to interpolate the html source strings.

Note: Tags are inspired by jsDoc tags at https://jsDoc.app

"""

from string import Template


def get_author_html(comment_data: dict) -> str:
    """
    Provides html source for author tag i.e., @author
    A hyper link will be created if author value has an email id ('@' symbol) present between '<' and '>'.
    :param comment_data: A dictionary of type {'line_number': line_number, 'tag': '@example',
                        'value': 'author name <email@email.com>'}
    :return: html source for author
    """
    author = comment_data['value']  # assuming whole comment as name if email found truncate
    email = ''

    author_html = Template(
        '<div><table><tr><th><span class="label">Author:</span></th><td><span><a class="author" '
        'href="$email">$author</a></span></tr></table></div>')
    if '<' in comment_data['value'] and '>' in comment_data['value']:
        # email or website is present
        content_in_braces = (comment_data['value'])[
                            comment_data['value'].find('<') + 1:comment_data['value'].find('>')]
        # added mailto link if value contains '@' else place whatever is present (assuming it is a website url)
        email = 'mailto:' + content_in_braces if '@' in content_in_braces else content_in_braces
        author = author[:author.find('<')]

    return author_html.substitute(author=author.strip(), email=email)


def get_file_html(comment_data: dict) -> str:
    """
    Provides html source for file tag
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@file', value:'some file name'}
    :return: html code
    """
    file_html = Template('<div><span class="file">$file</span></div>')
    return file_html.substitute(file=comment_data['value'])


def get_date_html(comment_data: dict) -> str:
    """
    Provides html source for date tag.
    Note: No date validations or conversions are done.
    whatever value is provided by user's comments the same will come here.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@file', value:'some file name'}
    :return: html markup
    """
    date_html = Template(
        '<div><table><tr><th><span class="label">Date:</span></th><td><span>$date</span></td></tr></table></div>')
    return date_html.substitute(date=comment_data['value'])


def get_version_html(comment_data: dict) -> str:
    """
    Provides html source for version tag.
    Note: No version validations or conversions are done.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@version', value:'5.4'}
    :return: html markup
    """
    version_html = Template(
        '<div><table><tr><th><span class="label">Version:</span></th><td><span>$version</span></td></tr></table></div>')
    return version_html.substitute(version=comment_data['value'])


def get_since_html(comment_data: dict) -> str:
    """
    Provides html source for since tag.
    Note: No since version validations are done.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@since', value:'5.4 - Does something special'}
    :return: html markup
    """
    since_html = Template(
        '<div><table><tr><th><span class="label">Since:</span></th><td><span>$since</span></td></tr></table></div>')
    return since_html.substitute(since=comment_data['value'])


def get_copyright_html(comment_data: dict) -> str:
    """
    Provides html source for copyright tag.
    No copyright symbols or year values are included.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@copyright', value:'Dilli Babu R'}
    :return: html markup
    """
    copyright_html = Template(
        '<div><table><tr class="copyright"><th><span '
        'class="label">Copyright:</span></th><td><span>$copyright</span></td></tr></table></div>')
    return copyright_html.substitute(copyright=comment_data['value'])


def get_license_html(comment_data: dict) -> str:
    """
    Provides html source for license tag.
    :param comment_data: A dictionary of type {'line_number':25,
                                        'tag':'@license', value:'GNU General Public License v3.0'} :return: html markup
    :return: html markup
    """
    license_html = Template(
        '<div><table><tr class="license"><th><span '
        'class="label">License:</span></th><td><span>$license</span></td></tr></table></div>')
    return license_html.substitute(license=comment_data['value'])


def get_function_html(comment_data: dict) -> str:
    """
    Provides html source for function tag.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@function', value:'get_some_data()'}
    :return: html markup
    """
    function_html = Template('<div><span class="function">$function</span></div>')
    return function_html.substitute(function=comment_data['value'])


def get_requires_html(comment_data: dict) -> str:
    """
    Provides html source for requires tag.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@requires', value:'get_some_data()'}
    :return: html markup
    """
    requires_html = Template('<div><span class="requires">$requires</span></div>')
    return requires_html.substitute(requires=comment_data['value'])


def get_description_html(comment_data: dict) -> str:
    """
    Provides html source for description tag.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@description',
                                                value:'Some details description about a function or anything'}
    :return: html markup
    """
    description_html = Template('<div><span class="description">$description</span></div>')
    return description_html.substitute(description=comment_data['value'])


def get_param_html(comment_data: dict) -> str:
    """
    Provides html source for param tag.
    Here we will try to fill as much data as possible.
    Typically a param tag will be in for @param {Type} param_name - param description
    if any of them are missing we will try to fill the remaining values, by checking the existence of braces and hyphen.
    :param comment_data: A dictionary of type {'line_number':25, 'tag':'@param', value:'{Integer} count - File counter'}
    :return: html markup
    """
    param_html = Template(
        '<tr><td class="param-table-cell"><span>$name</span></td><td '
        'class="param-table-cell"><span>$type</span></td><td '
        'class="param-table-cell"><span>$description</span></td></tr>')
    type = ''
    name = ''
    description = ''
    if '{' in comment_data['value'] and '}' in comment_data['value']:
        type = (comment_data['value'])[
               comment_data['value'].find('{') + 1:comment_data['value'].find('}')]
        name = (comment_data['value'])[
               comment_data['value'].find('}') + 1:]
    if '-' in comment_data['value']:
        name = name[:name.find('-')]
        description = (comment_data['value'])[
                      comment_data['value'].find('-') + 1:]
    return param_html.safe_substitute(name=name.strip(), type=type.strip(), description=description.strip())


def do_nothing(comment_data: dict) -> None:
    """
    work in progress stuff, just returns readable format of comment data
    :param comment_data: {'line_number':25, 'tag':'@namespace', value:'name space'}
    :return: html mark up
    """
    wip_html = Template('<p class="nothing">$line_number, $tag, $value</p>')
    return wip_html.substitute(line_number=comment_data['line_number'], tag=comment_data['tag'],
                               value=comment_data['value'])


def get_empty_line_html(comment_data: dict) -> str:
    """
    Work in progress
    :param comment_data: {'line_number':25, 'tag':'@emptyline', value:''}
    :return: html mark up
    """
    return '<p>' + comment_data['line_number'] + '</p>'


def get_html_for_tag(comment_data: dict) -> str:
    """
    This method receives call from another files (aaDoc.py) and identifies the tag and call the appropriate function
    based on the tag.
    Note: Work in progress
    :param comment_data: {'line_number':25, 'tag':'@file', value:'file name'}
    :return: str (html markup)
    """
    html = {
        '@author': get_author_html,
        '@date': get_date_html,
        '@constant': do_nothing,
        '@copyright': get_copyright_html,
        '@default': do_nothing,
        '@deprecated': do_nothing,
        '@description': get_description_html,
        '@file': get_file_html,
        '@function': get_function_html,
        '@global': do_nothing,
        '@ignore': do_nothing,
        '@license': get_license_html,
        '@module': do_nothing,
        '@name': do_nothing,
        '@namespace': do_nothing,
        '@package': do_nothing,
        '@param': get_param_html,
        '@requires': get_requires_html,
        '@returns': do_nothing,
        '@see': do_nothing,
        '@since': get_since_html,
        '@summary': do_nothing,
        '@throws': do_nothing,
        '@todo': do_nothing,
        '@type': do_nothing,
        '@version': get_version_html,
        '@emptyline': get_empty_line_html,
    }
    return html[comment_data['tag']](comment_data)


def get_param_table_header_html() -> str:
    """
    This function returns table headers used in creating param table.
    Should not used used for other tables.
    :return: html mark up
    """
    return '<div><span class="property-title">Parameters</span></div><div><table class="param-table"><tr class="param-header-row"><th class="param-table-cell">Name</th><th ' \
           'class="param-table-cell">Type</th><th class="param-table-cell">Description</th></tr> '


def get_base_html(title: str = "Documentation") -> str:
    """
    Returns base html having HTML5 declaration, head tag, title tag and till start of the body tag.
    :param title: title for the web page, default is 'Documentation'
    :return: html mark up
    """
    base_template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="author" content="aaDoc tool written by Dilli Babu R <dillir07@outlook.com>">
    <meta name="description" content="This page contains documentation, which is auto generated by aaDoc tool
    by using the comments written in Automation Anywhere Code by developers.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#2B65EC">
    <title>$title</title>
    <link rel="stylesheet" href="styles.css">
    </head>
    <body>""")
    return base_template.safe_substitute(title=title)