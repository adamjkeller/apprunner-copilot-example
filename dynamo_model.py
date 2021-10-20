from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from os import getenv

def get_region():
    from requests import get
    from json import loads
    try:
        region = loads(get(f'{getenv("ECS_CONTAINER_METADATA_URI_V4")}/task').text).get('AvailabilityZone')[:-1]
        print(region)
    except:
        print("Unable to source region from metadata, defaulting to us-east-1")
        region = 'us-east-1'
    return region

class UserModel(Model):
    """
    User table
    """
    class Meta:
        table_name = getenv('USERS_NAME')
        region = get_region()
        
    twitter_handle = UnicodeAttribute(null=True)
    github_handle = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute(hash_key=True)
    last_name = UnicodeAttribute(range_key=True)
