#!/usr/bin/env python3
"""Instagram Graph API Reels publishing. Requires professional account and authorized token."""
import os, sys, time, json, urllib.request, urllib.parse, urllib.error
API=os.getenv('META_GRAPH_VERSION','v24.0')
BASE=f'https://graph.facebook.com/{API}'
TOKEN=os.environ['IG_ACCESS_TOKEN']
IG_ID=os.environ['IG_USER_ID']
VIDEO_URL=os.environ['VIDEO_URL']
CAPTION=os.environ.get('VIDEO_CAPTION','The Standard — 90 Days to Rebuild Yourself. Link in bio.')
def request(method,path,params):
    data=urllib.parse.urlencode({**params,'access_token':TOKEN}).encode()
    url=BASE+path
    if method=='GET': url+='?'+data.decode();data=None
    req=urllib.request.Request(url,data=data,method=method)
    with urllib.request.urlopen(req,timeout=45) as r: return json.loads(r.read())
container=request('POST',f'/{IG_ID}/media',{'media_type':'REELS','video_url':VIDEO_URL,'caption':CAPTION,'share_to_feed':'true'})
creation_id=container['id'];print('Created container:',creation_id)
for i in range(24):
    time.sleep(10)
    status=request('GET',f'/{creation_id}',{'fields':'status_code,status'})
    print('Status',status.get('status_code'))
    if status.get('status_code')=='FINISHED':break
    if status.get('status_code') in ('ERROR','EXPIRED'):raise RuntimeError(str(status))
else:raise TimeoutError('Video processing timed out; check status before retrying to avoid duplicates')
published=request('POST',f'/{IG_ID}/media_publish',{'creation_id':creation_id})
print('PUBLISHED',published['id'])
