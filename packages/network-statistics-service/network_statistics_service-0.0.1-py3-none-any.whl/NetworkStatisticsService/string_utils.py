class StringUtils(object):
    @staticmethod
    def remove_empty_strings_from_string_list(string_list):
        return list(filter(None, string_list))
