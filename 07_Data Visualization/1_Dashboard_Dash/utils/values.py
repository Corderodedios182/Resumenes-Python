# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 12:02:16 2022

@author: cflorelu
"""
signals = ["Time",
           "s4_an2l_ramactwidthboc_C1611", #ancho plataforma
           "s4_hmo_pmac_fmplc_m5043_an2l_hmo_castspeed_C0470", #velodicdad línea
           "grade_number_C1074659440", #grado_acero
           "s4_drv_net_a_ea_seg12_torque_reff_C1074856029", #señales de línea 4 y segmento 12
           "s4_drv_net_a_ea_seg12_torque_ref_C1074856020",
           "hsa12_loopout_eslsprtrdactpst_C1075052642",
           "hsa12_loopout_esrsprtrdactpst_C1075052644",
           "hsa12_loopout_eslsprtrdactrod_C1075052643",
           "hsa12_loopout_esrsprtrdactrod_C1075052645",
           "hsa12_loopout_dslsprtrdactpst_C1075052646",
           "hsa12_loopout_dsrsprtrdactpst_C1075052648",
           "hsa12_loopout_dslsprtrdactrod_C1075052647",
           "hsa12_loopout_dsrsprtrdactrod_C1075052649",
           "hsa12_loopout_eslsactfrc_C1075052638",
           "hsa12_loopout_esrsactfrc_C1075052639",
           "hsa12_loopout_dslsactfrc_C1075052640",
           "hsa12_loopout_dsrsactfrc_C1075052641",
           "hsa12_group_hsaactgauts_C1075052605",
           "hsa12_group_hsaactgaubs_C1075052606",
           "hsa12_group_hsarefgaubs_C1075052604",
           "hsa12_group_hsarefgauts_C1075052603",
           "hsa12_loopout_dslsactpos_C1075052636",
           "hsa12_loopout_dsrsactpos_C1075052637",
           "hsa12_loopout_eslsactpos_C1075052634",
           "hsa12_loopout_esrsactpos_C1075052635",
           "s4_drv_net_a_ea_seg12_linear_speed_C1074856027",
           "s4_drv_net_a_ea_seg012_trq_cmd_C1611726945",
           "s4_drv_net_a_ea_seg12_actual_current_C1074856026",
           "s4_drv_net_a_ea_seg12_speed_ref_C1074856019",
           "hsa12_group_hsasegid_C1075052607"]

#Values Azure
config_values = {'Signals': {
                    'account_name': 'prodllanding',
                    'sas_token': 'sp=rl&st=2022-04-05T18:14:27Z&se=2023-01-01T03:14:27Z&sv=2020-08-04&sr=c&sig=%2Fqe%2F4HbbTL6Tvx2oYNkF2tV7Qjjdj%2BsO2fDdldVinUU%3D', 
                    'source': 'abfs://arg-landing-iba-sns-ccd2@prodllanding.blob.core.windows.net/date={date_}',
                    'columns_file': signals,
                    'columns_order': signals,
                    'columns_to_date': ['Time'],
                    'skip_rows': 0,
                    'output_ddf': 'ddf'
                    },
                'May22': {
                    'account_name': 'prodltransient',
                    'sas_token': 'sp=racwdli&st=2022-09-19T17:56:44Z&se=2023-07-30T01:56:44Z&sv=2021-06-08&sr=c&sig=doxPebIqOWxap%2BaZlvgsCqcEw51f7D2Jf26ObC%2FCSSQ%3D',
                    'source': 'abfs://mtto-predictivo-input-arg@prodltransient.blob.core.windows.net/202205_ccd2_iba_ideal.csv',
                    'columns_file': '',
                    'columns_new': '',
                    'columns_to_date': ['Time'],
                    'skip_rows': 0,
                    'output_ddf': 'ddf_may'}
                }

