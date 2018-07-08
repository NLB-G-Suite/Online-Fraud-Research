from crawlerFixed import search
import sys

def main(argv):
  query = argv[0]
  nres = argv[1]
  search(query, nres)

if __name__ == "__main__":
  main(sys.argv)
