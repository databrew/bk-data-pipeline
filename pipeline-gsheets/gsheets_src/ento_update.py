# This script is used updating ento labs data
# anomalies list for user input
#
# Author: atediarjo@gmail.com
import os
import pygsheets as pg
import pandas as pd
from datetime import datetime

# VARIABLES
VARNAME_DICT = {
    'CDC Individual Mosquitoes': ['date_of_collection', 
                       'sample_id', 
                       'site_of_collection',
                       'cluster', 
                       'study_arm', 
                       'hh_id', 
                       'le_id',
                       'box_id',
                       'tube_position_id',
                       'species_complex_id',
                       'phsyiological_status',
                       'sample_condition',
                       'species_pcr_complex_id',
                       'species_pcr_sibling_species',
                       'species_pcr_test_by',
                       'species_maldi_tof_complex_id',
                       'species_maldi_tof_sibling_species',
                       'species_maldi_tof_log_score',
                       'species_maldi_tof_repeat_pcr',
                       'species_maldi_tof_test_by',
                       'species_maldi_tof_qc',
                       'species_maldi_tof_query_date',
                       'field_parity_status',
                       'age_grading_maldi_tof_parity_status',
                       'age_grading_maldi_tof_log_score',
                       'age_grading_maldi_tof_added_to_db',
                       'age_grading_maldi_tof_query_date',
                       'age_grading_maldi_tof_test_by',
                       'plasmodium_elisa_results',
                       'plasmodium_elisa_test_by',
                       'plasmodium_maldi_tof_results',
                       'plasmodium_maldi_tof_log_score',
                       'plasmodium_maldi_tof_added_to_db',
                       'plasmodium_maldi_tof_query_date',
                       'plasmodium_maldi_tof_test_by',
                       'plasmodium_maldi_tof_qc',
                       'plasmodium_maldi_pcr_results',
                       'plasmodium_maldi_pcr_test_by',
                       'bloodmeal_elisa_results',
                       'bloodmeal_elisa_spcecifics',
                       'bloodmeal_elisa_test_by',
                       'bloodmeal_maldi_tof_results',
                       'bloodmeal_maldi_tof_spcecifics',
                       'bloodmeal_maldi_tof_log_score',
                       'bloodmeal_maldi_tof_repeat_pcr',
                       'bloodmeal_maldi_tof_test_by',
                       'bloodmeal_maldi_tof_qc',
                       'bloodemeal_maldi_tof_query_date'
                       ],
        'CDC Pooled Mosquitoes': ['date_of_collection', 
                       'pool_sample_id',
                       'pool_sample_id_ind_mosquitoes_enum', 
                       'site_of_collection',
                       'cluster', 
                       'study_arm', 
                       'hh_id', 
                       'le_id',
                       'box_id',
                       'tube_position_id',
                       'num_mosquitoes_per_tube_listed',
                       'species_complex_id',
                       'condition_of_pooled_sample',
                       'num_mosquitoes_per_tube_final',
                       'phsyiological_status',
                       'sample_condition',
                       'species_pcr_complex_id',
                       'species_pcr_sibling_species',
                       'species_pcr_test_by',
                       'species_maldi_tof_complex_id',
                       'species_maldi_tof_sibling_species',
                       'species_maldi_tof_log_score',
                       'species_maldi_tof_added_to_db',
                       'species_maldi_tof_query_date',
                       'species_maldi_tof_repeat_pcr',
                       'species_maldi_tof_test_by',
                       'species_maldi_tof_qc',
                       'plasmodium_elisa_results',
                       'plasmodium_elisa_test_by',
                       'plasmodium_maldi_tof_results',
                       'plasmodium_maldi_tof_log_score',
                       'plasmodium_maldi_tof_added_to_db',
                       'plasmodium_maldi_tof_query_date',
                       'plasmodium_maldi_tof_test_by',
                       'plasmodium_maldi_tof_qc',
                       'plasmodium_maldi_pcr_results',
                       'plasmodium_maldi_pcr_test_by',
                       'bloodmeal_elisa_results',
                       'bloodmeal_elisa_spcecifics',
                       'bloodmeal_elisa_test_by',
                       'bloodmeal_maldi_tof_results',
                       'bloodmeal_maldi_tof_log_score',
                       'bloodmeal_maldi_tof_added_to_db',
                       'bloodmeal_maldi_tof_query_date',
                       'bloodmeal_maldi_tof_repeat_pcr',
                       'bloodmeal_maldi_tof_test_by',
                       'bloodmeal_maldi_tof_qc'
        ],
        'RC Individual Mosquitoes': ['date_of_collection', 
                       'sample_id', 
                       'site_of_collection',
                       'cluster', 
                       'study_arm', 
                       'hh_id', 
                       'box_id',
                       'tube_position_id',
                       'species_complex_id',
                       'phsyiological_status',
                       'sample_condition',
                       'species_pcr_complex_id',
                       'species_pcr_sibling_species',
                       'species_pcr_test_by',
                       'species_maldi_tof_complex_id',
                       'species_maldi_tof_sibling_species',
                       'species_maldi_tof_log_score',
                       'species_maldi_tof_added_to_db',
                       'species_maldi_tof_query_date',
                       'species_maldi_tof_repeat_pcr',
                       'species_maldi_tof_test_by',
                       'species_maldi_tof_qc',
                       'oviposition_oviposited_yn',
                       'oviposition_day_oviposited',
                       'survival_dead_yn',
                       'survival_day_died',
                       'plasmodium_elisa_results',
                       'plasmodium_elisa_test_by',
                       'plasmodium_maldi_tof_results',
                       'plasmodium_maldi_tof_log_score',
                       'plasmodium_maldi_tof_added_to_db',
                       'plasmodium_maldi_tof_query_date',
                       'plasmodium_maldi_tof_test_by',
                       'plasmodium_maldi_tof_qc',
                       'plasmodium_pcr_results',
                       'plasmodium_pcr_test_by',
                       'bloodmeal_elisa_results',
                       'bloodmeal_elisa_spcecifics',
                       'bloodmeal_elisa_test_by',
                       'bloodmeal_maldi_tof_results',
                       'bloodmeal_maldi_tof_log_score',
                       'bloodmeal_maldi_tof_added_to_db',
                       'bloodmeal_maldi_tof_query_date',
                       'bloodmeal_maldi_tof_repeat_pcr',
                       'bloodmeal_maldi_tof_test_by',
                       'bloodmeal_maldi_tof_qc'
                       ],
        'RC Pooled Mosquitoes': ['date_of_collection', 
                       'pool_sample_id',
                       'pool_sample_id_ind_mosquitoes_enum', 
                       'site_of_collection',
                       'cluster',
                       'study_arm', 
                       'hh_id', 
                       'box_id',
                       'tube_position_id',
                       'num_mosquitoes_per_tube_listed',
                       'species_complex_id',
                       'condition_of_pooled_sample',
                       'num_mosquitoes_per_tube_final',
                       'phsyiological_status',
                       'sample_condition',
                       'species_pcr_complex_id',
                       'species_pcr_sibling_species',
                       'species_pcr_test_by',
                       'species_maldi_tof_complex_id',
                       'species_maldi_tof_sibling_species',
                       'species_maldi_tof_log_score',
                       'species_maldi_tof_added_to_db',
                       'species_maldi_tof_query_date',
                       'species_maldi_tof_repeat_pcr',
                       'species_maldi_tof_test_by',
                       'species_maldi_tof_qc',
                       'plasmodium_elisa_results',
                       'plasmodium_elisa_test_by',
                       'plasmodium_maldi_tof_results',
                       'plasmodium_maldi_tof_log_score',
                       'plasmodium_maldi_tof_added_to_db',
                       'plasmodium_maldi_tof_query_date',
                       'plasmodium_maldi_tof_test_by',
                       'plasmodium_maldi_tof_qc',
                       'plasmodium_pcr_results',
                       'plasmodium_pcr_test_by',
                       'bloodmeal_elisa_results',
                       'bloodmeal_elisa_spcecifics',
                       'bloodmeal_elisa_test_by',
                       'bloodmeal_maldi_tof_results',
                       'bloodmeal_maldi_tof_log_score',
                       'bloodmeal_maldi_tof_added_to_db',
                       'bloodmeal_maldi_tof_query_date',
                       'bloodmeal_maldi_tof_repeat_pcr',
                       'bloodmeal_maldi_tof_test_by',
                       'bloodmeal_maldi_tof_qc'],
        'Insecticide Resistance': [
            'date_of_collection', 
            'method_of_collection',
            'synergist',
            'synergist_assay',
            'insecticide',
            'insecticide_concentration',
            'replicate',
            'alive_or_dead',
            'tube_id',
            'mosquitoes_exposed',
            'num_mosquito_per_tube',
            'mosquito_id',
            'is_mosquito_available',
            'species_pcr_complex_id',
            'species_pcr_sibling_species',
            'species_pcr_test_by',
            'plasmodium_pcr_results',
            'plasmodium_pcr_test_by',
            'l119f_gste2_detection_pcr_results',
            'kdr_detection_pcr_results',
            'cyp6pa_detection_first_pcr_results',
            'cyp6pa_detection_second_pcr_results',
            'cyp6pb_detection_first_pcr_results',
            'cyp6pb_detection_second_pcr_results',
            '6.5kb_sv_detection_pcr_results'
        ]

}

CURR_TIME = datetime.now()
GSHEETS_TARGET = 'ento-labs' + '-' + 'production'

# authorize keyfile
gc = pg.authorize(service_file='key/key.json')

# get output
outdir = 'ento_labs_output'

# open gsheets
sh = gc.open(GSHEETS_TARGET)
worksheets = sh.worksheets()

# parse through worksheets
for worksheet in worksheets:
    if not worksheet.hidden:
        # create filename
        strings = (worksheet.title).split()
        outname = '_'.join([s.lower() for s in strings]) + '.csv'
        fullname = os.path.join(outdir, outname)  
        
        # store dataset
        data = sh.worksheet_by_title(worksheet.title).get_as_df().iloc[1:]
        data.columns = VARNAME_DICT[worksheet.title]
        data.to_csv(fullname,index = False)