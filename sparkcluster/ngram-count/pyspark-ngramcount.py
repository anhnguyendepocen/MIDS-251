import sys
import json
from operator import add
from pyspark import SparkContext
​
def line_to_words (line): # return a list of words
    line = line.encode('utf-8')
    return line.split(' ') # this will work for most text, probably want to do more here but this is the idea
​
def word_to_ngrams (word):
    # Bigrams
    #ngrams = zip(word, word[1:])
    # Trigrams
    ngrams = zip(word, word[1:], word[2:])
    # Fourgrams
    #zip(word, word[1:], word[2:], word[3:])
    return ngrams
​
def line_to_ngrams(line):
    ngrams = []
    for word in line_to_words(line):
        ngrams += word_to_ngrams(word)
    return ngrams
​
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: ngramcount <input file or directory> <output directory>"
        exit(-1)
    indir = sys.argv[1]
    outdir = sys.argv[2]
    sc = SparkContext(appName="NgramCount")
​
    # Required to allow spark to recursively read an hdfs directory
    hadoopConf=sc._jsc.hadoopConfiguration()
    hadoopConf.set("mapreduce.input.fileinputformat.input.dir.recursive","true")
​
    lines = sc.textFile(indir, 1)
    counts = lines.flatMap(lambda x: line_to_ngrams(x)) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
​
    # to look at the output for smaller jobs:
    output = counts.collect() # this converts rdd to python list
    for (word, count) in output:
        print "%s: %i" % (word, count)
​
    # for bigger jobs use rdd.saveAsTextFile("outputdirectory") to write output to hdfs
    counts.saveAsTextFile(outdir)
​
    sc.stop()
