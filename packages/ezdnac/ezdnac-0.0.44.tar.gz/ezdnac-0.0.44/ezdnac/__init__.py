from ezdnac.dnac import *
from ezdnac.device import *
from ezdnac.template import *
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
authToken = None
timeout = None
verifySSL = False
baseurl = '/api/v1/'
authbaseurl = '/api/system/v1/'



#####################################################
## Written by Johan Lahti, CCIE60702                #
## https://github.com/johan-lahti                   #
## shiproute.net                                    #
#####################################################