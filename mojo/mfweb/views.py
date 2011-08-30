from django.contrib.sessions.backends.file import SessionStore
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.conf import settings
from django import forms

from datetime import datetime
from urllib2 import urlopen
from json import loads

# Monkeyfarm path
mfroot = settings.MF_BASE_URL.rstrip('/')

#
# Helper functions not tied to templates
#

def template_sort(results):
    '''Sort our results in a proper order'''
    mysort = (
                'id',
                'label',
                'groups',
                'source_name',
                'build_label',
                'summary',
                'status_label',
                'package_label',
                'package_branch_label',
                'display_name',
                'create_date',
                'start_date',
                'update_date',
                'end_date',
                'email',
                'password',
                'api_key',
                'verify_code',
                'agreed_to_terms',
                'full_version',
                'major_version',
                'minor_version',
                'branches',
                'user_label',
                'group_label',
                'distro_label',
                'arch_label',
                'release_label',
                'tag_path',
                'host_signature',
                'tag_label',
                'build_handler_label',
                'build_count',
                'project_label',
                'target_label',
                'system_label',
                'releases',
                'build_type_label',
                'pre_tag_label',
                'tags',
                'scratch',
                'scratch_url',
                'bugs',
                'bug_urls',
                'eol',
                'fs_path',
                'tasks',
                'footprint',
                'one_per_system',
                'manage_repo',
                'auto_reup',
                'close_on_tag',
                'include_in_builds',
                'url',
                'only_latest',
                'locked',
                'requires_admin',
                'notes',
                'users',
                'restricted',
                'pending_users',
                'about',
                'karma',
                'comments',
                'config',
                'configs',
                'logs',
                'files',
                'sources',
                'builds',
                'build_prefix',
                'exclude_releases',
                'build_on_commit',
                'vcs_branch',
                'excluded_releases'
            )

    if results[0] in mysort:
        return mysort.index(results[0])
    else:
        return len(mysort) + 1

def get_project(request):
    '''Get our current Monkeyfarm project and save in session'''
    if request.method == 'GET':
        try:
            project = request.GET['project']
        except KeyError:
            try:
                project = request.session['project']
            except KeyError:
                project = 'ius'
    else:
        try:
            project = request.session['project']
        except KeyError:
            project = 'ius'

    # add project to session
    request.session['project'] = project

    return project

def date_format(resultDict):
    '''Modify create_date to ctime()'''
    for r in resultDict['results']:
        r['create_date'] = datetime.strptime(r['create_date'], '%Y-%m-%d %H:%M:%S').ctime()
    return resultDict

def result_dictionary(request, r, page):
    '''Creates a default result dictionary to send to our templates'''

    # get a list of all MF Projects    
    projects = getmf_json(
                    '%s/project/get_all.json' % (mfroot), 'projects', 'label')
    
    # get all systems in MF
    systems = getmf_json(
                    '%s/system/get_all.json' % (mfroot), 'systems', 'label'
    )
    
    resultDict = {}
    
    # if we give a list lets limit its data
    # to 75 items
    if type(r) == list:
        results = r[0:75]
    else:
        results = r
       
    resultDict['result'] = results
    resultDict['project'] = get_project(request)
    resultDict['project_list'] = projects
    resultDict['systems'] = systems
    resultDict['page'] = page
   
    # sort in the proper order
    try:
        resultDict['results'] = sorted(results.items(), key=template_sort)
    except AttributeError:
        resultDict['results'] = results

    return resultDict

def getmf_json(url, type, order=False, rev=False):
    '''Makes our Monkeyfarm request and parses with lib json,
    after we will pull the data and sort it by key'''
    request = urlopen(url).read()
    json = loads(request)
    result = json['data'][type]
        
    if order:
        # order the data by key    
        result.sort(key=lambda x: x[order], reverse=rev)
    return result

#
# Views tied directly to web templates
#

def builds(request):
    '''Request to the root of the website will land on this function'''
    # verify our working project
    project = get_project(request)

    builds = getmf_json(
                   '%s/build/get_all.json?project_label=%s' % (mfroot, project),
                   'builds',
                   'create_date',
                   True)
    
    # build our results for the template    
    resultDict = result_dictionary(request, builds, 'build')
    
    # change create_date to ctime()
    resultDict = date_format(resultDict)
    return render(request, 'listpage.html', resultDict)
        
def tasks(request):
    '''Func for returning all task on a project'''
    # verify our working project
    project = get_project(request)

    tasks = getmf_json(
                   '%s/task/get_all.json?project_label=%s' % (mfroot, project),
                   'tasks',
                   'create_date',
                   True)
    
    # build our results for the template    
    resultDict = result_dictionary(request, tasks, 'task')
    
    # change create_date to ctime()
    resultDict = date_format(resultDict)

    return render(request, 'listpage.html', resultDict)

def buildinfo(request, label):
    '''Grab all json information from a build'''
    # verify our working project
    project = get_project(request)

    build = getmf_json(
                   '%s/build/%s/get_all.json?project_label=%s' % (mfroot, label, project),
                   'build')
    
    # get status of a task for template
    t_status = []
    for task in build['tasks']:
        taskinfo = getmf_json(
                   '%s/task/%s/get_all.json?project_label=%s' % (mfroot, task, project),
                   'task')
        status = taskinfo['status_label']
        t_status.append((task, status))
    build['tasks'] = t_status
    
    # build our results for the template    
    resultDict = result_dictionary(request, build, 'build')
    return render(request, 'infopage.html', resultDict)

