"""

MTA models with Pyspark; to be included in the MTA package

"""

from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, concat_ws, split, explode, lit

from itertools import chain, tee, combinations

import re
import os
import json
import builtins
import pandas as pd
from collections import defaultdict
from itertools import chain


class BaselineModel:

	"""
	basic class implementing functionality commonly required by attribution models
	"""

	@staticmethod
	def ordered_tuple(t, dontmove=['(start)']):

		"""
		return tuple t ordered 
		"""

		sort = lambda t: tuple(sorted(list(t)))

		return (t[0],) + sort(t[1:]) if (t[0] in dontmove) and (len(t) > 1) else sort(t)

	@staticmethod
	@udf(returnType=ArrayType(StringType())) 
	def get_path_without_loops(path):

		"""
		remove adjacent duplicates from a list path
		"""
		
		clean_path = []

		for i, c in enumerate(path, 1):

			if i == 1:
				clean_path.append(c)
			else:
				if c != clean_path[-1]:
					clean_path.append(c)

		return clean_path

	@staticmethod
	@udf(returnType=ArrayType(StringType())) 
	def window(path, display):

		"""
		return a list of all touch point pairs present on the list path;
		for example, for a path a > b > c return a list [((start), a), (a,b), (b,c), (c, (end))]
		"""
		print('display is ', display)

		it1, it2 = tee(path)
		next(it2, None)

		c = [f'({it1},{it2})' for it1, it2 in zip(it1, it2)]

		return c

	@staticmethod
	@udf(returnType=ArrayType(StringType())) 
	def combs(path):

		"""
		return a list of all combinations of touch point present on the list path;
		for example, for a path a > b > c  return a list [a,b,c,a-b,a-c,b-c]
		"""

		c = []

		for n in range(4):

			for tup in combinations(set(path), n):

				c.append(BaselineModel.ordered_tuple(tup))

		return c

	def __init__(self):

		self.NULL = '(null)'
		self.START = '(start)'
		self.CONV = '(conversion)'
		self.END = '(end)'

	def load(self, file):

		"""
		load data; this method needs to support ingestion from several possible sources:
			- local hard drive
			- buckets (S3 or GC)
		"""

		self.sep = ','
		self.data = spark.read.option("inferSchema", "true") \
						.option("header", "true") \
							.csv(file)

		# certain column names must be present in the ingested data
		self.required_columns = set('path total_conversions total_conversion_value total_null exposure_times'.split())

		if not (set(self.data.columns) <= self.required_columns):  # note: ok to have extra columns
			raise ValueError(f'some required column names are missing!')

		return self

	def remove_loops(self):

		"""
		remove loops from paths and update conversion counts
		"""

		self.data = self.data.withColumn('path', \
							concat_ws(' > ', \
								BaselineModel.get_path_without_loops(split(self.data.path, r'\s*>\s*'))))

		# since now we may have some duplicate paths, we need to remove duplicates and update conversion counts
		self.data = self.data.groupBy('path').sum() \
						.toDF(*['path', 'total_conversions', 'total_conversion_value', 'total_null'])

		return self

	def pair_convs_and_exits(self, display):

		"""
		return a dictionary that maps each pair of touch points on the path to the number of conversions and
		nulls this pair is involved into
		"""

		k = defaultdict(lambda: defaultdict(int))

		# attach the start and end labels
		self.data = self.data.withColumn('path', split(concat_ws(' > ', 
					lit(f'{self.START}'), self.data.path, lit(f'{self.END}')), r'\s*>\s*'))

		self.data = self.data.withColumn('pairs', BaselineModel.window(self.data.path, display))

		# for row in self.data.select(explode(self.data.pairs), self.data.total_conversions, self.data.total_null).collect():
			
		# 	k[row['col']]['conversions'] += row['total_conversions']
		# 	k[row['col']]['nulls'] += row['total_null']

		# return k

	# def ordered_tuple(self, t):

	# 	"""
	# 	return tuple t ordered 
	# 	"""

	# 	sort = lambda t: tuple(sorted(list(t)))

	# 	return (t[0],) + sort(t[1:]) if (t[0] == '(start)') and (len(t) > 1) else sort(t)

	def get_generated_conversions(self, m=3):

		"""
		count all conversions and nulls "generated" by combinations of up to m touch points

		what this means: suppose we have a path (start) > a > b > a > and for this one there have been c conversions;
		then every combination of 1 (up to, say 2) touch points we give them +c credit:
		(start), a, b, a all get +c (a twice); also (start)-a, (start)-b, (start)-a, a-b, a-a, b-a all get +c

		so we are basically saying that if a combination is present on a converting path it gets +c; present twice? get credit twice, 
		and so on. 

		a few things to keep in mind:
			- labels like (start) and any combinations that involve labels do not get credit
			- we previously removed loops on the path, i.e. replaced a->a with a; what about combinations like a-a? 
				we provide an option to ignore or not

		"""

		k = defaultdict(lambda: defaultdict(float))

		# attach the start and end labels
		self.data = self.data.withColumn('path', split(self.data.path, r'\s*>\s*'))
		self.data = self.data.withColumn('combs', BaselineModel.combs(self.data.path))

		self.data.show()
		# for row in self.data.select(explode(self.data.combs), self.data.total_conversions, self.data.total_null).collect():
			
		# 	print(row)
		# 	k[row['combs']]['conversions'] += row['total_conversions']
		# 	k[row['combs']]['nulls'] += row['total_null']

		return k

	# def normalize_dict(d):
	# 	"""
	# 	returns a value-normalized version of dictionary d
	# 	"""
	# 	sum_all_values = builtins.sum(d.values())
	
	# 	for _ in d:
	# 		d[_] = builtins.round(d[_]/sum_all_values, 6)
	
	# 	return d

	

	


