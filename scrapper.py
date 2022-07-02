# https://developers.google.com/explorer-help/code-samples#python
import os
from typing import KeysView
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
import csv


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
   
    ## we can put keyword here to search it in youtube videos, channels and playlists ##
    serach_keyword = "language learning"
    
    request = youtube.search().list(
        part="snippet",
        ## results limitation ##
        maxResults = 50,
        q = serach_keyword
    )
    
    nextPageToken = request.execute()['nextPageToken']
    nextPage = youtube.search().list(
        q = serach_keyword,
        part='snippet',
        maxResults=100,
        pageToken=nextPageToken
        ).execute()
    
    request.execute()['items'] += nextPage['items']

    print(nextPageToken)
    
    ###we can return 100 result item or all of youtube results (request per day got limited by google we have to limit requests)
    """""
    while (nextPageToken):
        nextPage = youtube.search().list(
        q = serach_keyword,
        part='snippet',
        maxResults=100,
        pageToken=nextPageToken
        ).execute()
        request.execute()['items'] = request.execute()['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            request.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']
    """

    r = request.execute()
    r = json.dumps(r)
    loaded_r = json.loads(r)

    print(len(loaded_r['items']))
    
    number_of_results = len(loaded_r['items'])
    channels = []
    
    for i in range(number_of_results):
        channel_id = loaded_r['items'][i]['snippet']['channelId']
        request2 = youtube.channels().list(
            part="statistics",
            id = channel_id
        )
        
        rs = request2.execute()
        rs = json.dumps(rs)
        loaded_r2 = json.loads(rs)
        channel_details = loaded_r2['items'][0]['statistics']

        #add channel url to exist dictionary 
        channel_details["channel_url"] = "https://www.youtube.com/channel/" + channel_id
        channels.append(channel_details)
        
    print(json.dumps(channels))
   

    #Save results to csv#
    file = "YouTubeScrapper_" + serach_keyword + ".csv"


    def writeCSV(results, filename):
        
        keys = sorted(results.keys())
        with open(filename, "w", newline="", encoding="utf-8") as output:
            writer = csv.writer(output, delimiter=",")
            writer.writerow(keys)


    writeCSV(channels, file)
    print("_-_-_CSV file has been created_-_-_" )


if __name__ == "__main__":
    main()