import sys, json, urllib.request, time
sys.path.insert(0,'/app'); import fal_client
vid,aud,out=sys.argv[1],sys.argv[2],sys.argv[3]
vu=fal_client.upload_file(vid); au=fal_client.upload_file(aud)
t0=time.time()
r=fal_client.subscribe('fal-ai/latentsync', arguments={'video_url':vu,'audio_url':au,'guidance_scale':1.5,'loop_mode':'pingpong'})
u=(r.get('video') or {}).get('url') if isinstance(r.get('video'),dict) else r.get('video')
print('czas %.0fs'%(time.time()-t0), '| resp:', json.dumps(r)[:200])
urllib.request.urlretrieve(u,out); print('OK',out)
