name := "sparkingest"

version := "1.0"

scalaVersion := "2.10.6"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "1.5.2",
  "org.apache.spark" %% "spark-sql" % "1.5.2",
  "org.apache.spark" %% "spark-mllib" % "1.5.2",
  "joda-time" % "joda-time" % "2.9.1",
  "org.joda" % "joda-convert" % "1.8.1"
)

resolvers += "Akka Repository" at "http://repo.akka.io/releases"

