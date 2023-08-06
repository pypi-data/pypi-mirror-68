import os
import time
import json
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V2_2
from dsmr_parser import obis_references as obis_ref

from dsmr.telegram import Entity

class DSMRReader():

    def __init__(self, device = '/dev/ttyUSB0', serial_settings = SERIAL_SETTINGS_V2_2, telegram_specification = telegram_specifications.V2_2, debug=False):
        self.device                 = device
        self.serial_settings        = serial_settings
        self.telegram_specification = telegram_specification
        self.debug                  = debug

        self.serial_reader = SerialReader(
            device                 = self.device,
            serial_settings        = self.serial_settings,
            telegram_specification = self.telegram_specification
        )

        self.obis_mapping_json = [
            [
                'power_consumption',
                obis_ref.CURRENT_ELECTRICITY_USAGE
            ],
            [
                'power_production',
                obis_ref.CURRENT_ELECTRICITY_DELIVERY
            ],
            [
                'power_tariff',
                obis_ref.ELECTRICITY_ACTIVE_TARIFF
            ],
            [
                'power_consumption_low',
                obis_ref.ELECTRICITY_USED_TARIFF_1
            ],
            [
                'power_consumption_normal',
                obis_ref.ELECTRICITY_USED_TARIFF_2
            ],
            [
                'power_production_low',
                obis_ref.ELECTRICITY_DELIVERED_TARIFF_1
            ],
            [
                'power_production_normal',
                obis_ref.ELECTRICITY_DELIVERED_TARIFF_2
            ],
            [
                'gas_consumption',
                obis_ref.GAS_METER_READING
            ]
        ]

        self.obis_mapping = [
            [
                'Power Consumption',
                obis_ref.CURRENT_ELECTRICITY_USAGE
            ],
            [
                'Power Production',
                obis_ref.CURRENT_ELECTRICITY_DELIVERY
            ],
            [
                'Power Tariff',
                obis_ref.ELECTRICITY_ACTIVE_TARIFF
            ],
            [
                'Power Consumption (low)',
                obis_ref.ELECTRICITY_USED_TARIFF_1
            ],
            [
                'Power Consumption (normal)',
                obis_ref.ELECTRICITY_USED_TARIFF_2
            ],
            [
                'Power Production (low)',
                obis_ref.ELECTRICITY_DELIVERED_TARIFF_1
            ],
            [
                'Power Production (normal)',
                obis_ref.ELECTRICITY_DELIVERED_TARIFF_2
            ]
            # ,
            # [
            #     'Power Consumption Phase L1',
            #     obis_ref.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE
            # ],
            # [
            #     'Power Consumption Phase L2',
            #     obis_ref.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE
            # ],
            # [
            #     'Power Consumption Phase L3',
            #     obis_ref.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE
            # ],
            # [
            #     'Power Production Phase L1',
            #     obis_ref.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE
            # ],
            # [
            #     'Power Production Phase L2',
            #     obis_ref.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE
            # ],
            # [
            #     'Power Production Phase L3',
            #     obis_ref.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE
            # ],
            # [
            #     'Long Power Failure Count',
            #     obis_ref.LONG_POWER_FAILURE_COUNT
            # ],
            # [
            #     'Voltage Sags Phase L1',
            #     obis_ref.VOLTAGE_SAG_L1_COUNT
            # ],
            # [
            #     'Voltage Sags Phase L2',
            #     obis_ref.VOLTAGE_SAG_L2_COUNT
            # ],
            # [
            #     'Voltage Sags Phase L3',
            #     obis_ref.VOLTAGE_SAG_L3_COUNT
            # ],
            # [
            #     'Voltage Swells Phase L1',
            #     obis_ref.VOLTAGE_SWELL_L1_COUNT
            # ],
            # [
            #     'Voltage Swells Phase L2',
            #     obis_ref.VOLTAGE_SWELL_L2_COUNT
            # ],
            # [
            #     'Voltage Swells Phase L3',
            #     obis_ref.VOLTAGE_SWELL_L3_COUNT
            # ],
            # [
            #     'Voltage Phase L1',
            #     obis_ref.INSTANTANEOUS_VOLTAGE_L1
            # ],
            # [
            #     'Voltage Phase L2',
            #     obis_ref.INSTANTANEOUS_VOLTAGE_L2
            # ],
            # [
            #     'Voltage Phase L3',
            #     obis_ref.INSTANTANEOUS_VOLTAGE_L3
            # ],
            ,
            [
              'Gas Consumption',
              obis_ref.GAS_METER_READING
            ]
        ]

        # self.entities = [Entity(name, obis) for name, obis in self.obis_mapping]
        self.entities = [Entity(name, obis) for name, obis in self.obis_mapping_json]

    def __update_entities_telegram(self, telegram):
        '''
        Update entities with latest telegram and trigger state update.
        '''
        # Make all entities aware of new telegram
        for entity in self.entities:
            entity.telegram = telegram
        

    def read(self):
        '''
        Read DSMR telegrams
        '''
        try:
          if self.debug:
            print('>> Reading DSMR in debug mode') 

          for telegram in self.serial_reader.read():

            self.__update_entities_telegram(telegram)

            data = dict()

            # the combination of entities == dict/json
            for entity in self.entities:
                if entity.unit == 'kW':
                    value = float(entity.state()) * 1000
                else:
                    value = entity.state()

                # print(f'{entity.name} == {value} {entity.unit or ""}')

                data[entity.name] = f'{value} {entity.unit or ""}'.strip()

            print(json.dumps(data, indent=2))


          #   print('=' * 80)

        except Exception as e:
          print(f'[ERROR] {str(e)}')
        
        