from NetworkStatisticsService.exceptions import SpeedStatisticsException

class SpeedStatisticUtils(object):

	@staticmethod
	def extract_speed_statistics_from_command_output(statistics_rows):
		try: 
			stats = {}
			for row in statistics_rows:
				elems = row.split(":")
				stats[elems[0]] = float(elems[1].strip().split()[0].strip())
			return stats
		except IndexError as ie:
			raise SpeedStatisticsException("An error occured when processing the speed statistics.\nUnderlying error: " + str(ie))
