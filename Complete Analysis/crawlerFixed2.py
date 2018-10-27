from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2
import sys
import threading

DEVELOPER_KEY = "AIzaSyClserQ1cuNOX9SssQT6-BvBf65JZZ1Lk4"
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

def search(query,numOfResults,dataScaled):
    #res is the list of results
    res = []
    
    # Change search query to the required query by changing the first argument of this function
    threadLock.acquire()
    
    youtube_search(query, None,numOfResults,res)
    threadLock.release()
    
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
        if search_result['id']['videoId'] in dataScaled['videoId']:
            continue
        count += 1.0
        print threading.currentThread().getName()+' ' +str(100*(count/float(numOfResults)))[:4]+'%'
        title.append(search_result['snippet']['title']) 

        videoId.append(search_result['id']['videoId'])
        threadLock.acquire()

        response = youtube.videos().list(
        part='statistics, snippet',
        id=search_result['id']['videoId']).execute()
        threadLock.release()

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
            commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + search_result['id']['videoId'] + "&maxResults=50",timeout=60).read())
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
        # except ssl.SSLError:
        #     continue
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
    threadLock.acquire()
    data = json.load(open('crawlerResultScaledRem.json'))
    for keys in youtube_dict:
        data[keys] += youtube_dict[keys]
    with open('crawlerResultScaledRem.json', 'w') as fp:
        json.dump(data, fp)
    print threading.currentThread().getName()+' WRITING TO JSON FILE'
    threadLock.release()
    # with open('VideosPerChannel.json', 'w') as fp:
    #     json.dump(chan, fp)
threadLock=threading.Lock()
dataScaled = json.load(open('uniqueScaled.json'))

threading.Thread(name='1',target=search,args=('how to work the stock market',2500,dataScaled)).start()
threading.Thread(name='2',target=search,args=('how to start a business',2500,dataScaled)).start()
threading.Thread(name='3',target=search,args=('how to make money on facebook',2500,dataScaled)).start()
# threading.Thread(name='4',target=search,args=('easy advertising',2500,dataScaled)).start()
# threading.Thread(name='5',target=search,args=('easypaisa',2500,dataScaled)).start()
# threading.Thread(name='6',target=search,args=('photos to earn',2500,dataScaled)).start()
# threading.Thread(name='7',target=search,args=('blog for earning',2500,dataScaled)).start()
# threading.Thread(name='8',target=search,args=('adfly earn',2500,dataScaled)).start()
# threading.Thread(name='9',target=search,args=('url shortners to earn',2500,dataScaled)).start()












# threads=[]
# threading.Thread(name='1',target=search,args=('paytm',2500)).start()
# threading.Thread(name='2',target=search,args=('music cash app',2500)).start()
# threading.Thread(name='3',target=search,args=('sports money app',2500)).start()


# threading.Thread(name='1',target=search,args=('spending tracker',2500)).start()
# threading.Thread(name='2',target=search,args=('earn money from smartphones app',2500)).start()
# threading.Thread(name='3',target=search,args=('daily income online jobs without investment',2500)).start()
# threading.Thread(name='4',target=search,args=('neobux',2500)).start()
# threading.Thread(name='5',target=search,args=('dropshipping',2500)).start()
# threading.Thread(name='6',target=search,args=('payment proof',2500)).start()
# threading.Thread(name='7',target=search,args=('paypal automatic payments',2500)).start()
# threading.Thread(name='8',target=search,args=('bitcoin earning app',10)).start()
# threading.Thread(name='9',target=search,args=('passive income',10)).start()
# threading.Thread(name='10',target=search,args=('cost per click',10)).start()
# threading.Thread(name='11',target=search,args=('online surveys',10)).start()
# threading.Thread(name='12',target=search,args=('freelancing',10)).start()
# threading.Thread(name='13',target=search,args=('freelancing',10)).start()
# threading.Thread(name='14',target=search,args=('posting ads online for money',10)).start()
# threading.Thread(name='15',target=search,args=('paid to click',10)).start()
# threading.Thread(name='16',target=search,args=('click fraud',10)).start()












# search('earn money online',1000)
# search('admob easy money',1000)
# search('easy click money',1000)
# search('how to make easy money online',1000)
# search('earn online neobux',1000)
# search('self click for easy money',1000)
# search('android easy money making',1000)
# search('click on apps to make money',1000)

# search('make money through easy selling',100)
# search('make money through easy selling',1900)
# search('fortnite earn money',2000)
# search('game money',2000)
# search('affiliate marketing money',2000)
# search('earn easy money',2000)
# search('profit clicking',2000)

# search('earn money from home',100)

# search('earn money from home',1900)
# print "DONE",1
# search('online earning sites',2000)
# print "DONE",2

# search('money making apps',2000)
# print "DONE",3

# search('stock market fast money',2000)
# print "DONE",4


# search('earn cryptocurrency online',2000)
# print "DONE",6


# search('paypal earning',2000)
# print "DONE",9

# # search('online money scams',100)
# # print "DONE",10

# search('online money scams',1900)
# print "DONE",10

# search('easy money business',2000)
# print "DONE",11

# search('click on own app',2000)
# print "DONE",12

# search('admob vpn',2000)
# print "DONE",13

# search('earn money by watching ads',2000)
# print "DONE",14

# search('self click admob',2000)
# print "DONE",15

# search('adsense make money online',2000)
# print "DONE",16

# search('clixsense earn money',2000)
# print "DONE",17







