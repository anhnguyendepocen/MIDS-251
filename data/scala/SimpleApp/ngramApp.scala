import org.apache.spark.sql.SQLContext
import org.apache.spark.{SparkConf, SparkContext}
import org.joda.time.DateTime
import org.apache.spark.ml.feature.NGram
import org.apache.spark.sql.functions._

object ngramApp {
  def main(args: Array[String]) {
//    val year = "2008"
    val year = args(0)
    val file = "swift://reddit2.sjc01/" + year + "/*"
//    val file = "/Volumes/Drobo1/reddit_data/reddit_data/2007/RC_2007-10"
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)
    val df = sqlContext.read.json(file)

    val ngram = new NGram().setInputCol("bodyarr").setOutputCol("ngrams")

      val df2 = df.withColumn("bodyarr", split(col("body"), "\\s+"))

      ngramDF = ngram.transform(df2)

      val ngram_counts = ngramDF.select("ngrams").map(row => row.toString)

    val ngramDF = ngram.transform(df)

    val regex = "[^a-zA-Z0-9]".r

    val word_counts = df.select("body").flatMap(row => row.toString.split("\\s+"))
        .map(word => regex.replaceAllIn(word.trim.toLowerCase, ""))
        .filter(word => !word.isEmpty)
        .map(word => (word, 1))
        .reduceByKey(_ + _)

    authorperhour.saveAsTextFile("hdfs://master/user/" + year + "authorperhour_counts")
    authorperdaypersubreddit.saveAsTextFile("hdfs://master/user/" + "year" + "authorperdaypersubbreddit_counts")
    subreddit.saveAsTextFile("hdfs://master/user/" + year + "subreddit_counts")

    created_time.saveAsTextFile("hdfs://master/user/" + year + "time_counts")

    word_counts.saveAsTextFile("hdfs://master/user/" + year + "counts_all")

  }
}
