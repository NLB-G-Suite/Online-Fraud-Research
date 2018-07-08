from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2

DEVELOPER_KEY = "AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Authorization for using the Youtube API v3
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def youtube_search(q, token, res, max_results=50,order="relevance",  location=None, location_radius=None):
    # change res to number of results required
    if len(res) >= 900:
        return

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",  
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    for search_result in search_response.get("items", []):
    	res.append(search_result)
        
    youtube_search("make money through clicking", search_response.get("nextPageToken"), res)

if __name__=="__main__":
    #res is the list of results
    res = []
    
    # Change search query to the required query by changing the first argument of this function
    youtube_search("make money through clicking", None,res)
    
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    commentCount = []
    category = []
    videos = []
    comments = []
    tags = []
    description = []

    chan = {}

    count = 0.0
    for search_result in res:
        count += 1.0
        print str(100*(count/900.0))[:4]+'%'
        title.append(search_result['snippet']['title']) 

        videoId.append(search_result['id']['videoId'])

        response = youtube.videos().list(
        part='statistics, snippet',
        id=search_result['id']['videoId']).execute()

        try:
            channelId.append(response['items'][0]['snippet']['channelId'])
        except:
            channelId.append('No channelId')
        try:
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
        except:
            channelTitle.append('No channelTitle')
        try:
            categoryId.append(response['items'][0]['snippet']['categoryId'])
        except:
            categoryId.append('No categoryId')
        try:
            viewCount.append(response['items'][0]['statistics']['viewCount'])
        except:
            viewCount.append('No viewCount')
        try:
            tags.append(response['items'][0]['snippet']['tags'])
        except:
            tags.append('No tags')
        try:
            description.append(response['items'][0]['snippet']['description'])
        except:
            description.append('No description')
        try:
            commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + search_result['id']['videoId'] + "&maxResults=50").read())
            # chanVids = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&channelId="+response['items'][0]['snippet']['channelId']+"&part=snippet,id&order=date&maxResults=50").read())

            # d = []
            # for k in range(len(chanVids['items'])):
            #     if 'videoId' in chanVids['items'][k]['id']:
            #         d.append('https://www.youtube.com/watch?v='+chanVids['items'][k]['id']['videoId'])
            # if response['items'][0]['snippet']['channelId'] not in chan:
            #     chan[response['items'][0]['snippet']['channelId']] = d

            c = []
            for k in range(len(commentsOnVideo['items'])):
                c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
            comments.append(c)
        except:
            comments = []
        try:
            if 'commentCount' in response['items'][0]['statistics'].keys():
                commentCount.append(response['items'][0]['statistics']['commentCount'])
            else:
                commentCount.append([])
        except:
            commentCount.append([])
    youtube_dict = {'description': description, 'tags': tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'commentCount':commentCount, 'comments': comments}

    with open('buffer.json', 'w') as fp:
        json.dump(youtube_dict, fp)
   
    # with open('VideosPerChannel.json', 'w') as fp:
    #     json.dump(chan, fp)
