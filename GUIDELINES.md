# Guidelines

## Docker
### Using docker compose:
https://docs.docker.com/samples/django/

## Github
1. **Pull** `develop` before you create a new branch from it
2. Name new branches after the issue you are working on.  Eg, `issue23`.
3. If you want to divide the tasks for work on an issue into multiple branches, append an underscore and the name the task.  Eg, `issue23_fix_urls`.
4. When working on your own branch, **pull before you push**
5. Never merge your own code into other branches.  Always create a pull request and get a teammate to review.
6. Open pull requests **early** and **push often**

## Git Commands:
### Create branch `new_branch` off of `existing_branch`
``` shell
$ git checkout existing_branch
$ git pull origin existing_branch
$ git checkout -b new_branch
$ git push origin new_branch -u
```

### Merge Branch `develop` into branch `my_branch`
``` shell
$ git checkout develop
$ git pull origin develop
$ git checkout my_branch
$ git pull origin my_branch
$ git merge develop
```

If you have merge conflicts, I recommend resolving them from inside VSCode.  