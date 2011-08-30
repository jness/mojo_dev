from django.contrib.sessions.backends.file import SessionStore
from django.shortcuts import render_to_response, render
from django.http import Http404
from django.conf import settings
from django import forms

from re import search
from urllib2 import urlopen, HTTPError
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

def result_dictionary(request, r, viewtype):
    '''Creates a default result dictionary to send to our templates'''

    # get a list of all MF Projects and Systems 
    projects = get_mf_json(
                    '%s/project/get_all.json' % (mfroot), 'label')
    systems = get_mf_json(
                    '%s/system/get_all.json' % (mfroot), 'label')
   
    resultDict = {}
    # limit results to 50 items or less
    if type(r) == list:
        results = r[0:50]
    else:
        results = r

    # create the dict which will go to Django template
    resultDict['results'] = results
    resultDict['project'] = get_project(request)
    resultDict['project_list'] = projects
    resultDict['systems'] = systems
    resultDict['viewtype'] = viewtype

    # sort label names in the proper order
    try:
        resultDict['results'] = sorted(results.items(), key=template_sort)
    except AttributeError:
        resultDict['results'] = results
    except KeyError:
        resultDict['results'] = results

    return resultDict

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

def get_mf_json(url, order=False, rev=False):
    '''Makes our Monkeyfarm request and parses with lib json,
    after we will pull the data and sort it by key'''
    try:
        request = urlopen(url).read()
    except HTTPError:
        # try removing project label
        url = search('(.*)\?project_label=.*', url).group(1)
        try:
            request = urlopen(url).read()
        except HTTPError:
            raise Http404

    json = loads(request)
    result = json['data']
    result_types = result.keys()

    # determine the API call type
    for t in result_types:
        result_type = t
    data_results = result[result_type]

    # perform sorting if set
    if order:
        try:
            # order the data by key    
            data_results.sort(key=lambda x: x[order], reverse=rev)
        except AttributeError:
            pass
        except KeyError:
            pass

    return data_results

#
# Views tied directly to web templates
#

def mf_request(request, viewtype, label):
    '''Request to the root of the website will land on this function'''
    # verify our working project
    project = get_project(request)

    # provide differnt sort basedon viewtype
    sorts = {}
    sorts['build'] = 'create_date'
    try:
        order = sorts[viewtype]
    except KeyError:
        # default to label for sorting
        order = 'label'

    # check to see if this is a direct object request
    if label:
        s = '%s/%s/%s/get_one.json?project_label=%s' % (mfroot, viewtype, label, project)
        page = 'infopage.html'
    else:
        s = '%s/%s/get_all.json?project_label=%s' % (mfroot, viewtype, project)
        page = 'listpage.html'

    results = get_mf_json(s, order, True)

    
    # build our results for the template    
    resultDict = result_dictionary(request, results, viewtype)
    return render(request, page, resultDict)

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

            url = '%s/%s/get_all.json?mf_search_query=%s&project_label=%s' % (
                                    mfroot, search_type, search_word, project)

            results = get_mf_json(url, search_type, False)

            # build our results for the template    
            resultDict = result_dictionary(request, results, search_type)
            return render(request, 'listpage.html', resultDict)
            

