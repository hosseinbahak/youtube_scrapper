# https://developers.google.com/explorer-help/code-samples#python
import os
from typing import KeysView
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        part="snippet",
        maxResults=2,
        q="english language"
    )
 
    r = request.execute()
    r = json.dumps(r)
    loaded_r = json.loads(r)


    channel_id = loaded_r['items'][0]['snippet']['channelId']
    
    request2 = youtube.channels().list(
        part="statistics",
        id = channel_id
    )
    

    rs = request2.execute()
    rs = json.dumps(rs)
    loaded_r2 = json.loads(rs)
    
    channel_details = loaded_r2['items'][0]['statistics']

    channel_details["channel_url"] = "https://www.youtube.com/channel/" + channel_id

    print(channel_details)
   
    

if __name__ == "__main__":
    main()