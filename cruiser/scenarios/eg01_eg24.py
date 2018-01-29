from cruiser.inputfiles import InputFile, inparam


class Simulation(InputFile):
    """EG01 -> EG24 transition Scenario"""

    scenario = 'EG01-EG24'

    @inparam(default=3024, widget='IntSlider', min=1, max=30240)
    def duration(self, value):
        self.sim['simulation']['control']['duration'] = value

    @inparam(default=1, widget='IntSlider', min=1, max=12)
    def startmonth(self, value):
        self.sim['simulation']['control']['startmonth'] = value

    @inparam(default=1e299, widget='FloatSlider', min=0.0, max=1e299)
    def mine_throughput(self, value):
        self.sim['simulation']['facility'][0]['config']['Source']['throughput'] = value

    @inparam(default=1E100, widget='FloatSlider', min=0.0, max=1E100)
    def enrichment_swu_capacity(self, value):
        self.sim['simulation']['facility'][1]['config']['Enrichment']['swu_capacity'] = value

    @inparam(default=1e100, widget='FloatSlider', min=0.0, max=10, step=0.1, readout_format='.4f')
    def mixer_throughput(self, value):
        self.sim['simulation']['facility'][2]['config']['mixer']['throughput'] = value

    @inparam(default=1E100, widget='FloatSlider', min=0.0, max=1E100)
    def separations_throughput(self, value):
        self.sim['simulation']['facility'][1]['config']['separations']['throughput'] = value

    @inparam(default=.003, widget='FloatSlider', min=0.0, max=0.00711, step=0.0001, readout_format='.4f')
    def enrichment_tails_assay(self, value):
        self.sim['simulation']['facility'][1]['config']['Enrichment']['tails_assay'] = value

    def default(self):
        return {
 'simulation': {
  'archetypes': {
   'spec': [
    {'lib': 'cycamore', 'name': 'Source'},
    {'lib': 'cycamore', 'name': 'Sink'},
    {'lib': 'cycamore', 'name': 'Reactor'},
    {'lib': 'cycamore', 'name': 'Mixer'},
    {'lib': 'agents', 'name': 'NullRegion'},
    {'lib': 'agents', 'name': 'NullInst'},
    {'lib': 'cycamore', 'name': 'Separations'},
    {'lib': 'cycamore', 'name': 'DeployInst'},
    {'lib': 'cycamore', 'name': 'Separations'},
    {'lib': 'cycamore', 'name': 'Enrichment'},
    {'lib': 'cycamore', 'name': 'FuelFab'},
    {'lib': 'cycamore', 'name': 'Storage'},
   ],
  },
  'control': {'duration': '3024', 'startmonth': '1', 'startyear': '1959'},
  'facility': [
   {
    'config': {
     'Source': {
      'outcommod': 'natl_u',
      'outrecipe': 'natl_u_recipe',
      'throughput': '1e299',
     },
    },
    'name': 'mine',
   },
   {
    'config': {
     'Enrichment': {
      'feed_commod': 'natl_u',
      'feed_recipe': 'natl_u_recipe',
      'initial_feed': '1e100',
      'product_commod': 'uox',
      'swu_capacity': '1e100',
      'tails_assay': '0.003',
      'tails_commod': 'tailings',
     },
    },
    'name': 'enrichment',
   },
   {
    'config': {
     'Mixer': {
      'in_streams': {
       'stream': [
        {
         'commodities': {
          'item': [
           {'commodity': 'uox_TRU', 'pref': '1.0'},
           {'commodity': 'sfr_TRU', 'pref': '1.0'},
          ],
         },
         'info': {'buf_size': '1e100', 'mixing_ratio': '0.1378678'},
        },
        {
         'commodities': {
          'item': [
           {'commodity': 'uox_U', 'pref': '1.0'},
           {'commodity': 'sfr_U', 'pref': '1.0'},
          ],
         },
         'info': {'buf_size': '1e100', 'mixing_ratio': '0.7724704512'},
        },
        {
         'commodities': {
          'item': [
           {'commodity': 'natl_u', 'pref': '1.0'},
           {'commodity': 'tailings', 'pref': '2.0'},
          ],
         },
         'info': {'buf_size': '1e100', 'mixing_ratio': '0.0896617488'},
        },
       ],
      },
      'out_buf_size': '1e100',
      'out_commod': 'sfr_fuel',
      'throughput': '1e100',
     },
    },
    'name': 'sfr_mixer',
   },
   {
    'config': {
     'Sink': {
      'capacity': '1e299',
      'in_commods': {
       'val': [
        'cool_uox_waste',
        'tailings',
        'reprocess_waste',
        'sfr_reprocess_waste',
       ],
      },
     },
    },
    'name': 'sink',
   },
   {
    'config': {
     'Separations': {
      'feed_commod_prefs': {'val': '1.0'},
      'feed_commods': {'val': 'cool_uox_waste'},
      'feed_recipe': 'uox_waste_recipe',
      'feedbuf_size': '1E100',
      'leftover_commod': 'reprocess_waste',
      'leftoverbuf_size': '1E100',
      'streams': {
       'item': [
        {
         'commod': 'uox_TRU',
         'info': {
          'buf_size': '1E100',
          'efficiencies': {
           'item': [
            {'comp': 'Np', 'eff': '.998'},
            {'comp': 'Am', 'eff': '.998'},
            {'comp': 'Cm', 'eff': '.998'},
            {'comp': 'Pu', 'eff': '.998'},
           ],
          },
         },
        },
        {
         'commod': 'uox_U',
         'info': {
          'buf_size': '1E100',
          'efficiencies': {'item': {'comp': 'U', 'eff': '.998'}},
         },
        },
       ],
      },
      'throughput': '1E100',
     },
    },
    'name': 'uox_reprocessing',
   },
   {
    'config': {
     'Separations': {
      'feed_commod_prefs': {'val': '2.0'},
      'feed_commods': {'val': 'cool_sfr_waste'},
      'feedbuf_size': '1E100',
      'leftover_commod': 'sfr_reprocess_waste',
      'leftoverbuf_size': '1E100',
      'streams': {
       'item': [
        {
         'commod': 'sfr_TRU',
         'info': {
          'buf_size': '1E100',
          'efficiencies': {
           'item': [
            {'comp': 'Np', 'eff': '.998'},
            {'comp': 'Am', 'eff': '.998'},
            {'comp': 'Cm', 'eff': '.998'},
            {'comp': 'Pu', 'eff': '.998'},
           ],
          },
         },
        },
        {
         'commod': 'sfr_U',
         'info': {
          'buf_size': '1E100',
          'efficiencies': {'item': {'comp': 'U', 'eff': '.998'}},
         },
        },
       ],
      },
      'throughput': '1E100',
     },
    },
    'name': 'sfr_reprocessing',
   },
   {
    'config': {
     'Storage': {
      'in_commods': {'val': 'uox_waste'},
      'max_inv_size': '1e299',
      'out_commods': {'val': 'cool_uox_waste'},
      'residence_time': '36',
      'throughput': '1e299',
     },
    },
    'name': 'uox_pool',
   },
   {
    'config': {
     'Storage': {
      'in_commods': {'val': 'sfr_waste'},
      'max_inv_size': '1e299',
      'out_commods': {'val': 'cool_sfr_waste'},
      'residence_time': '36',
      'throughput': '1e299',
     },
    },
    'name': 'sfr_pool',
   },
   {
    'config': {
     'Reactor': {
      'assem_size': '30160',
      'cycle_time': '18',
      'fuel_incommods': {'val': 'uox'},
      'fuel_inrecipes': {'val': 'uox_recipe'},
      'fuel_outcommods': {'val': 'uox_waste'},
      'fuel_outrecipes': {'val': 'uox_waste_recipe'},
      'fuel_prefs': {'val': '1.0'},
      'n_assem_batch': '1',
      'n_assem_core': '3',
      'power_cap': '1000',
      'refuel_time': '1',
     },
    },
    'lifetime': '960',
    'name': 'lwr',
   },
   {
    'config': {
     'Reactor': {
      'assem_size': '5838',
      'cycle_time': '14',
      'fuel_incommods': {'val': 'sfr_fuel'},
      'fuel_inrecipes': {'val': 'sfr_fuel_recipe'},
      'fuel_outcommods': {'val': 'sfr_waste'},
      'fuel_outrecipes': {'val': 'sfr_waste_recipe'},
      'fuel_prefs': {'val': '1.0'},
      'n_assem_batch': '1',
      'n_assem_core': '3',
      'power_cap': '400',
      'refuel_time': '1',
     },
    },
    'lifetime': '960',
    'name': 'fr',
   },
  ],
  'recipe': [
   {
    'basis': 'mass',
    'name': 'natl_u_recipe',
    'nuclide': [
     {'comp': '0.711', 'id': 'U235'},
     {'comp': '99.289', 'id': 'U238'},
    ],
   },
   {
    'basis': 'mass',
    'name': 'uox_recipe',
    'nuclide': [
     {'comp': '0.0002558883', 'id': 'U234'},
     {'comp': '0.0319885317', 'id': 'U235'},
     {'comp': '0.96775558', 'id': 'U238'},
    ],
   },
   {
    'basis': 'mass',
    'name': 'depleted_u',
    'nuclide': [
     {'comp': '0.003', 'id': 'U235'},
     {'comp': '0.997', 'id': 'U238'},
    ],
   },
   {
    'basis': 'mass',
    'name': 'mox_recipe',
    'nuclide': [
     {'comp': '9.7224110389438E-05', 'id': 'U234'},
     {'comp': '0.0039469814', 'id': 'U235'},
     {'comp': '0.0021573569', 'id': 'U236'},
     {'comp': '0.8665733427', 'id': 'U238'},
     {'comp': '0.0060565044', 'id': 'Np237'},
     {'comp': '0.0030040068', 'id': 'Pu238'},
     {'comp': '0.0606135352', 'id': 'Pu239'},
     {'comp': '0.0286774758', 'id': 'Pu240'},
     {'comp': '0.0134998465', 'id': 'Pu241'},
     {'comp': '0.0084034605', 'id': 'Pu242'},
     {'comp': '0.0042991968', 'id': 'Am241'},
     {'comp': '7.73428708584307E-06', 'id': 'Am242m'},
     {'comp': '0.0019207217', 'id': 'Am243'},
     {'comp': '6.47352555460846E-06', 'id': 'Cm243'},
     {'comp': '0.0006812961', 'id': 'Cm244'},
     {'comp': '5.48431266087054E-05', 'id': 'Cm245'},
    ],
   },
   {
    'basis': 'mass',
    'name': 'sfr_fuel_recipe',
    'nuclide': [
     {'comp': '8.12E-11', 'id': 'He4'},
     {'comp': '4.71E-09', 'id': 'U232'},
     {'comp': '0.0003', 'id': 'U234'},
     {'comp': '0.0004', 'id': 'U235'},
     {'comp': '0.0003', 'id': 'U236'},
     {'comp': '0.83', 'id': 'U238'},
     {'comp': '0.0007', 'id': 'Np237'},
     {'comp': '0.0022', 'id': 'Pu238'},
     {'comp': '0.0947', 'id': 'Pu239'},
     {'comp': '0.0518', 'id': 'Pu240'},
     {'comp': '0.0072', 'id': 'Pu241'},
     {'comp': '0.0057', 'id': 'Pu242'},
     {'comp': '0.0031', 'id': 'Am241'},
     {'comp': '0.0002', 'id': 'Am242m'},
     {'comp': '0.0016', 'id': 'Am243'},
     {'comp': '0.0000', 'id': 'Cm242'},
     {'comp': '0.0000', 'id': 'Cm243'},
     {'comp': '0.0011', 'id': 'Cm244'},
     {'comp': '0.0003', 'id': 'Cm245'},
     {'comp': '0.0001', 'id': 'Cm246'},
    ],
   },
   {
    'basis': 'mass',
    'name': 'uox_waste_recipe',
    'nuclide': [
     {'comp': '9.47457840128509E-07', 'id': 'He4'},
     {'comp': '9.78856442957042E-14', 'id': 'Ra226'},
     {'comp': '2.75087759176098E-20', 'id': 'Ra228'},
     {'comp': '5.57475193532078E-18', 'id': 'Pb206'},
     {'comp': '1.68592497990149E-15', 'id': 'Pb207'},
     {'comp': '3.6888358546006E-12', 'id': 'Pb208'},
     {'comp': '3.02386544437848E-19', 'id': 'Pb210'},
     {'comp': '8.47562285269577E-12', 'id': 'Th228'},
     {'comp': '2.72787861516683E-12', 'id': 'Th229'},
     {'comp': '2.6258831537493E-09', 'id': 'Th230'},
     {'comp': '4.17481422959E-10', 'id': 'Th232'},
     {'comp': '6.60770597104927E-16', 'id': 'Bi209'},
     {'comp': '3.0968621961773E-14', 'id': 'Ac227'},
     {'comp': '9.24658854635179E-10', 'id': 'Pa231'},
     {'comp': '0.000000001', 'id': 'U232'},
     {'comp': '2.21390148606282E-09', 'id': 'U233'},
     {'comp': '0.0001718924', 'id': 'U234'},
     {'comp': '0.0076486597', 'id': 'U235'},
     {'comp': '0.0057057461', 'id': 'U236'},
     {'comp': '0.9208590237', 'id': 'U238'},
     {'comp': '0.0006091729', 'id': 'Np237'},
     {'comp': '0.000291487', 'id': 'Pu238'},
     {'comp': '0.0060657301', 'id': 'Pu239'},
     {'comp': '0.0029058707', 'id': 'Pu240'},
     {'comp': '0.0017579218', 'id': 'Pu241'},
     {'comp': '0.0008638616', 'id': 'Pu242'},
     {'comp': '2.86487251922763E-08', 'id': 'Pu244'},
     {'comp': '6.44271331287386E-05', 'id': 'Am241'},
     {'comp': '8.53362027193319E-07', 'id': 'Am242m'},
     {'comp': '0.0001983912', 'id': 'Am243'},
     {'comp': '2.58988475560194E-05', 'id': 'Cm242'},
     {'comp': '0.000000771', 'id': 'Cm243'},
     {'comp': '8.5616190260478E-05', 'id': 'Cm244'},
     {'comp': '5.72174539442251E-06', 'id': 'Cm245'},
     {'comp': '7.29567535786554E-07', 'id': 'Cm246'},
     {'comp': '0.00000001', 'id': 'Cm247'},
     {'comp': '7.69165773748653E-10', 'id': 'Cm248'},
     {'comp': '4.2808095130239E-18', 'id': 'Cm250'},
     {'comp': '1.64992658175413E-12', 'id': 'Cf249'},
     {'comp': '2.04190913935875E-12', 'id': 'Cf250'},
     {'comp': '9.86556100338561E-13', 'id': 'Cf251'},
     {'comp': '6.57970721693466E-13', 'id': 'Cf252'},
     {'comp': '8.58461800264195E-08', 'id': 'H3'},
     {'comp': '4.05781943561107E-11', 'id': 'C14'},
     {'comp': '4.21681236076192E-11', 'id': 'Kr81'},
     {'comp': '3.44484671160181E-05', 'id': 'Kr85'},
     {'comp': '0.0007880649', 'id': 'Sr90'},
     {'comp': '0.0011409492', 'id': 'Tc99'},
     {'comp': '0.0002731878', 'id': 'I129'},
     {'comp': '0.0002300898', 'id': 'Cs134'},
     {'comp': '0.0006596706', 'id': 'Cs135'},
     {'comp': '0.0018169192', 'id': 'Cs137'},
     {'comp': '0.0477938151', 'id': 'H1'},
    ],
   },
   {
    'basis': 'mass',
    'name': 'sfr_waste_recipe',
    'nuclide': [
     {'comp': '78.122', 'id': 'U238'},
     {'comp': '13.809', 'id': 'Pu239'},
     {'comp': '0.15', 'id': 'Am241'},
     {'comp': '7.919', 'id': 'Cs137'},
    ],
   },
  ],
  'region': {
   'config': {'NullRegion': None},
   'institution': [
    {
     'config': {'NullInst': None},
     'initialfacilitylist': {
      'entry': [
       {'number': '1', 'prototype': 'mine'},
       {'number': '1', 'prototype': 'sink'},
       {'number': '1', 'prototype': 'enrichment'},
       {'number': '1', 'prototype': 'sfr_mixer'},
       {'number': '1', 'prototype': 'sfr_pool'},
       {'number': '1', 'prototype': 'uox_pool'},
       {'number': '1', 'prototype': 'uox_reprocessing'},
       {'number': '1', 'prototype': 'sfr_reprocessing'},
      ],
     },
     'name': 'sink_source_facilities',
    },
    {
     'config': {
      'DeployInst': {
       'build_times': {
        'val': [
         '12',
         '24',
         '36',
         '48',
         '60',
         '72',
         '84',
         '96',
         '108',
         '120',
         '132',
         '144',
         '156',
         '168',
         '180',
         '192',
         '204',
         '216',
         '228',
         '240',
         '252',
         '264',
         '276',
         '288',
         '300',
         '312',
         '324',
         '336',
         '348',
         '360',
         '372',
         '384',
         '396',
         '408',
         '420',
         '432',
         '444',
         '456',
         '468',
         '480',
         '492',
         '504',
         '516',
         '528',
         '540',
         '552',
         '564',
         '576',
         '588',
         '600',
         '672',
         '684',
         '696',
         '708',
         '720',
         '732',
         '744',
         '756',
         '768',
         '780',
         '792',
         '804',
         '816',
         '828',
         '840',
         '852',
         '864',
         '876',
         '888',
         '900',
         '912',
         '924',
         '936',
         '948',
         '960',
         '972',
         '984',
         '996',
         '1008',
         '1020',
         '1032',
         '1044',
         '1056',
         '1068',
         '1080',
         '1092',
         '1104',
         '1116',
         '1128',
         '1140',
         '1152',
         '1164',
         '1176',
         '1188',
         '1200',
         '1212',
         '1224',
         '1236',
         '1248',
         '1260',
         '1272',
         '1284',
         '1296',
         '1308',
         '1320',
         '1141',
         '1190',
         '1239',
         '1288',
         '1338',
         '1387',
         '1436',
         '1485',
         '1534',
         '1584',
         '1596',
         '1608',
         '1620',
         '1632',
         '1644',
         '1656',
         '1668',
         '1680',
         '1692',
         '1704',
         '1716',
         '1728',
         '1740',
         '1752',
         '1764',
         '1776',
         '1788',
         '1800',
         '1812',
         '1824',
         '1836',
         '1848',
         '1860',
         '1872',
        ],
       },
       'n_build': {
        'val': [
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '2',
         '1',
         '1',
         '1',
         '1',
         '1',
         '1',
         '1',
         '1',
         '1',
         '1',
         '2',
         '1',
         '1',
         '1',
         '1',
         '4',
         '3',
         '5',
         '3',
         '4',
         '3',
         '4',
         '4',
         '4',
         '3',
         '5',
         '3',
         '4',
         '3',
         '5',
         '3',
         '4',
         '4',
         '4',
         '3',
         '5',
         '3',
         '4',
         '3',
         '4',
         '3',
         '4',
         '3',
         '5',
         '3',
         '4',
         '3',
         '5',
         '3',
         '4',
         '4',
         '4',
         '3',
         '5',
         '2',
         '5',
         '5',
         '5',
         '5',
         '5',
         '5',
         '5',
         '5',
         '5',
         '5',
         '2',
         '3',
         '3',
         '2',
         '4',
         '3',
         '3',
         '3',
         '4',
         '4',
         '4',
         '4',
         '3',
         '3',
         '3',
         '3',
         '5',
         '5',
         '5',
         '5',
         '6',
         '6',
         '6',
         '6',
        ],
       },
       'prototypes': {
        'val': [
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
         'lwr',
        ],
       },
      },
     },
     'name': 'lwr_inst',
    },
    {
     'config': {
      'DeployInst': {
       'build_times': {
        'val': [
         '1884',
         '1896',
         '1908',
         '1920',
         '1932',
         '1944',
         '1956',
         '1968',
         '1980',
         '1992',
         '2004',
         '2016',
         '2028',
         '2040',
         '2052',
         '2064',
         '2076',
         '2088',
         '2100',
         '2112',
         '2124',
         '2136',
         '2148',
         '2160',
         '2172',
         '2184',
         '2196',
         '2208',
         '2220',
         '2232',
         '2244',
         '2256',
         '2268',
         '2280',
         '2292',
         '2304',
         '2316',
         '2328',
         '2340',
         '2352',
         '2364',
         '2376',
         '2388',
         '2400',
         '2412',
         '2424',
         '2436',
         '2448',
         '2460',
         '2472',
         '2484',
         '2496',
         '2508',
         '2520',
         '2532',
         '2544',
         '2556',
         '2568',
         '2580',
         '2592',
         '2604',
         '2616',
         '2628',
         '2640',
         '2652',
         '2664',
         '2676',
         '2688',
         '2700',
         '2712',
         '2724',
         '2736',
         '2748',
         '2760',
         '2772',
         '2784',
         '2796',
         '2808',
         '2820',
         '2832',
         '2844',
         '2856',
         '2868',
         '2880',
         '2892',
         '2904',
         '2916',
         '2928',
         '2940',
         '2952',
         '2964',
         '2976',
         '2988',
         '3000',
         '3012',
        ],
       },
       'n_build': {
        'val': [
         '17',
         '17',
         '17',
         '15',
         '18',
         '15',
         '17',
         '15',
         '20',
         '15',
         '17',
         '18',
         '18',
         '15',
         '21',
         '16',
         '18',
         '16',
         '20',
         '16',
         '20',
         '17',
         '22',
         '16',
         '18',
         '18',
         '22',
         '16',
         '20',
         '21',
         '20',
         '18',
         '22',
         '18',
         '13',
         '13',
         '15',
         '13',
         '15',
         '13',
         '15',
         '13',
         '16',
         '15',
         '16',
         '13',
         '16',
         '16',
         '16',
         '16',
         '16',
         '17',
         '17',
         '17',
         '17',
         '16',
         '18',
         '17',
         '18',
         '21',
         '20',
         '21',
         '20',
         '21',
         '22',
         '21',
         '22',
         '22',
         '22',
         '25',
         '21',
         '22',
         '22',
         '22',
         '30',
         '28',
         '32',
         '30',
         '31',
         '28',
         '32',
         '32',
         '32',
         '30',
         '35',
         '31',
         '32',
         '31',
         '37',
         '31',
         '34',
         '35',
         '35',
         '32',
         '39',
        ],
       },
       'prototypes': {
        'val': [
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
         'fr',
        ],
       },
      },
     },
     'name': 'fr_inst',
    },
   ],
   'name': 'USA',
  },
 },
}
