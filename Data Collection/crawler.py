from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2

DEVELOPER_KEY = "AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def youtube_search(q, token, res, max_results=50,order="relevance",  location=None, location_radius=None):
    if len(res) >= 200:
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
    youtube_search("tutorial", search_response.get("nextPageToken"), res)


if __name__ == "__main__":
    res = []
    youtube_search("tutorial", None,res)
    
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

    for search_result in res:
        title.append(search_result['snippet']['title']) 

        videoId.append(search_result['id']['videoId'])

        response = youtube.videos().list(
        part='statistics, snippet',
        id=search_result['id']['videoId']).execute()

        channelId.append(response['items'][0]['snippet']['channelId'])
        channelTitle.append(response['items'][0]['snippet']['channelTitle'])
        categoryId.append(response['items'][0]['snippet']['categoryId'])
        viewCount.append(response['items'][0]['statistics']['viewCount'])
        
        try:
            commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + search_result['id']['videoId'] + "&maxResults=50").read())
            c = []
            for k in range(len(commentsOnVideo['items'])):
                c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
            comments.append(c)
        except:
            print 'error'
        
        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])
        else:
            commentCount.append([])
    youtube_dict = {'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'commentCount':commentCount, 'comments': comments}

    with open('data1.json', 'w') as fp:
        json.dump(youtube_dict, fp)
