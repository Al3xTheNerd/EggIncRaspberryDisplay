from utils import ei_pb2 as ei
import requests
from base64 import b64decode, b64encode
from google.protobuf.json_format import MessageToDict
import zlib
client_version = 64
s = requests.Session()

def open_authenticated_message(message):
    # Create The Authenticated Message Object
    authenticated_message = ei.AuthenticatedMessage()

    # Parse The Information
    authenticated_message.ParseFromString(b64decode(message))
    
    # Check if message is compressed
    if authenticated_message.compressed == 1:
        # Return Decompressed Message
        return(zlib.decompress(authenticated_message.message))
    
    # Return Only The Message
    return authenticated_message.message


def basicRequestInfo(ei_user_id):
    """
    Used in some requests to verify identity \n
    Returns A Dictionary
    """
    basicRequestInfo = ei.BasicRequestInfo()
    # Define requred fields for rinfo
    basicRequestInfo.ei_user_id = ei_user_id # 1
    basicRequestInfo.client_version = client_version # 2
    basicRequestInfo.version = "1.31"
    basicRequestInfo.build = "111284"
    basicRequestInfo.platform = "IOS"
    basicRequestInfo.country = "US"
    basicRequestInfo.language = "en"
    basicRequestInfo.debug = False
    # Return object
    return basicRequestInfo


def get_first_contact(ei_user_id):
    """
    URL : https://www.auxbrain.com/ei/bot_first_contact \n
    Used to pull First Contact info (Soul Eggs, Golden Eggs, Artifact Lists, etc.) \n
    Returns A Dictionary
    """
    # Create The Request And Response Objects
    first_contact_request = ei.EggIncFirstContactRequest()
    first_contact_response = ei.EggIncFirstContactResponse()

    # Set The Request Parameters
    first_contact_request.ei_user_id = ei_user_id
    first_contact_request.client_version = client_version

    # Push And Save The Request
    response = s.post("https://www.auxbrain.com/ei/bot_first_contact", data = { 'data' : b64encode(first_contact_request.SerializeToString()).decode('utf-8') })

    # Parse The Response
    first_contact_response.ParseFromString(b64decode(response.text))

    # Return That Which You Seek
    return MessageToDict(first_contact_response)


def get_periodicals(ei_user_id):
    """
    URL : https://www.auxbrain.com/ei/get_periodicals \n
    Used to pull Periodicals \n
    Returns A Dictionary
    """
    # Create The Request And Response Objects
    get_periodicals_request = ei.GetPeriodicalsRequest()
    periodicals_response = ei.PeriodicalsResponse()

    # Set The Request Parameters
    get_periodicals_request.user_id = ei_user_id
    get_periodicals_request.current_client_version = client_version

    # Push And Save The Request
    response = s.post("https://www.auxbrain.com/ei/get_periodicals", data = { 'data' : b64encode(get_periodicals_request.SerializeToString()).decode('utf-8') })
    
    # Deauthenticate And Parse The Response
    periodicals_response.ParseFromString(open_authenticated_message(response.text))

    # Return That Which You Seek
    return MessageToDict(periodicals_response)


def get_config(ei_user_id):
    """
    URL : https://www.auxbrain.com/ei/get_config \n
    Used to pull Game Config \n
    Returns A Dictionary
    """
    # Create The Request And Response Objects
    config_request = ei.ConfigRequest()
    config_response = ei.ConfigResponse()

    # Set The Request Parameters
    config_request.rinfo.MergeFrom(basicRequestInfo(ei_user_id))
    config_request.soul_eggs = 100
    config_request.artifacts_enabled = True
    config_request.fuel_tank_unlocked = True
    # Push And Save The Request
    response = s.post("https://www.auxbrain.com/ei/get_config", data = { 'data' : b64encode(config_request.SerializeToString()).decode('utf-8') })
    
    # Deauthenticate And Parse The Response
    config_response.ParseFromString(open_authenticated_message(response.text))

    # Return That Which You Seek
    return MessageToDict(config_response)


def get_afx_config(ei_user_id):
    """
    URL : https://www.auxbrain.com/ei_afx/config \n
    Used to pull Game Artifacts Config \n
    Returns A Dictionary
    """
    # Create The Request And Response Objects
    afx_config_request = ei.ArtifactsConfigurationRequest()
    afx_config_response = ei.ArtifactsConfigurationResponse()

    # Set The Request Parameters
    afx_config_request.rinfo.MergeFrom(basicRequestInfo(ei_user_id))
    
    # Push And Save The Request
    response = s.post("https://www.auxbrain.com/ei_afx/config", data = { 'data' : b64encode(afx_config_request.SerializeToString()).decode('utf-8') })
    
    # Deauthenticate And Parse The Response
    afx_config_response.ParseFromString(open_authenticated_message(response.text))

    # Return That Which You Seek
    return MessageToDict(afx_config_response)


def get_daily_gift_info():
    """
    URL : https://www.auxbrain.com/ei/daily_gift_info \n
    Used to determine Current Day Number and Seconds Until Next Day \n
    Returns A Dictionary
    """
    # Create The Response Object
    daily_gift_info_response = ei.DailyGiftInfo()

    # Push And Save The Request
    response = requests.post("https://www.auxbrain.com/ei/daily_gift_info")

    # Parse The Response
    daily_gift_info_response.ParseFromString(b64decode(response.text))

    # Return That Which You Seek
    return MessageToDict(daily_gift_info_response)


def get_coop_status(ei_user_id, contract_identifier, coop_identifier):
    """
    URL : https://www.auxbrain.com/ei/coop_status \n
    Used to pull Current Coop Information \n
    Note: Coop Name must be all lowercase \n
    Returns A Dictionary
    """
    # Create The Request And Response Objects
    coop_info_request = ei.ContractCoopStatusRequest()
    coop_info_response = ei.ContractCoopStatusResponse()

    # Set The Request Parameters
    coop_info_request.contract_identifier = contract_identifier
    coop_info_request.coop_identifier = coop_identifier
    coop_info_request.user_id = ei_user_id
    coop_info_request.client_version = client_version


    # Push And Save The Request
    response = s.post("https://www.auxbrain.com/ei/coop_status", data = { 'data' : b64encode(coop_info_request.SerializeToString()).decode('utf-8') })
    
    # Deauthenticate And Parse The Response
    coop_info_response.ParseFromString(open_authenticated_message(response.text))

    # Return That Which You Seek
    return MessageToDict(coop_info_response)

def get_sub_status(ei_user_id):
    """
    URL : https://www.auxbrain.com/ei_srv/subscription_status/$EI \n
    Used to determine Current Day Number and Seconds Until Next Day \n
    Returns A Dictionary
    """
    # Create The Response Object
    subInfo = ei.UserSubscriptionInfo()

    # Push And Save The Request
    response = requests.post(f"https://www.auxbrain.com/ei_srv/subscription_status/{ei_user_id}")
    subInfo.ParseFromString(open_authenticated_message(response.text))

    # Return That Which You Seek
    return MessageToDict(subInfo)