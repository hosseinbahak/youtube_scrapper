import os
from typing import KeysView
from unittest import result
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
import xlsxwriter

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
   
    ## we can put keyword and count of results we need here to search it in youtube videos, channels and playlists ##
    serach_keyword = "language learning"
    count_of_results_times_50 = 2   #50*2
    results = []

    #initializing xlsx file
    file_name = "YouTubeScrapper_" + serach_keyword + ".xlsx"
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'channelName')
    worksheet.write('B1', 'subscriberCount')
    worksheet.write('C1', 'viewCount')
    worksheet.write('D1', 'channel_url')


    ###we can return 50 result item per request cause of youtube limitations
    for i in range(count_of_results_times_50):   
        request = youtube.search().list(
            part="snippet",
            maxResults = 50,
            q = serach_keyword
        )

        nextPageToken = request.execute()['nextPageToken']
        results =  results + request.execute()['items'] 
        
    

    loaded_r = json.loads(json.dumps(results))
    
    number_of_results = len(loaded_r)
    channels = []

    for i in range(number_of_results):
        channel_id = loaded_r[i]['snippet']['channelId']
        request = youtube.channels().list(
            part="snippet, statistics",
            id = channel_id
        )
        
        channelResult = request.execute()
        channelResult = json.dumps(channelResult)
        loaded_channel_detail = json.loads(channelResult)
        
        channel_detail = loaded_channel_detail['items'][0]['statistics']
        channel_detail['channelName'] = loaded_channel_detail['items'][0]['snippet']['title']
        #add channel url to exist dictionary 
        channel_detail["channel_url"] = "https://www.youtube.com/channel/" + channel_id
        
        #worksheet.write(row, column, text) 
        worksheet.write(i+1, 0, channel_detail['channelName'])
        worksheet.write(i+1, 1, channel_detail['subscriberCount'])
        worksheet.write(i+1, 2, channel_detail['viewCount'])
        worksheet.write(i+1, 3, channel_detail['channel_url'])

    workbook.close()    
        
   

if __name__ == "__main__":
    main()