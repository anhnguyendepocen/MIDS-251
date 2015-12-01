name := "sparkingest"

version := "1.0"

scalaVersion := "2.10.6"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "1.5.2",
  "org.apache.spark" %% "spark-sql" % "1.5.2",
  "org.json4s" %% "json4s-native" % "3.3.0"
)

resolvers += "Akka Repository" at "http://repo.akka.io/releases"
    