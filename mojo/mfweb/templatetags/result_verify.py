from django import template
from django.conf import settings

register = template.Library()
@register.filter

def result_verify(value, key):

    links = ('tags', 
             'groups', 
             'users', 
             'user_label', 
             'group_label', 
             'package_branch_label', 
             'archs',
             'tasks', 
             'build_label', 
             'package_label', 
             'build_handlers',
             'targets',
             'releases',
             'project_label',
             'vcs_handler_label',
             'distro_label',
             'build_handler_label')

    mfkey = key.rstrip('s')
    mfkey = mfkey.replace('_label', '')

    # handle all hyperlinks
    if key in links: 
        url = '<a href="%s%s/%s">%s</a>' % (settings.BASE_URL, mfkey, value, value)
        return url

    # branches label is really package_branch
    if key == 'branches':
        url = '<a href="%s%s/%s">%s</a>' % (settings.BASE_URL, 'package_branch', value, value)
        return url

    # handle comments
    elif key == 'comments':
        comment = "<b>%s</b> @ %s (<b>karma:</b> %s)<br>%s<br><br>" % (
                    value['user_label'],
                    value['create_date'],
                    value['karma'],
                    value['comment'])

        return comment

    # handle config block
    elif key == 'config':
        code = '<pre>%s</pre>' % value
        return code

    # handle Success/Fail colors
    elif value == 'BuildSuccess':
        color = '<font color="#00CC00">%s</font>' % value
        return color
    elif value == 'BuildFail':
        color = '<font color="red">%s</font>' % value
        return color

    else:
        return value