# class Shapley(BaselineModel):

# 	def __init__(self):
# 		pass

		

# def order_by_exposure_time(s):
	
# 	clean_path = []

# 	for i, c in enumerate(s, 1):

# 		if i == 1:
# 			clean_path.append(c)
# 		else:
# 			if c not in clean_path:
# 				clean_path.append(c)

# 	return clean_path

# order_by_exposure_time_UDF = udf(order_by_exposure_time, ArrayType(StringType()))



# def touch(df, t='first'):

# 	_touch = defaultdict(int)

# 	df = remove_loops(df)
# 	df = df.withColumn('path', split(df.path, r'\s*>\s*'))
# 	df = df.withColumn('ch_1', df.path.getItem(0) if t == 'first' else df.path.getItem(size(df.path)-1))

# 	for row in df.select('ch_1', 'total_conversions').groupBy('ch_1').sum().toDF('channel', 'counts').collect():
# 		_touch[row['channel']] = row['counts']

# 	return normalize_dict(_touch)

# keep_unique = udf(lambda s: list(builtins.set(s)), ArrayType(StringType()))
# count_unique = udf(lambda s: len(builtins.set(s)), IntegerType())

# def linear(df, share='same'):

# 	_lin = defaultdict(float)

# 	df = df.withColumn('path', split(df.path, r'\s*>\s*'))
# 	df = df.withColumn('n', count_unique(df.path))
# 	df = df.withColumn('s', df.total_conversions/df.n)

# 	for row in df.select(explode(keep_unique(df.path)).alias('channel'), df.s).groupBy('channel').sum().toDF('channel', 'counts').collect():
# 		_lin[row['channel']] = row['counts']

# 	return normalize_dict(_lin)

# costs = udf(lambda p, s: {c: i*s/builtins.sum(range(1,len(p) + 1)) for i, c in enumerate(p, 1)}, MapType(StringType(), FloatType()))

# def time_decay(df):

# 	dec_ = defaultdict(float)

# 	df = df.withColumn('path', split(df.path, r'\s*>\s*'))

# 	df = df.withColumn('path', order_by_exposure_time_UDF(df.path))

# 	df = df.withColumn('credits', costs(df.path, df.total_conversions))

# 	for row in df.select(explode(df.credits)).groupBy('key').sum().toDF('channel', 'counts').collect():
# 		dec_[row['channel']] = row['counts']

# 	return normalize_dict(dec_)

# pos_creds = udf(lambda channels, n, convs: {c: cr for c, cr in zip(channels, 
# 						[convs/1.] if n == 1 else [convs/2.]*2 if n == 2 else [0.4*convs] + [0.2*convs]*(n-2) + [0.4*convs])}, MapType(StringType(), FloatType()))

