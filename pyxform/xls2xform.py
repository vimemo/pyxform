"""
xls2xform converts properly formatted Excel documents into XForms for
use with ODK Collect.
"""
import sys
import xls2json
import builder
import json
import argparse
from utils import sheet_to_csv

def xls2xform_convert(xlsform_path, xform_path):
    warnings = []

    json_survey = xls2json.parse_file_to_json(xlsform_path, warnings=warnings)
    survey = builder.create_survey_element_from_dict(json_survey)
    # Setting validate to false will cause the form not to be processed by
    # ODK Validate.
    # This may be desirable since ODK Validate requires launching a subprocess
    # that runs some java code.
    survey.print_xform_to_file(xform_path, validate=True, warnings=warnings)

    return warnings


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_XLSForm')
    parser.add_argument('output_path')
    parser.add_argument('--json',
        action='store_true',
        help="Capture everything and report in JSON format.")
    parser.add_argument('--external_choices_csv',
        default=None,
        help="Output the choices sheet as a csv at the given location.")
    args = parser.parse_args()
    
    if args.external_choices_csv:
        success = sheet_to_csv(args.path_to_XLSForm, args.external_choices_csv, "external_choices")
        if not success:
            print "Count not output external_choices sheet. Maybe it is missing or empty."
    if args.json:
        # Store everything in a list just in case the user wants to output
        # as a JSON encoded string.
        response = {'code': None, 'message': None, 'warnings': []}

        try:
            response['warnings'] = xls2xform_convert(args.path_to_XLSForm, args.output_path)

            response['code'] = 100
            response['message'] = "Ok!"

            if response['warnings']:
                response['code'] = 101
                response['message'] = 'Ok with warnings.'

        except Exception as e:
            # Catch the exception by default.
            response['code'] = 999
            response['message'] = str(e)

        print json.dumps(response)
    else:
        warnings = xls2xform_convert(args.path_to_XLSForm, args.output_path)

        # Regular output. Just print.
        print "Warnings:"
        for w in warnings:
            print w
        print 'Conversion complete!'
