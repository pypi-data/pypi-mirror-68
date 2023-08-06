import os
import json
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V2_2
from dsmr_parser import obis_references as obis_ref

class DSMREntity(object):
  """
  Entity reading values from DSMR telegram.
  """

  def __init__(self, name, obis):
    """Initialize entity."""
    self._name = name
    self._obis = obis
    self.telegram = {}

  def get_dsmr_object_attr(self, attribute):
    """Read attribute from last received telegram for this DSMR object."""
    # Make sure telegram contains an object for this entities obis
    if self._obis not in self.telegram:
        return None

    # Get the attribute value if the object has it
    dsmr_object = self.telegram[self._obis]
    return getattr(dsmr_object, attribute, None)

  @property
  def name(self):
    """Return the name of the sensor."""
    return self._name

  def state(self):
    """Return the state of sensor, if available, translate if needed."""
    from dsmr_parser import obis_references as obis

    value = self.get_dsmr_object_attr('value')

    if self._obis == obis.ELECTRICITY_ACTIVE_TARIFF:
      return self.translate_tariff(value)

    try:
      value = round(float(value), 2)
    except TypeError:
      pass

    if value is not None:
      return value

    return None

  @property
  def unit_of_measurement(self):
    """Return the unit of measurement of this entity, if any."""
    return self.get_dsmr_object_attr('unit')

  @staticmethod
  def translate_tariff(value):
    """Convert 2/1 to normal/low."""
    # DSMR V2.2: Note: Rate code 1 is used for low rate and rate code 2 is
    # used for normal rate.
    if value == '0002':
      return 'normal'
    if value == '0001':
      return 'low'

    return None




class DSMRReader():
    def __init__(self, device = '/dev/ttyUSB0', serial_settings = SERIAL_SETTINGS_V2_2, telegram_specification = telegram_specifications.V2_2):
        self.device                 = device
        self.serial_settings        = serial_settings
        self.telegram_specification = telegram_specification

        self.serial_reader = SerialReader(
            device                 = self.device,
            serial_settings        = self.serial_settings,
            telegram_specification = self.telegram_specification
        )

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

        self.devices = [DSMREntity(name, obis) for name, obis in self.obis_mapping]

    def __update_entities_telegram(self, telegram):
        '''
        Update entities with latest telegram and trigger state update.
        '''
        # Make all device entities aware of new telegram
        for device in self.devices:
            device.telegram = telegram

        

    def read(self):
        '''
        Read DSMR telegrams
        '''

        try:
          for telegram in self.serial_reader.read():

            self.__update_entities_telegram(telegram)

            for device in self.devices:
                if device.unit_of_measurement == 'kW':
                    value = float(device.state()) * 1000
                else:
                    value = device.state()
                    print(f'{device.name} == {value} {device.unit_of_measurement or ""}')


            print('=' * 80)

        except Exception as e:
          print(str(e))
        
        