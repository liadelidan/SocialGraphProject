#! /usr/bin/env python2
import json
import requests


def count_user_commits(user):
    r = requests.get('https://api.github.com/users/%s/repos' % user)
    repos = json.loads(r.content)

    for repo in repos:
        if repo['fork'] is True:
            # skip it
            continue
        n = count_repo_commits(repo['url'] + '/commits')
        repo['num_commits'] = n
        yield repo


def count_repo_commits(commits_url, _acc=0):
    r = requests.get(commits_url)
    commits = json.loads(r.content)
    n = len(commits)
    if n == 0:
        return _acc
    link = r.headers.get('link')
    if link is None:
        return _acc + n
    next_url = find_next(r.headers['link'])
    if next_url is None:
        return _acc + n
    # try to be tail recursive, even when it doesn't matter in CPython
    return count_repo_commits(next_url, _acc + n)


# given a link header from github, find the link for the next url which they use for pagination
def find_next(link):
    for l in link.split(','):
        a, b = l.split(';')
        if b.strip() == 'rel="next"':
            return a.strip()[1:-1]



user = 'liadelidan'
nodes = '{"nodes": [{"id": "project", "group": 0}, {"id": "test", "group": 0}'
links = '"links": [{"source": "test", "target": "project", "value": 1}'
group = 0
for repo in count_user_commits(user):
    group += 1
    links += ',{"source": "' + str(repo['name']) + '0", "target": "project", "value": 1}'
    for i in range(int(repo['num_commits'])):
        nodes += ',{"id": "' + str(repo['name']) + str(i) + '", "group": ' + str(group) + '}'
        links += ',{"source": "' + str(repo['name']) + str(i) + '", "target": "' + str(repo['name']) + '0", "value": 1}'

nodes += "],"
links += "  ]}"


new_data = nodes+links
with open('data.json', 'w') as f:
    f.write(new_data)