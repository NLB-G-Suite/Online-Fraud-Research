import crawlerFixed
import sys
import json2csv
import linkAnalysis
import uniqueChan
import fraudUserGenerator
import virusTotalScan
import virusTotalImport
import ldaperVideo
import sampleClassifier

def main(argv):
	# query = argv[1]
	# nres = argv[2]
	# print nres
	# print "Running crawler.."
	# crawlerFixed.search(query, nres)
	# print "Exiting crawler.. Starting Link Analysis.."
	# linkAnalysis.linkWork(nres)
	# print "Ending Link Analysis.. Sending links to virusTotal.."
	# virusTotalScan.scan()
	print 'Getting VirusTotal Results..'
	virusTotalImport.getResults()
	print 'VirusTotal Results Retrieved, running LDA on descriptions..'
	ldaperVideo.ldaDesc()
	print 'All data collected, running classifier'
	sampleClassifier.findPercentage()
	print 'All videos classified, creating CSV file..'
	json2csv.csvConvert()
	print 'Success!'
	# print "Starting LDA Analysis per Channel.."
	# descriptionsTagsTitlesExtract.makeDict()
	# ldaonTitlesDescriptionTags.runLda()
	# fraudUserGenerator.potentialFraud()
	# print 'Ending LDA.. Identifying unique channels..'
	# uniqueChan.findPercentage()
	# print "DONE"

if __name__ == "__main__":
  main(sys.argv)
