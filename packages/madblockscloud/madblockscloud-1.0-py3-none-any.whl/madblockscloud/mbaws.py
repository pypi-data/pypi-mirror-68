import boto3
def sendsms(access_id=None,secret_access_key=None,ph_no=None,message=None):
    print("Sending SMS to "+str(ph_no))
    client = boto3.client(
        "sns",
        aws_access_key_id=access_id,
        aws_secret_access_key=secret_access_key,
        region_name="us-east-1"
    )
    client.publish(
        PhoneNumber=ph_no,
        Message=message
    )
    print("message sent")


def face_reg(region=None,access_id=None,secret_access_key=None,sourceimage=None,targetimage=None):
    # Replace sourceFile and targetFile with the image files you want to compare.
    print("Finding Face match..")
    sourceFile=sourceimage
    targetFile=targetimage
    client=boto3.client('rekognition',region_name=region,aws_access_key_id=access_id,
         aws_secret_access_key= secret_access_key)
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')
    try:
     response=client.compare_faces(SimilarityThreshold=70,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    except:
     print("Face not detected, Invalid Image")
     return(0)
    faceMatchFlag=0
    for faceMatch in response['FaceMatches']:
        faceMatchFlag=1
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print('Face Matched with '+str(confidence)+"%")
        return(1)
    if faceMatchFlag==0:
        print ('Not Matched')
        return(0)
    imageSource.close()
    imageTarget.close()
    
def object_detect(region=None,access_id=None,secret_access_key=None,targetimage=None):
    print("Finding Objects from image")
    sourceFile=targetimage
    client = boto3.client('rekognition',region_name=region,aws_access_key_id=access_id,
         aws_secret_access_key= secret_access_key)
    imageSource=open(sourceFile,'rb')
    response = client.detect_labels(
        Image={'Bytes': imageSource.read()})
    d={}
    l=[]
    for faceDetail in response['Labels']:
       print(faceDetail['Name'],faceDetail['Confidence'])
       d[faceDetail['Name']]=faceDetail['Confidence']
       l.append(str(faceDetail['Name']))
    if(len(l)>0):
        #print(d)
        k=max(d.values())
        for i in l:
            if d[i]==k:
                return(l,i)
