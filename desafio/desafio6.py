from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, sum


spark = SparkSession.builder.appName("VendasExercicio").getOrCreate()

df = spark.read.csv("vendas.csv", header=True, inferSchema=True)

print("Primeiras 5 linhas do DataFrame:")
df.show(5)


clientes_com_maior_valor = df.groupBy("id_cliente").agg(sum("valor_compra").alias("total_compra"))
clientes_com_maior_valor.show()

df_com_ano = df.withColumn("ano", year(col("data_compra")))  
vendas_anuais = df_com_ano.groupBy("ano").agg(sum("valor_compra").alias("total_vendas_anuais"))
vendas_anuais.show()

clientes_com_maior_valor.write.csv("clientes_com_maior_valor.csv", header=True)

vendas_anuais.write.json("vendas_anuais.json")

spark.stop()