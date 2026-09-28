import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import java.nio.file.{Files, Paths}
import java.nio.charset.StandardCharsets

object OneHealthPreprocessing {

  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder()
      .appName("OneHealth Nexus Preprocessing")
      .master("local[*]")
      .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    val inputPath = "data/processed/cleaned_documents.csv"
    val outputPath = "data/processed/spark_output"

    println("======================================")
    println("      ONEHEALTH NEXUS - SPARK")
    println("======================================")

    // Read dataset
    val df = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(inputPath)

    println("\nInput records:")
    println(df.count())

    println("\nInput columns:")
    df.columns.foreach(println)

    // Spark preprocessing
    val cleanedDF = df
      .filter(col("clean_text").isNotNull)
      .filter(length(trim(col("clean_text"))) > 0)
      .dropDuplicates("clean_text")

    println("\nRecords after Spark preprocessing:")
    println(cleanedDF.count())

    println("\nSample processed records:")
    cleanedDF.show(10, truncate = false)

    // Collect small final result and save using normal file I/O
    val result = cleanedDF
      .select("document_id", "source", "date", "clean_text")
      .collect()

    val outputDir = Paths.get(outputPath)

    if (!Files.exists(outputDir)) {
      Files.createDirectories(outputDir)
    }

    val outputFile = outputDir.resolve("processed_documents.txt")

    val header = "document_id\tsource\tdate\tclean_text\n"

    val body = result.map { row =>
      val id = Option(row.getAs[Any]("document_id")).map(_.toString).getOrElse("")
      val source = Option(row.getAs[Any]("source")).map(_.toString).getOrElse("")
      val date = Option(row.getAs[Any]("date")).map(_.toString).getOrElse("")
      val text = Option(row.getAs[Any]("clean_text")).map(_.toString).getOrElse("")
        .replace("\n", " ")
        .replace("\r", " ")

      s"$id\t$source\t$date\t$text"
    }.mkString("\n")

    Files.write(
      outputFile,
      (header + body).getBytes(StandardCharsets.UTF_8)
    )

    println("\n======================================")
    println("Spark preprocessing completed!")
    println("======================================")
    println(s"Output saved to: $outputFile")
    println(s"Final records: ${result.length}")

    spark.stop()
  }
}