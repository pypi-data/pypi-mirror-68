from NetworkStatisticsService.exceptions import CommandOutputFormatException, LatencyStatisticsException

class LatencyStatisticUtils(object):

	@staticmethod
	def __get_packet_loss_from_command_output(packet_loss_row):
		stats = {}
		try:
			stats['Loss'] = float(packet_loss_row.split(",")[-1].strip().split()[0][:-1])
			return stats
		except (IndexError, ValueError) as error:
			raise CommandOutputFormatException("Ping command output for the packet loss row was not of expected format.\nUnderlaying error: " + str(error))

	@staticmethod
	def __get_ping_statistics_from_command_output(min_avg_max_row):
		try:
			elems = min_avg_max_row.split("=")
			keys = elems[0].strip().split()[-1].split("/")
			values = elems[1].strip().split()[0].split("/")
			stats = {}
			for index, key in enumerate(keys):
				stats[key.capitalize()] = float(values[index])
			return stats
		except IndexError as ie:
			raise CommandOutputFormatException("Ping command output for the packe loss row was not of expected format.\nUnderlaying error: " + str(ie))

	@staticmethod
	def extract_latency_statistics_from_command_output(statistics_rows):
		try:
			packet_loss_row, min_avg_max_row = statistics_rows[0], statistics_rows[1]
			loss_stats = LatencyStatisticUtils.__get_packet_loss_from_command_output(packet_loss_row)
			ping_stats = LatencyStatisticUtils.__get_ping_statistics_from_command_output(min_avg_max_row)
			return {**loss_stats, **ping_stats}
		except IndexError as ie:
			raise LatencyStatisticsException("Accessing the two statistic rows failed.\nUnderlying error: " + str(ie))
		except CommandOutputFormatException as cofe:
			raise LatencyStatisticsException("An error occured when processing the latency statistics.\nUnderlying error: " + str(cofe))
