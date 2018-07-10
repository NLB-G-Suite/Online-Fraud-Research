import crawlerFixed
import sys
import descriptionsTagsTitlesExtract
import ldaonTitlesDescriptionTags
import perVideoLDA
import uniqueChan


def main(argv):
	query = argv[1]
	nres = argv[2]
	crawlerFixed.search(query, nres)
	descriptionsTagsTitlesExtract.makeDict()
	ldaonTitlesDescriptionTags.runLda()
	perVideoLDA.checkKeywords()
	uniqueChan.findPercentage()

if __name__ == "__main__":
  main(sys.argv)
