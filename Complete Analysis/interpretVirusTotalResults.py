import json
import csv

x = json.load(open('URL_VirusTotal_Results.json'))
f = csv.writer(open("URL_VirusTotal_Results.csv", "wb+"))
p = csv.writer(open("URL_VirusTotal_Positives.csv", "wb+"))

f.writerow(['URL',
			'Detected',
			'True/False Positive'
			])
p.writerow(['URL',
			'Detected',
			'True/False Positive'
			])

for list in x.values():
	for dictionary in list:
		try:
			malwareType={}
			for site in dictionary["scans"].keys():
				if dictionary["scans"][site]["detected"]==True:
					malwareType[site]=dictionary["scans"][site]["result"]
			if len(malwareType):
				if ('amazon.com' in dictionary["url"] or 'amzn.' in dictionary["url"]  or "adf.ly" in dictionary["url"]):
					p.writerow([
					dictionary["url"],
					malwareType,
					"False Positive"
					])
				else:
					p.writerow([
						dictionary["url"],
						malwareType,
						"True Positive"
						])
			f.writerow([
					dictionary["url"],
					malwareType
					])
		except Exception,e:
			if "scans" in str(e):
				print dictionary
				