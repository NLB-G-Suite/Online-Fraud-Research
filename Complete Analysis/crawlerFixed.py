from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2
import sys

DEVELOPER_KEY = "AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Authorization for using the Youtube API v3
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

sys.setrecursionlimit(11000)

def youtube_search(q, token,numOfResults, res,order="relevance",  location=None, location_radius=None):
    # change res to number of results required
    if len(res) >= int(numOfResults):
        return

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    location=location,
    locationRadius=location_radius).execute()

    for search_result in search_response.get("items", []):
    	res.append(search_result)
        
    youtube_search(q, search_response.get("nextPageToken"), numOfResults, res)

def search(query,numOfResults):
    #res is the list of results
    res = []
    
    # Change search query to the required query by changing the first argument of this function
    youtube_search(query, None,numOfResults,res)
    
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
    print len(res)
    count = 0.0
    for search_result in res:
        count += 1.0
        print str(100*(count/float(numOfResults)))[:4]+'%'
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
            comments.append('No comments')
        try:
            if 'commentCount' in response['items'][0]['statistics'].keys():
                commentCount.append(response['items'][0]['statistics']['commentCount'])
            else:
                commentCount.append("No commentCount")
        except:
            commentCount.append("No commentCount")
    youtube_dict = {'description': description, 'tags': tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'commentCount':commentCount, 'comments': comments}

    data = json.load(open('crawlerResult.json'))
    for keys in youtube_dict:
        data[keys] += youtube_dict[keys]
    with open('crawlerResult.json', 'w') as fp:
        json.dump(data, fp)
   
    # with open('VideosPerChannel.json', 'w') as fp:
    #     json.dump(chan, fp)

# search('earn money online',1000)
# search('admob easy money',1000)
# search('easy click money',1000)
# search('how to make easy money online',1000)
# search('earn online neobux',1000)
# search('self click for easy money',1000)
# search('android easy money making',1000)
search('click on apps to make money',1000)





