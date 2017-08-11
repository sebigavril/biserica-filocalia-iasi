import os
import subprocess

import facebook
import youtube

nginxConfigFile = os.environ.get("FILOCALIA_NGINX_CONFIG_FILE")
if nginxConfigFile is None:
    raise Exception("No env variable FILOCALIA_NGINX_CONFIG_FILE found!")

facebookStreamUrl = facebook.getStreamUrl()
youtubeStreamUrl = youtube.getStreamUrl()

print "Facebook Stream: " + facebookStreamUrl
print "Youtube Stream: " + youtubeStreamUrl

subprocess.call(["nginx", "-s", "stop"])

f = open("nginx.conf.default","r")
filedata = f.read()
f.close()

newdata = filedata.replace("FILOCALIA_FB_STREAM_URL", facebookStreamUrl).replace("FILOCALIA_YT_STREAM_URL", youtubeStreamUrl)

f = open(str(nginxConfigFile),"w")
f.write(newdata)
f.close()

subprocess.call(["nginx"])
