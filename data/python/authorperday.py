import re
import glob
from datetime import datetime
import pickle
import cPickle
import sys
from dateutil import parser

# Time Format 2014-04-16T00:00:00.000-05:00


if len(sys.argv) > 1:
	year = sys.argv[1]
else:
	print "Need the year for the directory"
	sys.exit(1)

auth_tuple = re.compile(r'^\(\(([^,]*),([^,]*),([^\)]*)\),([0-9]*)')

#year = "2015"
fn = "/Users/rcordell/Development/MIDS-251/data/{0}/authorperday_counts/part-0*".format(year)
part_files = glob.glob(fn)

# split the list into 100 files each
chunks=[part_files[x:x+100] for x in xrange(0, len(part_files), 100)]

n = 0
for k, chunk in enumerate(chunks):
    subreddits = {}
    hour = {}
    total_files = len(chunk)
    for j,f in enumerate(chunk):
        with open(f,"r") as infile:
            for i, line in enumerate(infile):
                print "{0:3}:{1:5}  {2:5d}/{3:5d} : {4:5d} \r".format(k, len(chunks), j+1, total_files,i),
                match = auth_tuple.match(line)
                if match:
                    author = match.group(2)
                    subreddit = match.group(1)
                    dt = datetime.strptime(match.group(3).split('T')[0], "%Y-%m-%d")
 #                   dt = parser.parse(match.group(3))
                    count = int(match.group(4))
                    if dt not in hour:
                        hour[dt]={subreddit: {author: count}}
                    elif subreddit not in hour[dt]:
                        hour[dt][subreddit]= {author: count}
                    elif author not in hour[dt][subreddit]:
                        hour[dt][subreddit][author] = count
                    else:
                        hour[dt][subreddit][author] += count
                    if dt not in subreddits:
                        subreddits[dt]=count
                    else:
                        subreddits[dt]+=count

    # save the postings
    fp = "/Users/rcordell/Development/MIDS-251/data/{0}/authorperday_{1}.pkl".format(year,n)
    with open(fp, 'wb') as of:
        cPickle.dump(hour, of, -1)


    # save the postings
    fp = "/Users/rcordell/Development/MIDS-251/data/{0}/subredditsperday_{1}.pkl".format(year,n)
    with open(fp, 'wb') as of:
        cPickle.dump(subreddits, of, -1)

    n+=1
