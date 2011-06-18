# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
"""
This module contains pyxform's `main` method plus related subroutines.

`main` is executed as the command line ``pyxform`` program.
"""

from optparse import OptionParser
#optparse is an awesome python utility for parsing cl options:
#http://docs.python.org/library/optparse.html

import sys, re, os, gzip
try:
    import simplejson as json
except ImportError:
    import json

import StringIO

# I moved pyxform specific imports into the main method to avoid import errors.

def main():
    usage = "Usage: %prog survey_filename.xls [--flagged-arguments *...]"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="output_filename",
                      help="the destination of the outputted file")
    parser.add_option("-f", "--format", dest="output_format", default="xml",
                      help="the format of the output. (xml, json, pyxform)")
    parser.add_option("-q", "--question-types", dest="question_types",
                      help="path to the question types file used in creating the survey")
    parser.add_option("-n", "--survey_name", help="the desired survey name",
                      action="store", dest="survey_name", default=False)
    parser.add_option("-t", "--translators", help="the path to the translation files",
                      action="store", dest="translators")
    parser.add_option("-i", "--include-dir", help="path to a directory to include source files (json and xls)",
                      action="store", dest="include_dir")
    parser.add_option("-p", "--pretty", help="make the json indented and pretty", action="store_true",
                      dest="pretty")
    parser.add_option("-s", "--skip-validation", dest="skip_validate", action="store_true",
                      help="checks the validity of the form using ODK Validate. (slightly faster. Use only when confident in the input)")
    (options, args) = parser.parse_args()
    
    dir_name = os.path.dirname(os.path.abspath(__file__))

    #nosetests passes something to stdin
    # if not sys.stdin.isatty():
    #     if len(args) != 0:
    #         parser.error("In this usage, pyxform takes no arguments")
    #     inpstr = ""
    #     for i in sys.stdin.readlines():
    #         inpstr += i
    #     pyx_package = json.loads(inpstr)
    # else:
    #begin untab
    sname = "SomeName"
    
    if len(args) != 1:
        parser.error("In this usage, pyxformr takes one argument")
    try:
        pyx_package = process_file_to_python_dict(args[0])
        dir_name = os.path.dirname(os.path.abspath(args[0]))
    except Exception, e:
        parser.error(e)
    
    if isinstance(pyx_package, list):
        pyx_package = {'type':'survey', 'children': pyx_package}
    
    if options.question_types:
        pyx_package['question_types'] = process_file_to_python_dict(options.question_types)
        sname = pyx_package[u'name']
    sections = {sname:pyx_package}

    if options.include_dir:
        import glob
        include_files = glob.glob(os.path.join(options.include_dir, "*.xls"))
        for ifile in include_files:
            name = ifile.split("/")[-1]
            f = process_file_to_python_dict(ifile)
            sections[name] = f
    from builder import create_survey as builder_create_survey
    survey = builder_create_survey(name_of_main_section=sname, sections=sections)
    if options.translators:
        #from translator import Translator
        f = open(options.translators, 'r')
        _transl = json.loads(f.read())
        translations = _transl.get(u"_dict", None)
        def translate_element(s):
            for child in s._children:
                translate_element(child)
            l = s.get_label()
            result = {"English": l}
            if l.__class__ in [unicode, str]:
                match = translations.get(l, None)
                if match is not None:
                    match['English'] = l
                    s.set_label(match)
        if translations is not None:
            translate_element(survey)
    else:
        translations = None
    
    if not options.skip_validate:
        "print to a temporary file and run ODK validate on it"
        pass

    #run the package through pyxform.
    #get back a string (or stringIO?)
    oformat = options.output_format
    if oformat == "xml":
        o = survey.to_xml()
    elif oformat in ["json", "jsongz", "pyxform"]:
        if options.pretty:
            o = json.dumps(survey.to_dict(), indent=4)
        else:
            o = json.dumps(survey.to_dict())

    if options.output_filename:
        if oformat in ["jsongz", "pyxform"]:
            with gzip.open(options.output_filename, 'wb') as outfile:
                outfile.write(o)
        else:
            with open(options.output_filename, 'w') as outfile:
                outfile.write(o)
    else:
        sys.stdout.write(o)
    exit(0)

def process_file_to_python_dict(fn, action=None):
    if not os.path.exists(fn): raise Exception("File not found: %s" % fn)
    if action is None:
        for act_key, res in INPUT_FILENAME_REGEX.items():
            for r in res:
                if re.search(r, fn):
                    action = act_key
                    break
        if action is None: #still
            raise Exception("Don't know what to do with this file: %s" % fn)
    if action == "spreadsheet":
        from xls2json import SurveyReader as ExcelSurveyReader
        s = ExcelSurveyReader(fn)
        z = s.to_dict()
        return s.to_dict()
    elif action in ["jsongz", "json"]:
        if action == "jsongz":
            with gzip.open(fn, 'rb') as jz:
                jsf = jz.read()
        else:
            with open(fn, 'r') as j:
                jsf = j.read()
        return json.loads(jsf)

if __name__ == "__main__":
    main()
