def Help(s=None):
      if s==None:
            Help_ext()
      else:
            Help_main(s)

      return None


def Help_ext(ss=None):
      helpw='''
Welcome to Mydemos_pkg 1.7.0's help utility!

Enter the name of any module, keyword, or topic to get help on writing
Python programs and using Python modules.  To quit this help utility and
return to the interpreter, just type "quit".

To get a list of available modules, type "modules".  Each module also comes with a one-line summary of what it does; to list the modules whose name
or summary contain a given string such as "spam", type "modules spam".
'''
      helpw1='''

help> '''
      hb='''
about bytedesign:
you can output an amazing graph usage:
from Mydemos_pkg import bytedesign
bytedesign.bytedesign()
and look at the turtle-graph!
'''
      hch='''
about chaos:
it make a chaos line to you!
from Mydemos_pkg import chaos
chaos.chaos()
'''
      hcl='''
about clock:
it make a clock to you!
from Mydemos_pkg import clock
clock.clock()
'''

      hco='''
about colormixer:
it make a colormixer to you and u can use your mouse to control it!
from Mydemos_pkg import colormixer
colormixer.colormixer()
'''
      hcs='''
about colorspiral:
it make a colorspiral!
from Mydemos_pkg import colorspiral
colorspiral.colorspiral(6)#sides
'''
      hd='''
about download:
it download a file!
from Mydemos_pkg import download_file
download_file.download(\"http://www.example.com/demo.pdf\")
'''
      hf='''
about forest:
it make a forest!
from Mydemos_pkg import forest
forest.forest() #only_debug
'''
      hfr='''
it makes a curve!
from Mydemos_pkg import fractalcurves
fractalcurves.fractalcurves()
'''
      hh='''
it shows you how hanoi game worked.
from Mydemos_pkg import hanoi
hanoi.hanoi()
'''

      hl='''
it make a lindenmayer.
from Mydemos_pkg import lindenmayer
lindenmayer.lindenmayer()
'''
      hpa='''
it make a paint software.
from Mydemos_pkg import paint
paint.paint()
'''
      hpe='''
it make a peace.
from Mydemos_pkg import peace
peace.peace()
'''
      hpen='''
it make a penrose.
from Mydemos_pkg import penrose
penrose.penrose()
'''
      hpi='''
it could install or uninstall or upgrade sth modules.
usage:
from Mydemos_pkg.pip_install import *
install('paddlehub')
upgrade('paddlehub')
uninstall('paddlehub')
'''
      hpl='''
it make earth,sun,moon.
from Mydemos_pkg import planet_and_moon
planet_and_moon.planet_and_moon()
'''

      hpr='''
it make a progress.
from Mydemos_pkg import progress
progress.progress(0.1)#delay
'''
      hro='''
it make a rosette.
from Mydemos_pkg import penrose
rosette.rosette()
'''
      hr='''
it make a round_dance.
from Mydemos_pkg import round_dance
round_dance.round_dance()
'''
      hs='''
it sort_test.
from Mydemos_pkg import sort
sort.sort_test()
'''
      hsa='''
it sort_test.
from Mydemos_pkg import sort_animate
sort_animate.sort_animate()
'''
      ht='''
it make a tree.
from Mydemos_pkg import tree
tree.tree()
'''
      htw='''
it make two canvas.
from Mydemos_pkg import two_canvas
two_canvas.two_canvas()
'''
      huc='''
it converts unicodes.
nonBMPtoBMP ->unicodes from nonBMP to BMP,if you: print(nonBMPtoBMP('\\U0001F600'))onidle you get a emoji!
'''

      hu='''
make a whole unicode map.
make_unicode ->make unicodemap.
unicode_1 ->BMP
unicode_2 ->Plane2
BMP_plane2 -> BMP and Plane2
'''

      hy='''
it make a yinyang graph.
from Mydemos_pkg import yinyang
yinyang.yinyang()
'''
     #ok
      all_helps={'bytedesign':hb,
                      'chaos':hch,
                      'clock':hcl,
                      'colormixer':hco,
                      'colorspiral':hcs,
                      'download_file':hd,
                      'forest':hf,
                      'fractalcurves':hfr,
                      'hanoi':hh,
                      'lidenmayer':hl,
                      'nim':'nim',
                      'paint':hpa,
                      'peace':hpe,
                      'penrose':hpen,
                      'pip_install':hpi,
                      'planet_and_moon':hpl,
                      'progress':hpr,
                      'rosette':hro,
                      'sort':hs,
                      'sort_animate':hsa,
                      'tree':ht,
                      'two_canvas':htw,
                      'unicodeconvert':huc,
                      'unicodes':hu,
                      'yinyang':hy}


      #print(all_helps)#debug
      mdd='''
bytedesign
chaos
clock
colormixer
colorspiral
download_file
forest
fractalcurves
hanoi
lidenmayer
nim
paint
peace
penrose
pip_install
planet_and_moon
progress
rosette
sort
sort_animate
tree
two_canvas
unicodeconvert
unicodes
yinyang
'''
      if ss==None:
          print(helpw)
          d=input(helpw1)
          while d.lower()!='quit':
                try:
                      print(all_helps[d])
                except KeyError:
                      if d.replace(' ','')=='':
                            sss='''
You are now leaving help and returning to the Python interpreter.
If you want to ask for help on a particular object directly from the
interpreter, you can type "help(object)".  Executing "help('string')"
has the same effect as typing a particular string at the help> prompt.
'''
                            print(sss)
                            return
                      if 'modules' in d:
                            if d.replace(' ','')=='modules':
                                  print(mdd)
                            else:
                                  try:
                                        print(all_helps[d.replace(' ','').replace('modules','')])
                                  except KeyError:
                                        print('No module found as %s'%d)
                      else:
                            print('No module found as %s'%d)
                d=input(helpw1)
          sss='''
You are now leaving help and returning to the Python interpreter.
If you want to ask for help on a particular object directly from the
interpreter, you can type "help(object)".  Executing "help('string')"
has the same effect as typing a particular string at the help> prompt.
'''
          print(sss)
      else:
          try:
              print(all_helps[d])
          except KeyError:
              if d=='modules':
                  print(mdd)
              else:
                  print('No anything found as %s'%ss)


def Help_main(s):
    Help_ext(s)
