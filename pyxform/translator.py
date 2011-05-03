# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from collections import defaultdict
import glob
import os
import utils

def infinite_dict():
    return defaultdict(infinite_dict)

# Here's the big idea:
# translator = Translator()
# translator.add_translation(...)
# translator.translate('How are you?')
# {"English" : "How are you?", "French" : "cava?", "Spanish" : ...}

class Translator(object):
    
    def __init__(self, dictionary={}):
        self._dict = defaultdict(dict)
        self._languages = []

    def add_translation(self, english_string, destination_language, translated_string):
        if destination_language not in self._languages:
            self._languages.append(destination_language)
        self._dict[english_string][destination_language] = translated_string

    def translate(self, string):
        return self._dict.get(string, string)

    def to_dict(self):
        return {
            u"_dict" : self._dict,
            u"_languages" : self._languages,
            }

    def load_from_json(self, path):
        d = utils.get_pyobj_from_json(path)
        for k, v in d.iteritems():
            setattr(self, k, v)

    def dump_to_json(self, path):
        utils.print_pyobj_to_json(self.to_dict(), path)

this_directory = os.path.dirname(__file__)
translators_folder = os.path.join(this_directory, "translators", "*.json")
TRANSLATORS = {}
for path in glob.glob(translators_folder):
    translator = Translator()
    translator.load_from_json(path)
    directory, file_name = os.path.split(path)
    translator_name, extension = os.path.splitext(file_name)
    TRANSLATORS[translator_name] = translator


# code used to construct a translator from the excel files from phase II.
# import glob, os
# from xls2json import ExcelReader, print_pyobj_to_json
# from translator import Translator

# translator = Translator()

# def add_dict(d):
#     keys = d.keys()
#     keys.remove(u"English")
#     for key in keys:
#         yield {u"english_string" : d[u"English"],
#                u"destination_language" : key,
#                u"translated_string" : d[key]}

# def add_row(d):
#     assert type(d)==dict, str(d)
#     for k, v in d.items(): 
#         if type(v)==dict and u"English" in v.keys():
#             for result in add_dict(v): yield result

# xls_files = glob.glob( os.path.join("translators", "*", "*.xls") )
# all_translations = []
# for xls_file in xls_files:
#     excel_reader = ExcelReader(xls_file)
#     for sheet_name, list_of_dicts in excel_reader.to_dict().items():
#         for d in list_of_dicts:
#             for result in add_row(d):
#                 translator.add_translation(**result)
# print_pyobj_to_json(translator.to_dict(), "nigeria.json")