# def position_based(df):

# 	posb = defaultdict(float)

# 	df = remove_loops(df)

# 	df = df.withColumn('path', split(df.path, r'\s*>\s*'))

# 	df = df.withColumn('n', count_unique(df.path))
# 	df = df.withColumn('cr', pos_creds(df.path, df.n, df.total_conversions))

# 	for row in df.select(explode(df.cr)).groupBy('key').sum().toDF('channel', 'counts').collect():
# 		posb[row['channel']] = row['counts']

# 	return normalize_dict(posb)




# window_udf = udf(window, ArrayType(StringType()))




# def outcome_counts(tp_list, convs, nulls, nc=3, count_duplicates=False):

# 	"""
# 	calculate the sum of all conversions and exits (nulls) associated with presence
# 	of various combination of touch points on a path tp_list

# 	inputs:
# 	-------

# 		tp_list: a list of touch points, e.g. [alpha, beta, gamma, alpha, mu, ...]
# 		convs: total number of conversions for this path
# 		nulls: total number of nulls for this path
# 		nc: length of element subsequences for combinations, e.g. 2 for pairs, 1 for singles, etc.
# 		count_duplicates: if True, count combinations

# 	output:
# 	------
# 		a dictionary mapping combinations to counts of conversions and nulls and probabilities of conversion, 
# 		e.g. {(alpha, gamma): {'cs': 3, 
# 								'ns': 6}, ...}
# 	"""

# 	dedupl_tp_list = [tp_list[0]]

# 	if not count_duplicates:
# 		for _ in tp_list[1:]:
# 			if _ not in dedupl_tp_list[-1]:
# 				dedupl_tp_list.append(_)
# 		tp_list = dedupl_tp_list

# 	r = defaultdict(lambda: defaultdict(float))

# 	for n in range(1, nc+1):

# 		# combinations('ABCD', 2) --> AB AC AD BC BD CD
# 		for c in combinations(tp_list, n):
			
# 			t = ordered_tuple(c)  # tuple(sorted(list(t)))

# 			if t != ('(start)',):
# 				r[t]['cs'] += convs
# 				r[t]['ns'] += nulls

# 	return r

# def trans_matrix(k):

# 	"""
# 	calculate transition matrix which will actually be a dictionary mapping 
# 	a pair (a, b) to the probability of moving from a to b, e.g. T[(a, b)] = 0.5
# 	"""

# 	tr = defaultdict(float)

# 	outs = defaultdict(int)

# 	for pair in k:

# 		outs[pair[0]] += k[pair]['conversions'] + k[pair]['null']

# 	for pair in k:

# 		tr[pair] = (k[pair]['conversions'] + k[pair]['null'])/outs[pair[0]]

# 	return tr

if __name__ == '__main__':


	# in pyspark Spark session is readily available as spark
	spark = SparkSession.builder.master("local").appName("test session").getOrCreate()

	# set a smaller number of executors because this is running locally
	spark.conf.set("spark.sql.shuffle.partitions", "4")

	bl = BaselineModel()

	bl.load(file='data/data.csv.gz').remove_loops()

	bl.data.show()

	bl.pair_convs_and_exits(display='YYYYYY!!!')

	# print(bl.ordered_tuple(('(start)', 'a','b','d','a'), dontmove=['(start)']))

	# read the data file
	# df = spark.read.option("inferSchema", "true") \
	# 		.option("header", "true") \
	# 		.csv("data/data.csv.gz")

	# c = defaultdict(int)

	# attribution = defaultdict(lambda: defaultdict(float))

# attribution['last_touch'] = touch(df, 'last')
# attribution['first_touch'] = touch(df, 'first')
# attribution['linear'] = linear(df)
# attribution['time_decay'] = time_decay(df)
# attribution['position_based'] = position_based(df)

# res = pd.DataFrame.from_dict(attribution)

# print(res)

# k = pair_convs_and_exits(df)
# t = trans_matrix(k)

# print(t)


# df.show(5)
# o = combination_contributions(['(start)', 'alpha', 'gamma', 'beta', 'gamma', 'kappa'], 3, 16, nc=3)
# print(o)
