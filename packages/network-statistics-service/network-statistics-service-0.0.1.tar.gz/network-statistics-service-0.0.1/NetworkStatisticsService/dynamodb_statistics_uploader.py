import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal
from NetworkStatisticsService.informal_statistics_uploader import InformalStatisticUploaderInterface
from NetworkStatisticsService.exceptions import DynamoDbException


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Decimal):
			if abs(o) % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)


class DynamoDBStatisticsUploader(InformalStatisticUploaderInterface):
	def __init__(self, aws_config):
		super().__init__()
		self.__aws_region = aws_config.aws_region
		self.__aws_profile = aws_config.aws_profile
		self.__stats_table = aws_config.stats_table
		self.__logs_table = aws_config.logs_table
	
	def upload_statistics(self, stats_dict: dict):
		session = boto3.Session(profile_name=self.__aws_profile)
		dynamodb_client = session.resource('dynamodb', region_name=self.__aws_region)
		table = dynamodb_client.Table(self.__stats_table)
		stats_dict = json.loads(json.dumps(stats_dict), parse_float=Decimal)
		
		try:
			table.put_item(Item=stats_dict)
		except ClientError as ce:
			error_log = {"Error": ce, "Timestamp": stats_dict["Timestamp"]}
			self.upload_logs(error_log)

	def upload_logs(self, logs_dict: dict):
		session = boto3.Session(profile_name=self.__aws_profile)
		dynamodb_client = session.resource('dynamodb', region_name=self.__aws_region)
		table = dynamodb_client.Table(self.__logs_table)
		stats_dict = json.loads(json.dumps(stats_dict), parse_float=Decimal)
		
		try:
			table.put_item(Item=stats_dict)
		except ClientError as ce:
			raise DynamoDbException("Failed to upload logs to DynamoDB: " + ce)
