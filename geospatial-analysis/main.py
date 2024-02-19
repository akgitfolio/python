from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans


spark = SparkSession.builder.appName("Geospatial Analysis").getOrCreate()


data_path = "path/to/synthetic_data.csv"
synthetic_data = spark.read.csv(data_path, header=True, inferSchema=True)


synthetic_data.show(5)


assembler = VectorAssembler(inputCols=["latitude", "longitude"], outputCol="features")
feature_vector = assembler.transform(synthetic_data)


kmeans = KMeans(featuresCol="features", k=5)
model = kmeans.fit(feature_vector)


clustered_data = model.transform(feature_vector)


clustered_data.select("latitude", "longitude", "prediction").show(5)


spark.stop()
