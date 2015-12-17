import glob
import pickle

data = {}
for year in range(2012,2013):
	fn = "/Users/rcordell/Development/MIDS-251/data/{0}/authorperday_?.pkl".format(year)
		
	part_files = glob.glob(fn)
	if len(part_files) == 0:
		fn = "/Users/rcordell/Development/MIDS-251/data/{0}/authorperday.pkl".format(year)
		part_files = glob.glob(fn)
	print len(part_files)
	for i, pkl in enumerate(part_files):
		with open(pkl, 'rb') as pkl_file:
			print "{0:5d}:{1:5d}".format(year, i),
			data.update(pickle.load(pkl_file))

print len(data)

	





'''
    for j,f in enumerate(chunk):
        with open(f,"r") as infile:
            for i, line in enumerate(infile):
                print "{0:3}:{1:5}  {2:5d}/{3:5d} : {4:5d} \r".format(k, len(chunks), j+1, total_files,i),
                match = auth_tuple.match(line)
                if match:
                    author = match.group(2)
                    subreddit = match.group(1)
                    dt = parser.parse(match.group(3))
                    count = int(match.group(4))
                    if dt not in hour:
                        hour[dt]={subreddit: {author: count}}
                    elif subreddit not in hour[dt]:
                        hour[dt][subreddit]= {author: count}
                    elif author not in hour[dt][subreddit]:
                        hour[dt][subreddit][author] = count
'''