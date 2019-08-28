from __future__ import print_function
from __future__ import unicode_literals

import time
import sys
import os
import shutil
import csv
import boto3
import pyspark
import zipfile
import tarfile

from time import gmtime, strftime
from awsglue.utils import getResolvedOptions

import mleap.pyspark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.sql.types import StructField, StructType, StringType, DoubleType, FloatType
from pyspark.ml.feature import StringIndexer, VectorIndexer, OneHotEncoder, VectorAssembler
from pyspark.sql.functions import *
from mleap.pyspark.spark_support import SimpleSparkSerializer

from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

def csv_line(data):
    r = ','.join(str(d) for d in data[1])
    return str(data[0]) + "," + r

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_BUCKET'])

# This is needed to save RDDs which is the only way to write nested Dataframes into CSV format
spark.sparkContext._jsc.hadoopConfiguration().set("mapred.output.committer.class",
                                                  "org.apache.hadoop.mapred.FileOutputCommitter")


windturbine_rawdata = glueContext.create_dynamic_frame.from_catalog(
    database="endtoendml-db", table_name="data")

df = windturbine_rawdata.toDF()
df = df.na.replace('', "HAWT", subset=["turbine_type"])
df = df.na.fill(37.0, subset=["oil_temperature"])

col0_indexer = StringIndexer(inputCol="turbine_id", outputCol="indexed_turbine_id")
col1_indexer = StringIndexer(inputCol="turbine_type", outputCol="indexed_turbine_type")
col10_indexer = StringIndexer(inputCol="wind_direction", outputCol="indexed_wind_direction")
col11_indexer = StringIndexer(inputCol="breakdown", outputCol="indexed_breakdown")

turbine_id_encoder = OneHotEncoder(inputCol="indexed_turbine_id", outputCol="turb_id").setDropLast(False)
turbine_type_encoder = OneHotEncoder(inputCol="indexed_turbine_type", outputCol="turb_type").setDropLast(False)
wind_direction_encoder = OneHotEncoder(inputCol="indexed_wind_direction", outputCol="wind_dir").setDropLast(False)

#col4_imputer = Imputer(inputCols=["col4float"], outputCols=["oil_temp"], strategy="median")

assembler = VectorAssembler(inputCols=['turb_id', 'turb_type', 'wind_speed', 'rpm_blade', 'oil_temperature', 'oil_level','temperature','humidity', 'vibrations_frequency', 'pressure', 'wind_dir'], outputCol="features")

pipeline = Pipeline(stages=[col0_indexer, col1_indexer, col10_indexer, col11_indexer, turbine_id_encoder, turbine_type_encoder, wind_direction_encoder, assembler])

model = pipeline.fit(df)
df = model.transform(df)


# Split the overall dataset into 80-20 training and validation
(train_df, validation_df) = df.randomSplit([0.8, 0.2])
    
# Convert the train dataframe to RDD to save in CSV format and upload to S3
train_rdd = train_df.rdd.map(lambda x: (x.indexed_breakdown, x.features))
train_lines = train_rdd.map(csv_line)
train_lines.saveAsTextFile('s3://{0}/data/preprocessed/train'.format(args['S3_BUCKET']))

# Convert the validation dataframe to RDD to save in CSV format and upload to S3
validation_rdd = validation_df.rdd.map(lambda x: (x.indexed_breakdown, x.features))
validation_lines = validation_rdd.map(csv_line)
validation_lines.saveAsTextFile('s3://{0}/data/preprocessed/val'.format(args['S3_BUCKET']))

# Serialize and store the model via MLeap
timestamp = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
model_filename = '/tmp/model-' + timestamp + '.zip'
SimpleSparkSerializer().serializeToBundle(model, 'jar:file:' + model_filename, validation_df)

# Unzip the model as SageMaker expects a .tar.gz file but MLeap produces a .zip file
    
with zipfile.ZipFile(model_filename) as zf:
    zf.extractall("/tmp/model-" + timestamp)

# Write back the content as a .tar.gz file
    
with tarfile.open("/tmp/model-" + timestamp + ".tar.gz", "w:gz") as tar:
    tar.add("/tmp/model-" + timestamp + "/bundle.json", arcname='bundle.json')
    tar.add("/tmp/model-" + timestamp + "/root", arcname='root')
    
# Upload the model in tar.gz format to S3 so that it can be used with SageMaker for inference later
s3 = boto3.resource('s3') 
#file_name = os.path.join(args['bucket'], '/model/', 'model.tar.gz')
s3.Bucket(args['S3_BUCKET']).upload_file('/tmp/model-' + timestamp + '.tar.gz', 'output/sparkml/model.tar.gz')

