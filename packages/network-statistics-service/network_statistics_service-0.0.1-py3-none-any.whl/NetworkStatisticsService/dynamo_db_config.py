class DynamoDBConfig(object):
	def __init__(self, aws_profile = 'default', aws_region = None, stats_table = None, logs_table = None):
		super().__init__()
		self.aws_profile = aws_profile
		self.aws_region = aws_region
		self.stats_table = stats_table
		self.logs_table = logs_table
	
	
	def is_valid(self, check_for_stats):
		if self.aws_region is None:
			return False
		if check_for_stats and self.stats_table is None:
			return False
		if not check_for_stats and self.logs_table is None:
			return False
		return True