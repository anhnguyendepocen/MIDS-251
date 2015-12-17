import re
import glob
from datetime import datetime
from dateutil import parser
import pickle
import sys

if len(sys.argv) > 1:
    year = sys.argv[1]
else:
    print "Need the year for the directory"
    sys.exit(1)

sr_tuple = re.compile(r'^\({2}([^,]*),([^,]*)\),([0-9]*)')

fn = "/Users/rcordell/Development/MIDS-251/data/{0}/subreddit_counts/part-0*".format(year)
part_files = glob.glob(fn)
total_files = len(part_files)

print "Processing {0} files...\n".format(len(part_files))

subreddits = {}

for j,f in enumerate(part_files):
    with open(f,"r") as infile:
        for i, line in enumerate(infile):
            print "{0:5d}/{1:5d} : {2:5d} \r".format(j,total_files,i),
            match = sr_tuple.match(line)
            if match:
#                subreddit = match.group(1)
                dt = parser.parse(match.group(2))
#                count = int(match.group(3))

                if dt not in subreddits:
                    subreddits[dt]=int(match.group(3))
                else:
                    subreddits[dt]+=int(match.group(3))

# save the postings
fp = "/Users/rcordell/Development/MIDS-251/data/{0}/subredditsperminute.pkl".format(year)
with open(fp, 'wb') as of:
    pickle.dump(subreddits, of, -1)