def taskinfo(request, label):
    '''Grab all json information from a task'''
    # verify our working project
    project = get_project(request)

    task = getmf_json(
                   '%s/task/%s/get_all.json?project_label=%s' % (mfroot, label, project),
                   'task')
    
    # build our results for the template    
    resultDict = result_dictionary(request, task, 'task')
    return render(request, 'infopage.html', resultDict)

def packages(request):
    '''Return all packages in a project'''
    # verify our working project
    project = get_project(request)

    packages = getmf_json(
                    '%s/package/get_all.json?project_label=%s' % (mfroot, project),
                    'packages')  

    # build our results for the template    
    resultDict = result_dictionary(request, packages, 'package')
    return render(request, 'listpage.html', resultDict)
    
def packageinfo(request, label):
    '''Grab all json information from a package'''
    # verify our working project
    project = get_project(request)

    package = getmf_json(
                   '%s/package/%s/get_all.json?project_label=%s' % (mfroot, label, project),
                   'package')
    
    # build our results for the template    
    resultDict = result_dictionary(request, package, 'package')
    return render(request, 'infopage.html', resultDict)
    
def users(request):
    '''Return all users registered in Monkeyfarm'''
    # verify our working project
    project = get_project(request)

    users = getmf_json(
                    '%s/user/get_all.json' % (mfroot),
                    'users')  

    # build our results for the template    
    resultDict = result_dictionary(request, users, 'user')
    return render(request, 'listpage.html', resultDict)
    
def userinfo(request, label):
    '''Return all json information from a user'''
    # verify our working project
    project = get_project(request)

    user = getmf_json(
                    '%s/user/%s/get_all.json' % (mfroot, label),
                    'user')  

    # build our results for the template    
    resultDict = result_dictionary(request, user, 'user')
    return render(request, 'infopage.html', resultDict)
    
def groups(request):
    '''Return all groups registered in Monkeyfarm'''
    # verify our working project
    project = get_project(request)

    groups = getmf_json(
                    '%s/group/get_all.json' % (mfroot),
                    'groups')   
        
    # build our results for the template    
    resultDict = result_dictionary(request, groups, 'group')
    return render(request, 'listpage.html', resultDict)
    
def groupinfo(request, label):
    '''Return all json information from a user'''
    # verify our working project
    project = get_project(request)

    group = getmf_json(
                    '%s/group/%s/get_all.json' % (mfroot, label),
                    'group')  

    # build our results for the template    
    resultDict = result_dictionary(request, group, 'group')
    return render(request, 'infopage.html', resultDict)
    
def tags(request):
    '''Return all tags in a project'''
    # verify our working project
    project = get_project(request)

    tags = getmf_json(
                    '%s/tag/get_all.json?project_label=%s' % (mfroot, project),
                    'tags')   
        
    # build our results for the template    
    resultDict = result_dictionary(request, tags, 'tag')
    return render(request, 'listpage.html', resultDict)
    
def taginfo(request, label):
    '''Grab all json information from a tag'''
    # verify our working project
    project = get_project(request)

    tag = getmf_json(
                   '%s/tag/%s/get_all.json?project_label=%s' % (mfroot, label, project),
                   'tag')
    
    # build our results for the template    
    resultDict = result_dictionary(request, tag, 'tag')
    return render(request, 'infopage.html', resultDict)

def packagebranchinfo(request, label):
    '''Grab all json information from a tag'''
    # verify our working project
    project = get_project(request)

    packagebranch = getmf_json(
                   '%s/package_branch/%s/get_all.json?project_label=%s' % (mfroot, label, project),
                   'package_branch')
    
    # build our results for the template    
    resultDict = result_dictionary(request, packagebranch, 'packagebranch')
    return render(request, 'infopage.html', resultDict)

def targets(request):
    '''Return all tags in a project'''
    # verify our working project
    project = get_project(request)

    targets = getmf_json(
                    '%s/target/get_all.json' % (mfroot),
                    'targets')   
        
    # build our results for the template    
    resultDict = result_dictionary(request, targets, 'target')
    return render(request, 'listpage.html', resultDict)
    
def targetinfo(request, label):
    '''Grab all json information from a tag'''
    # verify our working project
    project = get_project(request)

    target = getmf_json(
                   '%s/target/%s/get_all.json' % (mfroot, label),
                   'target')
    
    # build our results for the template    
    resultDict = result_dictionary(request, target, 'target')
    return render(request, 'infopage.html', resultDict)

def systems(request):
    '''Return all systems'''
    # verify our working project
    project = get_project(request)

    systems = getmf_json(
                    '%s/system/get_all.json' % (mfroot),
                    'systems')  

    # build our results for the template    
    resultDict = result_dictionary(request, systems, 'system')
    return render(request, 'listpage.html', resultDict)
    
def systeminfo(request, label):
    '''Grab all json information from a package'''
    # verify our working project
    project = get_project(request)

    system = getmf_json(
                   '%s/system/%s/get_all.json' % (mfroot, label),
                   'system')
    
    # build our results for the template    
    resultDict = result_dictionary(request, system, 'system')
    return render(request, 'infopage.html', resultDict)

def search(request):
    '''Handle searches from the web interface'''
    # verify our working project

    if request.method == 'GET':
        project = get_project(request)
        try:
            search_type = request.GET['type']
            search_word = request.GET['search']
        except KeyError:
            return builds(request)
        else:
            
            url = '%s/%s/get_all.json?project_label=%s&mf_search_query=%s' % (
                                    mfroot, search_type, project, search_word)
            
            results = getmf_json(url, search_type+'s', 'create_date', True)
            
            # build our results for the template    
            resultDict = result_dictionary(request, results, search_type)
            return render(request, search_type+'s.html', resultDict)
        
