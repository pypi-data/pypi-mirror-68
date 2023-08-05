import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

d={}

def classifyimage(api=None,url=None,targetimage=None):
    authenticator = IAMAuthenticator(api)
    visual_recognition = VisualRecognitionV3(
        version='2018-03-19',
        authenticator=authenticator
    )
    visual_recognition.set_service_url(url)
    print("Scanning...")
    try:
        with open(targetimage, 'rb') as images_file:
            classes = visual_recognition.classify(
            images_file=images_file,
            threshold='0.6',
            owners=["me"]).get_result()
        a=json.dumps(classes, indent=2)
        #print(a)
        d=json.loads(a)
        d=d['images'][0]['classifiers'][0]['classes'][0]
        class_id=d['class']
        score_id=d['score']
        print("Class Found :"+str(class_id))
        print("Score :"+str(score_id))
        b=class_id
        c=float(score_id)
        return(class_id,score_id)
    except:
        print("No Class Found")
        return("No Class",0)
