import time


class TimeUtils(object):

    @staticmethod
    def get_current_timestamp(return_as_dict=True, dict_key='Timestamp'):
        secondsSinceEpoch = round(time.time())
        if return_as_dict:
            return {dict_key: secondsSinceEpoch}
        else:
            return secondsSinceEpoch
