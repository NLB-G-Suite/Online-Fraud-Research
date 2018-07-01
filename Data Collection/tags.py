def main():
  tags = []
  
  # get video IDs
  
  for id in videos:
    results = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + id + "&type=video&key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74").read())
    tags.append(results["tags"])
    
if __name__ == "__main__":
  main()
