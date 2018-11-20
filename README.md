
# Mysite built with Django

## TODO
- [x] Article
- [x] Author
- [x] Category
- [x] Tags
- [x] Comment
- [x] Import/Export from/to markdown
  - hexo-style markdown file
- [x] user login via email

## How to run
clone this repo
```bash
$ cd mysite
$ source siteEnv/bin/activate
$ virtualenv -p python3 siteEnv
$ python manage.py runserver
```

### The way to export or import content

```bash
$ source siteEnv/bin/activate
$ python manage.py exportmd --help
$ python manage.py importmd --help
```