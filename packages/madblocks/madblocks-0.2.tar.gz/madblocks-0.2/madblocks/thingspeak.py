import urllib.request as url
import json
def upload_data_ts(api=None,field1=None,field2=None,field3=None,field4=None,field5=None,field6=None,field7=None,field8=None):
    print("Uploading Data")
    a=url.urlopen("https://api.thingspeak.com/update?api_key="+str(api)+"&field1="+str(field1)+
                "&field2="+str(field2)+
                "&field3="+str(field3)+
                "&field4="+str(field4)+
                "&field5="+str(field5)+
                "&field6="+str(field6)+
                "&field7="+str(field7)+
                "&field8="+str(field8))
    print(a)
    print("Data Uploaded")
    return

def read_data_ts(ch_no=None,field_no=1):
    print("Reading Data") 
    a=url.urlopen("https://api.thingspeak.com/channels/"+str(ch_no)+"/fields/"+str(field_no)+".json?results=1").read().decode()
    a=json.loads(a)
    c=a['feeds'][0]["field"+str(field_no)]
    print("Field "+str(field_no)+" value:"+str(c))    
    return(c)

