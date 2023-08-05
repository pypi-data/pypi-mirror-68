from setuptools import setup
 
NAME = 'Mydemos_pkg'
VERSION = '1.2.7.30'
PACKAGES = ['Mydemos_pkg']
setup(name = NAME
        , version = VERSION
        , packages = PACKAGES,
      description='a small pkg demos for you and everyone',
      long_description='''
Mydemos_pkg1.2.7.0will be a really-new-module:MyHelp!

USAGE just like help()!!!

IfYouSawIt,PleaseInstallIt!

走过路过，不要错过！
```shell
pip install Mydemos_pkg
```
~~lastest_version~~

OK,I will have a list for the version that released.


1.0.1.1

1.1.1.0

1.1.3.0

1.1.4.0

1.2.1.0

1.2.3.0

1.2.3.1


1.2.4.0:added unicode/cs

1.2.5.1:added unicodeerr

1.2.5.9:fixed NameError in unicodeconvert

1.2.6.0b1:may add things in nother way

1.2.6.0:make unicodes

1.2.6.2dev0:download_file.py added

1.2.6.2:added

1.2.7.0dev0 a pre-new module: __**MyHelp**__!!!!!!usage:
```py
from Mydemos_pkg.MyHelp import Help
Help(...)
```
1.2.7.0.debug: __**MyHelp**__ added pre-new command:quit!

1.2.7.0:release Help!

1.2.7.2:release a no-usage module:run!

1.2.7.30:fix progressError
```py
\'\'\'
USAGE
\'\'\'
from Mydemos_pkg.nim import nim
nim()
from Mydemos_pkg.sort import sort_test
sort_test()
```
so it's that.......
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

'''
      ,long_description_content_type='text/markdown'
) 
