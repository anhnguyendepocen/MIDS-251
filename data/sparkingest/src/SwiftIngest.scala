/* SwiftIngest.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.json4s.json4s


object SwiftIngest {
  def main(args: Array[String]) {
    val file = "swift://reddit2.sjc01/2007/*"
      val conf = new SparkConf().setAppName("Swift Ingest")
      val sc = new SparkContext(conf)
      val lines = sc.textFile(file)
      val comments = lines.map(x => )



  }
}