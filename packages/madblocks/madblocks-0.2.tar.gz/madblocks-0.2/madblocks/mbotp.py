import random
import time

def otp(passlen=None):
    s="0123456789"
    otp="".join(random.sample(s,passlen))
    time.sleep(1)
    return(otp)
