#! /usr/bin/env python

import json, urllib, os, os.path, errno

class book(dict):
  def __init__(self,isbn,meta={},upgrade=True):
    self.isbn=isbn
    self.update(meta)
    if upgrade:
      self.upgradebookmeta()

  def bookmetajsonurl(self):
    return "http://xisbn.worldcat.org/webservices/xid/isbn/"+self.isbn+"?method=getMetadata&fl=*&format=json"
  
  def upgradebookmeta(self):
    bomejsur=urllib.urlopen(self.bookmetajsonurl())
    self.update(json.load(bomejsur)['list'][0])
    bomejsur.close()

def json_load_book(bojson):
  bodict=json.load(bojson)
  return book(bodict['isbn'],bodict,False)

class bookshelf(dict):
  def __init__(self, path):
    self.path=path
    if not os.path.exists(path):
      os.makedirs(path)
    elif not os.path.isdir(path):
      raise OSError(errno.ENOTDIR)
    self.loadbookshelf()

  def __del__(self):
    if 'y'==raw_input('Save changes? (y): ').lower():
      self.save()

  def loadbookshelf(self):
    bookfiles=os.listdir(self.path)
    if not os.path.exists(self.path+'/bookshelf.json'):
      self.meta={} #empty dict
    else:
      bookfiles.remove('bookshelf.json')
      bsmefi=open(self.path+'/bookshelf.json')
      self.meta=json.load(bsinfi)
      bsmefi.close()
    for bofina in bookfiles:
      bofi=open(self.path+'/'+bofina)
      bona=bofina[:-5] #[:-len('.json')]
      self[bona]=json_load_book(bofi)
      bofi.close()

  def save(self):
    while self.has_key('bookshelf'):
      newname=raw_input('Please give a different name for the book "bookshelf": ')
      if newname!='bookshelf':
        self[newname]=self['bookshelf']
        del self['bookshelf']
    for bo in self:
      bofi=open(self.path+'/'+bo+'.json','w')
      json.dump(self[bo],bofi)
      bofi.close()
    bsmefi=open(self.path+'/bookshelf.json','w')
    json.dump(self.meta,bsmefi)
    bsmefi.close()

def bookcollector():
  bs=None
  while True:
    if isinstance(bs,bookshelf):
      path=raw_input('Bookshelf path (default: '+bs.path+'): ')
      if path!='':
        bs=bookshelf(path)
    else:
      bs=bookshelf(raw_input('Bookshelf path: '))
    key=raw_input('Book key (q to exit): ')
    if key.lower()=='q':
      break
    else:
      bs[key]=book(raw_input('ISBN: '))
      updatejss=raw_input('Other updates (json): ')
      if updatejss!='':
        bs[key].update(json.loads(updatejss))
      print json.dumps(bs[key])

bookcollector()
