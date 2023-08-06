"""
main - entry point of the package

This file is performing CSV read into HYPER file and measures time elapsed (performance)
"""
# package to handle files/folders and related metadata/operations
import os
# Custom classes specific to this package
from project_locale.localizations_common import LocalizationsCommon
from tableau_hyper_management.ProjectNeeds import ProjectNeeds
from tableau_hyper_management.TableauHyperApiExtraLogic import TableauHyperApiExtraLogic
from tableau_hyper_management.TypeDetermination import TypeDetermination
# get current script name
SCRIPT_NAME = os.path.basename(__file__).replace('.py', '')

# main execution logic
if __name__ == '__main__':
    # instantiate Localizations Common class
    class_lc = LocalizationsCommon()
    # ensure all compiled localization files are in place (as needed for localized messages later)
    class_lc.run_localization_compile()
    # establish localization language to use
    language_to_use = class_lc.get_region_language_to_use_from_operating_system()
    # instantiate Extractor Specific Needs class
    class_pn = ProjectNeeds(SCRIPT_NAME, language_to_use)
    # load application configuration (inputs are defined into a json file)
    class_pn.load_configuration()
    # adding a special case data type
    class_pn.config['data_types']['empty'] = '^$'
    class_pn.config['data_types']['str'] = ''
    # initiate Logging sequence
    class_pn.initiate_logger_and_timer()
    # reflect title and input parameters given values in the log
    class_pn.class_clam.listing_parameter_values(
        class_pn.class_ln.logger, class_pn.timer, 'Tableau Hyper Converter',
        class_pn.config['input_options'][SCRIPT_NAME], class_pn.parameters)
    relevant_files_list = class_pn.class_fo.fn_build_file_list(
            class_pn.class_ln.logger, class_pn.timer, class_pn.parameters.input_file)
    # log file statistic details
    class_pn.class_fo.fn_store_file_statistics(
            class_pn.class_ln.logger, class_pn.timer, relevant_files_list, 'Input')
    # loading from a specific folder all files matching a given pattern into a data frame
    input_dict = {
        'compression': class_pn.parameters.input_file_compression,
        'field delimiter': class_pn.parameters.csv_field_separator,
        'file list': relevant_files_list,
        'format': class_pn.parameters.input_file_format,
        'name': 'irrelevant',
    }
    working_data_frame = class_pn.class_dio.fn_load_file_into_data_frame(
            class_pn.class_ln.logger, class_pn.timer, input_dict)
    if working_data_frame is not None:
        tuple_supported_file_types = class_pn.class_dio.implemented_disk_write_file_types
        if class_pn.parameters.output_file_format.lower() in tuple_supported_file_types:
            output_dict = input_dict
            output_dict['file list'] = 'irrelevant'
            output_dict['format'] = class_pn.parameters.output_file_format
            output_dict['name'] = class_pn.parameters.output_file
            output_dict['compression'] = class_pn.parameters.output_file_compression
            class_pn.class_dio.fn_store_data_frame_to_file(
                class_pn.class_ln.logger, class_pn.timer, working_data_frame, output_dict)
            # store statistics about output file
            class_pn.class_fo.fn_store_file_statistics(
                class_pn.class_ln.logger, class_pn.timer,
                class_pn.parameters.output_file, 'Generated')
        elif class_pn.parameters.output_file_format.lower() == 'hyper':
            # instantiate Tableau Hyper Api Extra Logic class
            class_thael = TableauHyperApiExtraLogic(language_to_use)
            supported_types = class_thael.supported_input_file_types
            if class_pn.parameters.input_file_format.lower() in supported_types:
                class_pn.timer.start()
                c_td = TypeDetermination(language_to_use)
                # advanced detection of data type within Data Frame
                detected_csv_structure = c_td.fn_detect_csv_structure(
                    class_pn.class_ln.logger, working_data_frame, class_pn.parameters,
                    class_pn.config['data_types'])
                class_pn.timer.stop()
                # create HYPER from Data Frame
                class_thael.fn_run_hyper_creation(
                    class_pn.class_ln.logger, class_pn.timer, working_data_frame,
                    detected_csv_structure, class_pn.parameters)
                # store statistics about output file
                class_pn.class_fo.fn_store_file_statistics(
                    class_pn.class_ln.logger, class_pn.timer,
                    class_pn.parameters.output_file, 'Generated')
            else:
                print('For time being only CSV, JSON and Pickle file types are supported'
                      + ' as input file type in combination with '
                      + 'Tableau Extract (Hyper) as output file type.')
    # just final message
    class_pn.class_bn.fn_final_message(
            class_pn.class_ln.logger, class_pn.parameters.output_log_file,
            class_pn.timer.timers.total(SCRIPT_NAME))
