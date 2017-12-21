import github
from github import Github


# user_name = input('Please Enter your GitHub UserName: '
# password = input('Please Enter your GitHub Password: ')


g = Github('2deea60c5efb17e2623e13cf3324fad5e992cc2f')
for repo in g.get_user('FriedrichBu').get_repos():
    print (repo.name)

print(g.get_user('tipsy').followers)

# print("Wrong login details")