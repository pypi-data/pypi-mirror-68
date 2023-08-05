# user_manager.py
# Ethan Guthrie
# 04/06/2020
""" Allows user and permission settings to be configured. """

class UserManager:
    """ Class for the UserManager object. """
    def __init__(self, login_object):
        """ Initializes the UserManager object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_user.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_user"
    def disable_radius(self):
        """ Disables RADIUS authentication. """
        # Generating payload.
        user_data = {
            "radius": "0"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_radius(self):
        """ Enables RADIUS authentication. """
        # Generating payload.
        user_data = {
            "radius": "1"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_permissions(self, user="Administrator"):
        """ GETs the permissions for the provided user. """
        # Creating permission type list.
        permission_types = ["Login User", "Framed User", "Callback Login", "Callback Framed",
                            "Outbound", "Administrative", "NAS Prompt", "Authenticate Only",
                            "Callback NAS Prompt", "Call Check", "Callback Administrative"]
        # Initializing dictionary.
        user_permissions = {}
        # Setting user type string.
        if user == "Administrator":
            user_type = "RTA"
        elif user == "Device Manager":
            user_type = "RTD"
        elif user == "Read Only User":
            user_type = "RTU"
        else:
            return -1

        # GETing User Manager page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for permissions.
        for i in range(0, len(permission_types)):
            addr = resp.text.find("NAME=\"USR_" + user_type + "_" + str(i + 1) + "\"")
            start_index = str(resp.text).find("VALUE=", addr) + 7
            end_index = str(resp.text).find("\"", start_index)
            user_permissions[permission_types[i]] = bool(int(resp.text[start_index:end_index]))

        return user_permissions
    def get_server_info(self):
        """ GETs information about the RADIUS server. """
        # GETing User Manager page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for server IP.
        addr = resp.text.find("NAME=\"USR_RADSRV\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        server_ip = resp.text[start_index:end_index]

        # Parsing response for server secret.
        addr = resp.text.find("NAME=\"USR_RADSEC\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        server_secret = resp.text[start_index:end_index]

        # Parsing response for server port.
        addr = resp.text.find("NAME=\"USR_RADPRT\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        server_port = int(resp.text[start_index:end_index])

        # Generating dictionary.
        server_data = {
            "IP": server_ip,
            "Secret": server_secret,
            "Port": server_port
        }

        return server_data
    def get_user(self, user="Administrator"):
        """ GETs information about the provided user. """
        # Setting user num string.
        if user == "Administrator":
            num = "1"
        elif user == "Device Manager":
            num = "2"
        elif user == "Read Only User":
            num = "3"
        else:
            return -1

        # GETing User Manager page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for user name.
        addr = resp.text.find("NAME=\"account" + num + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        name = resp.text[start_index:end_index]

        # Parsing response for user password.
        addr = resp.text.find("NAME=\"passwd" + num + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        password = resp.text[start_index:end_index]

        # Parsing response for user WAN access.
        addr = resp.text.find("NAME=\"limit" + num + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        wan_access = bool(int(resp.text[start_index:end_index]))

        # Generating dictionary.
        user_data = {
            "Type": user,
            "Name": name,
            "Password": password,
            "WAN Access": wan_access
        }

        return user_data
    def set_permissions(self, user="Administrator", login_user=False,
                        framed_user=False, callback_login=False, callback_framed=False,
                        outbound=False, administrative=False, nas_prompt=False,
                        authenticate_only=False, callback_nas_prompt=False,
                        call_check=False, callback_administrative=False):
        """ Sets permissions for the provided user. """
        # Setting user type string.
        if user == "Administrator":
            user_type = "RTA"
        elif user == "Device Manager":
            user_type = "RTD"
        elif user == "Read Only User":
            user_type = "RTU"
        else:
            return -1

        # Generating payload.
        user_data = {
            "USR_" + user_type + "_1": str(int(login_user)),
            "USR_" + user_type + "_2": str(int(framed_user)),
            "USR_" + user_type + "_3": str(int(callback_login)),
            "USR_" + user_type + "_4": str(int(callback_framed)),
            "USR_" + user_type + "_5": str(int(outbound)),
            "USR_" + user_type + "_6": str(int(administrative)),
            "USR_" + user_type + "_7": str(int(nas_prompt)),
            "USR_" + user_type + "_8": str(int(authenticate_only)),
            "USR_" + user_type + "_9": str(int(callback_nas_prompt)),
            "USR_" + user_type + "_10": str(int(call_check)),
            "USR_" + user_type + "_11": str(int(callback_administrative))
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def set_server_info(self, server, secret, port):
        """ Sets information for the RADIUS server. """
        # Generating payload.
        user_data = {
            "radius": "1",
            "USR_RADSRV": server,
            "USR_RADSEC": secret,
            "USR_RADPRT": str(port)
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_user(self, username, passwd, wan_access=False, user="Administrator"):
        """ Sets information for the provided user. """
        # Setting user num string.
        if user == "Administrator":
            num = "1"
        elif user == "Device Manager":
            num = "2"
        elif user == "Read Only User":
            num = "3"
        else:
            return -1

        # Generating payload.
        user_data = {
            "account" + num: username,
            "passwd" + num: passwd,
            "limit" + num: str(int(wan_access))
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
