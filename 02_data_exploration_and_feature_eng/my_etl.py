import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import Imputer
from pyspark.ml import Pipeline
from pyspark.sql.types import FloatType

def csv_line(data):
    r = ','.join(str(d) for d in data[1])
    return str(data[0]) + "," + r

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'bucket'])

windturbine_rawdata = glueContext.create_dynamic_frame.from_catalog(
    database="endtoendml-db", table_name="data")

df = windturbine_rawdata.toDF()
df = df.na.replace('', "HAWT", subset=["turbine_type"])

df = df.withColumn("wind_speed", df["wind_speed"].cast(FloatType()))
df = df.withColumn("RPM_blade", df["RPM_blade"].cast(FloatType()))
df = df.withColumn("col4float", df["col4float"].cast(FloatType()))
df = df.withColumn("oil_level", df["oil_level"].cast(FloatType()))
df = df.withColumn("temperature", df["temperature"].cast(FloatType()))
df = df.withColumn("humidity", df["humidity"].cast(FloatType()))
df = df.withColumn("vibrations_frequency", df["vibrations_frequency"].cast(FloatType()))
df = df.withColumn("pressure", df["pressure"].cast(FloatType()))

col0_indexer = StringIndexer(inputCol="turbine_id", outputCol="indexed_turbine_id")
col1_indexer = StringIndexer(inputCol="turbine_type", outputCol="indexed_turbine_type")
col10_indexer = StringIndexer(inputCol="wind_direction", outputCol="indexed_wind_direction")
col11_indexer = StringIndexer(inputCol="breakdown", outputCol="indexed_breakdown")

turbine_id_encoder = OneHotEncoder(inputCol="indexed_turbine_id", outputCol="turb_id").setDropLast(False)
turbine_type_encoder = OneHotEncoder(inputCol="indexed_turbine_type", outputCol="turb_type").setDropLast(False)
wind_direction_encoder = OneHotEncoder(inputCol="indexed_wind_direction", outputCol="wind_dir").setDropLast(False)

col4_imputer = Imputer(inputCols=["col4float"], outputCols=["oil_temp"], strategy="median")

pipeline = Pipeline(stages=[col0_indexer, col1_indexer, col10_indexer, col11_indexer, turbine_id_encoder, turbine_type_encoder, wind_direction_encoder, col4_imputer])

model = pipeline.fit(df)
df = model.transform(df)

df = df.withColumnRenamed("indexed_breakdown", "break_down")

assembler = VectorAssembler(inputCols=['turb_id', 'turb_type', 'wind_speed', 'RPM_blade', 'oil_temp', 'oil_level','temperature', 
              'humidity', 'vibrations_frequency', 'pressure', 'wind_dir'], outputCol="features")

df = assembler.transform(df)

df = df.select('break_down', 'features')

# This is needed to save RDDs which is the only way to write nested Dataframes into CSV format
spark.sparkContext._jsc.hadoopConfiguration().set("mapred.output.committer.class",
                                                  "org.apache.hadoop.mapred.FileOutputCommitter")

# Split the overall dataset into 80-20 training and validation
(train_df, validation_df) = df.randomSplit([0.8, 0.2])
    
# Convert the train dataframe to RDD to save in CSV format and upload to S3
train_rdd = train_df.rdd.map(lambda x: (x.break_down, x.features))
train_lines = train_rdd.map(csv_line)
train_lines.saveAsTextFile('s3://{0}/data/preprocessed/train'.format(args['bucket']))

# Convert the validation dataframe to RDD to save in CSV format and upload to S3
validation_rdd = validation_df.rdd.map(lambda x: (x.break_down, x.features))
validation_lines = validation_rdd.map(csv_line)
validation_lines.saveAsTextFile('s3://{0}/data/preprocessed/val'.format(args['bucket']))
