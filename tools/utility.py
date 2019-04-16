import os
import chardet
import re

rootdir=os.path.dirname(os.path.abspath(__file__))+"/../docs"
dirmaplist={}
dirkeylist=[]

def initdirmaplist():
  for root, _, _ in os.walk(rootdir, False):
    basename = os.path.basename(root)
    if basename != "images" and basename != "docs" and basename != "rsts" and basename != "_static":
      list = os.listdir(root)
      list.sort()
      dirmaplist[root] = list

def convert():
  for root in dirkeylist:
    print(root)
    basename = os.path.basename(root)
    if basename != "images" and basename != "docs" and basename != "rsts" and basename != "_static":
      for file in dirmaplist[root]:
        f = open(root+"/"+file, "rb+")
        data = f.read()
        charset = chardet.detect(data)["encoding"]
        if len(data) <= 0:
          title = "# {name}\n\n".format(name=file[file.find("_")+1:file.rfind(".")])
          if charset != None:
            f.write(title.decode(charset).encode("utf-8"))
          else:
            f.write(title.encode("utf-8"))
          f.close()
          continue
        f.seek(0, 0)
        line = f.readline()
        pattern = re.compile(r'(#{1,4}?)( ?)((\w+|\d{0,2})(\.(\d{0,2})){1,3})? (.*)')
        if charset != None:
          intro = pattern.findall(line.decode(charset).encode("utf-8").decode("utf-8"))
        else:
          intro = pattern.findall(line.decode("utf-8"))
        if len(intro) > 0 and len(intro[0]) == 7:
          if len(intro[0][0]) == 1:
            title = ""
          else:
            title = "# {chapter} {name}\n\n".format(chapter=intro[0][2],name=intro[0][6])
        else:
          title = "# {name}\n\n".format(name=file[file.find("_")+1:file.rfind(".")])
        # data = data.replace(b'\r\n', b'\n')
        
        print(charset, file)
        if charset != None:
          data = data.decode(charset).encode("utf-8")
          f.seek(0, 0)
          if title != "":
            f.write(title.encode("utf-8"))
          f.write(data)
        f.close()

def mk_int(s):
  s = s.strip()
  return int(s) if s else 0

def summary():
  sf = open(rootdir+"/summary.md", "w+")
  sf.write("# 目录\n\n")
  sf.write("<style>p{margin-bottom:0 !important;}</style>\n")
  for root in dirkeylist:
    alpha=0
    basename = os.path.basename(root)
    if basename != "images" and basename != "docs" and basename != "rsts":
      for file in dirmaplist[root]:
        name = basename+"/"+file
        f = open(root+"/"+file, "r")
        line = f.readline()
        print(basename, file)
        pattern = re.compile(r'#{1,4}? ((\w+|\d{0,2})(\.(\d{0,2})){1,3})? (.*)')
        intro = pattern.findall(line)
        if len(intro) > 0 and len(intro[0]) == 5:
          title = intro[0][4]
        else:
          title = file[file.find("_")+1:file.rfind(".")]
        pattern = re.compile(r'((\w+|\d{0,2})(\.(\d{0,2})){1,3})')
        match = pattern.findall(file)
        if len(match) > 0 and len(match[0]) > 0:
          s = match[0][0].split(".")
          if len(s) == 3 and s[0].isalpha() and alpha == 0:
            txt = "* {chapter}. [{title}](./{name})\n".format(chapter=file[0:file.find(".")], title=title, name=name)
            sf.writelines(txt)
          elif (len(s) == 3 and mk_int(s[1]) == 0 and mk_int(s[2]) == 0):
            txt = "* {chapter}. [{title}](./{name})\n".format(chapter=file[0:file.find("_")], title=title, name=name)
            sf.writelines(txt)
          if (len(s) == 3 and s[0].isalpha() and mk_int(s[1]) != 0) or (len(s) == 3 and mk_int(s[1]) != 0 and mk_int(s[2]) == 0 and not s[0].isalpha()):
            txt = "  - {chapter}. [{title}](./{name})\n".format(chapter=file[0:file.find("_")], title=title, name=name)
            sf.writelines(txt)
          if len(s) == 3 and mk_int(s[1]) != 0 and mk_int(s[2]) != 0 and not s[0].isalpha():
            txt = "    - {chapter}. [{title}](./{name})\n".format(chapter=file[0:file.find("_")], title=title, name=name)
            sf.writelines(txt)
          if len(s) == 4 and mk_int(s[1]) != 0 and mk_int(s[2]) != 0 and mk_int(s[3]) != 0 and not s[0].isalpha():
            txt = "      - {chapter}. [{title}](./{name})\n".format(chapter=file[0:file.find("_")], title=title, name=name)
            sf.writelines(txt)
          if len(s) == 3 and s[0].isalpha():
            alpha+=1
        f.close()
  sf.close()

def index():
  sf = open(rootdir+"/index.rst", "w+")
  sf.write('''.. mysql_zh_manual56 documentation master file, created by
   sphinx-quickstart on Fri Apr 12 00:40:42 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mysql_zh_manual56's documentation!
=============================================

.. toctree::
   :maxdepth: 2
   :caption: mysql56中文文档:\n\n''')
  sf.write("   summary.md\n")
  sf.write("   glossary.md\n")
  for root in dirkeylist:
    alpha=0
    basename = os.path.basename(root)
    if basename != "images" and basename != "docs" and basename != "rsts":
      for file in dirmaplist[root]:
        pattern = re.compile(r'((\w+|\d{0,2})(\.(\d{0,2})){1,3})')
        match = pattern.findall(file)
        if len(match) > 0 and len(match[0]) > 0:
          s = match[0][0].split(".")
          title=""
          if (len(s) == 3 and s[0].isalpha() and  mk_int(s[1]) != 0 and mk_int(s[2]) == 0):
            title=s[0]
            alpha+=1
          if (len(s) == 3 and mk_int(s[1]) == 0 and mk_int(s[2]) == 0 and not s[0].isalpha()):
            title=file[:file.rfind(".")]
          if title != "":
            chapter = "rsts/{title}.rst".format(title=title)
            print(basename, chapter)
            if (alpha == 1 and len(title) == 1) or len(title) > 1:
              sf.write("   "+chapter+"\n")
            if not os.path.exists(rootdir+"/rsts"):
              os.mkdir(rootdir+"/rsts")
            cf = open(rootdir+"/"+chapter, "w+")
            cf.write('''


{title}
{underline}

.. toctree::
   :caption: {title}:
   :maxdepth: 1\n\n'''.format(title=title,underline="="*(5+len(title))))
            cffs = os.listdir(rootdir+"/"+basename)
            cffs.sort()
            for cff in cffs:
              toc = "   ../{name}\n".format(name=basename+"/"+cff)
              cf.write(toc)
            cf.close()
  sf.write("\n\n\n")
  sf.close()

if __name__ == "__main__":
  import sys
  initdirmaplist()
  dirkeylist=sorted(dirmaplist.keys())
  if len(sys.argv) >= 2:
    fn = sys.argv[1]
    if fn in dir():
      eval(fn+"()")
    else:
      print(fn, " not exists")
  else:
    convert()
    summary()
    index()