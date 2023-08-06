from dsmr_parser import obis_references

class Entity():
  """
  Entity reading values from DSMR telegram.
  """

  def __init__(self, name, obis):
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
    value = self.get_dsmr_object_attr('value')

    if self._obis == obis_references.ELECTRICITY_ACTIVE_TARIFF:
      return self.translate_tariff(value)

    try:
      value = round(float(value), 2)

    except TypeError:
      pass

    return value

  @property
  def unit(self):
    """Return the unit of measurement of this entity, if any."""
    return self.get_dsmr_object_attr('unit')

  @staticmethod
  def translate_tariff(value):
    """Convert 2/1 to normal/low."""
    # DSMR V2.2: Note: Rate code 1 is used for low rate and rate code 2 is
    # used for normal rate.
    if value == '0002':
      return 'normal'
    elif value == '0001':
      return 'low'
    else:
      return None