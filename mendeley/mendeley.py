#!/usr/bin/env python

from mendeley_client import *
import os
import sys
import json
import codecs

def lib( client ):
	A = []
	page = 0
	pages = 1
	while page < pages:
		r = client.library( page = page, items = 1000 )
		pages = r['total_pages']
		A.append( r['documents'] )
		page = page + 1
	A = sum( A, [] )
	return map( lambda x : client.document_details( x )  , map( lambda x: x['id'],  A ) )

def write( file, data):
	f = open('../' + file, 'w')
	f.write( json.dumps( data ) )
	f.close()

# edit config.json first
mendeley = create_client()
response = mendeley.library()

data = []
data = lib( mendeley )

data.sort(  key=lambda x: x['year'] if 'year' in x else '9999', reverse=True )

write('all.json', data )

## select starred
starred = filter( lambda x: x['isStarred'] != u'0', data )
write('star.json', starred )

## latest additions
data.sort(  key=lambda x: x['added'], reverse=True )
write('latest.json', data[:15] )

## my own papers
response = mendeley.documents_authored()

own = map( lambda x : mendeley.document_details( x )  , map( lambda x: x['id'],  response['documents'] ) )
own.sort(  key=lambda x: x['year'], reverse=True )

write('my-all.json', own )

## can also be cherrypicked, e.g.
## tags = ['sna', 'politics', 'participation', 'education']
tags = sum( map( lambda x: x['tags'], own ) , [] )

been = []
results = {}

for tag in tags:
        f = filter( lambda d : tag in d['tags'], own )
        ## add items as been already
        map( lambda d: been.append( d['id'] ) , f )
        results[tag] = f

f = filter( lambda d : d['id'] not in been , own )
results['others'] = f

write('my.json', results)


## information about folders
folders = mendeley.folders()
folders.sort( key = lambda x: x['size'], reverse=True )
write('folders.json', folders )
