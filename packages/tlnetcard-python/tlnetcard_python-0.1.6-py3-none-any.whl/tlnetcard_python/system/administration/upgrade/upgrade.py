# upgrade.py
# Ethan Guthrie
# 04/16/2020
""" Allows SNMP Device Firmware to be upgraded. """

# Standard library.
from os.path import isfile

class Upgrade:
    """ Class for the Upgrade object. """
    def __init__(self, login_object):
        """ Initializes the Upgrade object. """
        self._login_object = login_object
        self._post_url = login_object.get_base_url() + "/delta/adm_upgrade"
    def upgrade_snmp_firmware(self, path="ups-tl-01_12_05c.bin"):
        """ Upgrades SNMP Device Firmware. """
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Creating upload payload.
        upgrade_data = {
            'UL_F_NETWORK': path
        }

        # Uploading SNMP configuration.
        self._login_object.get_session().post(self._post_url, data=upgrade_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        print("NOTE: The card at " + self._login_object.get_base_url()
              + " will be offline for approximately 1 minute.")

        return 0
