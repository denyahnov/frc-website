from api import *

config = Config("client.cfg",["TBA_KEY","EVENT","TEAM"])

TBA.set_key(config.Get("TBA_KEY"))
TBA.set_event(config.Get("EVENT"))