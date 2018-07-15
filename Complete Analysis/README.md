# Online-Frauds-Research
========================= Project Overview =========================

The purpose of each file in this repository is as follows:
1. crawlerFixed.py: Running this program will create a json file namely crawlerResults.json which contains information about the videos returned by a search query specified in the file. The information includes title of file, video ID, comments on the video,descriptions of the video and tags etc.It also creates VideosPerChannel.json which stores the videos returned by search query against their channels.

2. linkAnalysis.py: This file is used to extract links from the description and distinguish between the links that are up and down, classifies the videos from crawler results into benign and fraudulent and stores the categories of each video. This is added in the json generated from crawler.

3. json2csv.py: A Csv file of the json compiled above is generated.

4. descriptionsTagsTitlesExtract.py: It parses VideosPerChannel.json to extract all videos uploaded by the potential fraud channels identified from crawlerResults. It stores the videos with their titles,descriptions and tags in tagsDescriptionsTitleChannel.json

5. ldaonTitlesDescriptionTags.py: Runs lda on titles and descriptions stored in tagsDescriptionsTitleChannel.json

6. fraudUserGenerator.py: Matches lda results generated on titles and descriptions, and tags against a set of keywords to identify channels dominated by potentially fraudulent videos. Stores channels identified through titles,tags and descriptions seperately in ldaOn_ad_clickTitles.json,ldaOn_ad_clickTag.json,ldaOn_ad_clickDescription.json respectively.

7. uniqueChan.py: From all json files generated above identifies unique potentially fraud channels.It extracts videos from those channels which has sensitive words and stores the frequency of keywords occuring in titles,tags and descriptions respectively. Displays results in FraudChannels.csv. 
It also generates PercentageFraudChannel.csv which displays total videos from a potential fraud channel,the number of fraud videos in channel and percentage of fraud videos. 