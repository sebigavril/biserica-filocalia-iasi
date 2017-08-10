import subprocess

import youtube
import facebook

facebookStreamUrl = facebook.getStreamUrl()
youtubeStreamUrl = youtube.getStreamUrl()

print "Facebook Stream: " + facebookStreamUrl
print "Youtube Stream: " + youtubeStreamUrl

f = open("nginx.conf.default","r")
filedata = f.read()
f.close()

newdata = filedata.replace("FILOCALIA_FB_STREAM_URL", facebookStreamUrl).replace("FILOCALIA_YT_STREAM_URL", youtubeStreamUrl)

# todo extract file name
filename = "/usr/local/etc/nginx/nginx.conf"
f = open(filename,"w")
f.write(newdata)
f.close()

subprocess.call(["nginx", "-s", "stop"])
subprocess.call(["nginx"])
