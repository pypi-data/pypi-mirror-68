class NetworkStatisticsServiceException(Exception):
	pass

class CommandOutputFormatException(NetworkStatisticsServiceException):
	pass

class LatencyStatisticsException(NetworkStatisticsServiceException):
	pass

class SpeedStatisticsException(NetworkStatisticsServiceException):
	pass

class DynamoDbException(NetworkStatisticsServiceException):
	pass

class CommandRunException(NetworkStatisticsServiceException):
	pass