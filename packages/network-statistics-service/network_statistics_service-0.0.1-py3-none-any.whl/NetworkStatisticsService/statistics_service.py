from NetworkStatisticsService.command_line_utils import CommandLineUtils
from NetworkStatisticsService.latency_statistic_utils import LatencyStatisticUtils
from NetworkStatisticsService.speed_statistic_utils import SpeedStatisticUtils
from NetworkStatisticsService.time_utils import TimeUtils
from NetworkStatisticsService.informal_statistics_uploader import InformalStatisticUploaderInterface
from NetworkStatisticsService.dynamodb_statistics_uploader import DynamoDBStatisticsUploader
from NetworkStatisticsService.exceptions import CommandRunException, DynamoDbException, LatencyStatisticsException, NetworkStatisticsServiceException, SpeedStatisticsException

class StatisticsService(object):
	
	def __init__(self, default_ping_count = 20, stats_uploader = None):
		# TODO - see if it is easier to pass a DynamoDB Config Object (and encapsulate the check into it)
		super().__init__()
		if stats_uploader is not None:
			if not issubclass(stats_uploader, InformalStatisticUploaderInterface):
				raise ValueError("Provided statistics uploader does not implement the InformalStatisticUploaderInterface.")
		
		self.__default_ping_count = default_ping_count
		self.__stats_uploader = stats_uploader

		self.speed_statistics_enabled = True
		self.latency_statistics_enabled = True

		self.stats_upload_enabled = False
		self.logs_upload_enabled = False
		
		self.aws_config = None
	

	def gather_statistics(self, override_ping_count=None):
		timestamp_dict = TimeUtils.get_current_timestamp()

		try:
			latency_stats = self.__gather_latency_statistics(override_ping_count)
			speed_stats = self.__gather_speed_statistics()  
			full_stats = {**latency_stats, **speed_stats, **timestamp_dict}
			self.__upload_statistics(full_stats)
		except NetworkStatisticsServiceException as re:
			error_dict = {**{'Error': re}, **TimeUtils.get_current_timestamp()}
			self.__upload_logs(error_dict)

		return full_stats


	def __gather_latency_statistics(self, override_ping_count):
		if self.latency_statistics_enabled:
			ping_count = self.__default_ping_count
			if override_ping_count is not None:
				ping_count = override_ping_count

			try:
				ping_command = "ping www.google.com -c " + str(ping_count)
				statistics_rows = self.__gather_statistics(ping_command)
				latency_statistics = LatencyStatisticUtils.extract_latency_statistics_from_command_output(statistics_rows)
				return latency_statistics
			except (LatencyStatisticsException, CommandRunException) as re:
				raise NetworkStatisticsServiceException("Latency statistics failed. Nested error: " + str(re))
		else:
			return {}


	def __gather_speed_statistics(self):
		if self.speed_statistics_enabled:
			try:
				statistics_rows = self.__gather_statistics("speedtest --simple")
				speed_statistics = SpeedStatisticUtils.extract_speed_statistics_from_command_output(statistics_rows)
				return speed_statistics
			except (SpeedStatisticsException, CommandRunException) as re:
				raise NetworkStatisticsServiceException("Speed statistics failed. Nested error: " + str(re))
		else:
			return {}


	def __gather_statistics(self, command):
		output, error = CommandLineUtils.run_bash_command(command)
		if error is not None:
			raise CommandRunException("Command " + command + " failed with error:\n" + error)
		else:
			output_rows = output.decode().split("\n")
			return list(filter(None, output_rows))[-2:]


	def __upload_statistics(self, stats_dict):
		if self.stats_upload_enabled:
			if self.__stats_uploader is None:
				# Defaults to using dynamoDB.
				if self.aws_config is None or not self.aws_config.is_valid(True):
					raise DynamoDbException("Upload enabled and no other provider offered. Dynamo DB configuration is incomplete.\n" + 
									"Please set values to aws_region and dynamodb_stats_table_name.")
				self.__stats_uploader = DynamoDBStatisticsUploader(self.aws_config)
			self.__stats_uploader.upload_statistics(stats_dict)


	def __upload_logs(self, logs_dict):
		if self.logs_upload_enabled:
			if self.__stats_uploader is None:
				# Defaults to using dynamoDB.
				if self.aws_config is None or not self.aws_config.is_valid(False):
					raise DynamoDbException("Upload enabled and no other provider offered. Dynamo DB configuration is incomplete.\n" + 
									"Please set values to aws_region and dynamodb_logs_table_name.")
				self.__stats_uploader = DynamoDBStatisticsUploader(self.aws_config)
			self.__stats_uploader.upload_statistics(logs_dict)
		else:
			print(logs_dict)
