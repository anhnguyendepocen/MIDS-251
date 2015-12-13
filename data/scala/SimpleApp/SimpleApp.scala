import org.apache.spark.sql.SQLContext
import org.apache.spark.{SparkConf, SparkContext}
import org.joda.time.DateTime

object SimpleApp {
  def main(args: Array[String]) {
//    val year = "2008"
    val year = args(0)
    val file = "swift://reddit2.sjc01/" + year + "/*"
//    val file = "/Volumes/Drobo1/reddit_data/reddit_data/2007/RC_2007-10"
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)
    val df = sqlContext.read.json(file)

    val created_time = df.select("created_utc").map(row => (new DateTime(row.getString(0).toLong*1000)
                  .withSecondOfMinute(0)
                  .withMillisOfSecond(0), 1))
                  .reduceByKey(_ + _)

    val subreddit = df.select("subreddit", "created_utc")
        .map(row => ((row.getAs[String]("subreddit"), (new DateTime(row.getAs[String]("created_utc").toLong*1000))
        .withSecondOfMinute(0).withMillisOfSecond(0)), 1))
        .reduceByKey(_ + _)

    val authorperhour = df.select("author", "created_utc")
        .map(row => ((row.getAs[String]("subreddit"), (new DateTime(row.getAs[String]("created_utc").toLong*1000))
        .withMinuteOfHour(0).withSecondOfMinute(0).withMillisOfSecond(0)), 1))
        .reduceByKey(_ + _)

    val authorperdaypersubreddit = df.select("author", "subreddit", "created_utc")
        .map(row => ((row.getAs[String]("subreddit"),
                    row.getAs[String]("author"),
                    new DateTime(row.getAs[String]("created_utc").toLong*1000)
                    .withHourOfDay(0).withMinuteOfHour(0).withSecondOfMinute(0).withMillisOfSecond(0)),
                    1))
        .reduceByKey(_ + _)

    val word_counts = df.select("body").flatMap(row => row.toString.split(" "))
        .map(word => (word.trim, 1))
        .reduceByKey(_ + _)

    authorperhour.saveAsTextFile("hdfs://master/user/" + year + "authorperhour_counts")
    authorperdaypersubreddit.saveAsTextFile("hdfs://master/user/" + "year" + "authorperdaypersubbreddit_counts")
    subreddit.saveAsTextFile("hdfs://master/user/" + year + "subreddit_counts")

    created_time.saveAsTextFile("hdfs://master/user/" + year + "time_counts")

    word_counts.saveAsTextFile("hdfs://master/user/" + year + "counts_all")

  }
}