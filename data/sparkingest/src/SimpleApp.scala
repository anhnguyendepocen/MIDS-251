/**
  * Created by rcordell on 11/29/15.
  */
/* SimpleApp.scala */
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SQLContext


object SimpleApp {
  def main(args: Array[String]) {
    val file = "swift://reddit2.sjc01/2007/*" // Should be some file on your system
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)
    val df = sqlContext.read.json(file)

    df.registerTempTable("comments")

    println("========== Number of comments processed: %s".format(df.count()))
    val comments = sqlContext.sql("SELECT body FROM comments").collect()
    val commentCount = sqlContext.sql("SELECT COUNT(*) FROM comments").collect().head.getLong(0)
    println("========== Comment Count from SQL SELECT :%s".format(commentCount))

    val body = comments.map(row => row.getAs[String](fieldName = "body"))

    val words = body.flatMap(content => content.toString.split(" "))
                    .map(word => (word, 1))
                    .reduceByKey(_ + _)

    words.sortBy(_._2, false).take(25)
      .foreach{ case (word, count) => println("\n %s \t\t Count: %s".format(word, count)) }

  }
}