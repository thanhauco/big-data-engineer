package com.example

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

object BigDataEngineerSpark {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("BigDataEngineerETL")
      .master("local[*]")
      .getOrCreate()

    val rawDf = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv("data/raw/telemetry.csv")

    val enrichedDf = rawDf
      .withColumn("date_partition", to_date(col("event_ts")))
      .withColumn("amount", col("amount").cast("decimal(18,2)"))
      .filter(col("amount").isNotNull)

    val summary = enrichedDf
      .groupBy("date_partition", "region")
      .agg(sum("amount").as("total_revenue"), countDistinct("order_id").as("orders"))

    summary.show(false)

    spark.stop()
  }
}
