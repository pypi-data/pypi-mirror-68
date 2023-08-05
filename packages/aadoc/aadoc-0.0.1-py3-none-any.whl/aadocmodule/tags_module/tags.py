"""
This file is the source list of all the tags used by aadoc.
This is return a regex pattern by joining all the tags and returning as string.

new tags can be added and old tags can be modified or removed.
Note: Making changes would require changes in other parts of the code as well.
mostly in html_helpers.py file.

Note: Tags are inspired by jsDoc tags at https://jsDoc.app

"""


def generate_tags_for_re() -> str:
    """
    Reads tags list and generates re match pattern
    :return: re-match pattern of tags separated by '|',
                which created by joining tags using join function.
    """

    tags_list = [
        '@author',
        '@date',
        '@constant',
        '@copyright',
        '@default',
        '@deprecated',
        '@description',
        '@file',
        '@function',
        '@global',
        '@ignore',
        '@license',
        '@module',
        '@name',
        '@namespace',
        '@package',
        '@param',
        '@requires',
        '@returns',
        '@see',
        '@since',
        '@summary',
        '@throws',
        '@todo',
        '@type',
        '@version',
    ]
    return '|'.join(tags_list)
