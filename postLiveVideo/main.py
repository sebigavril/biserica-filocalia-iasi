from youtube import client as y_client
from youtube import archive
from youtube import privacy
from youtube import stream

from facebook import client as f_client

y_client = y_client.get_authenticated_service()

archive.archive_last_live_event(y_client)
privacy.make_archive_private(y_client)

if stream.is_stream_live(y_client):
     f_client.postLiveStream()



# import schedule
# schedule.every().day.at("10:00").do(make_archive_private, client)
# schedule.every().minute.do(archive_last_live_event, client)
#
# while True:
#     schedule.run_pending()
#     time.sleep(30)



