from pyspark import SparkContext, SparkConf
import json

# Module Constants
APP_NAME = "Reddit Comment Analysis"
REDDIT_FILES = "swift://reddit2.sjc01/*/*"

if __name__ == "__main__":
    
    # Configure Spark
    conf = SparkConf().setMaster("spark://master:7077")
    conf = conf.setAppName(APP_NAME)
    sc = SparkContext(conf=conf)

    # execute the work we want to do with Spark
    comments = sc.textFile(REDDIT_FILES).map(lambda line: json.loads(line))
    words = comments.flatMap(lambda comment: comment['body'].split(" "))
    counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b: a + b)
    counts.saveAsTextFile("hdfs://master/usr/hadoop/word_counts")
    sc.stop()
