import urllib.request as url

def device_push(api=None,status=None):
    print("Uploading Data")
    a=url.urlopen("http://madblocks.tech/dashboard/device_push.php?device_api_key="+
                  str(api)+"&device_status="+str(status))
    print(a)
    print("Data Uploaded")
    return

def device_pull(api=None):
    print("Reading Data")
    a=url.urlopen("http://madblocks.tech/dashboard/device_pull.php?device_api_key="+str(api)).read().decode().split("<br/>")[0].split(",")[2].split(":")[1][1:]
    print("Device Status:"+str(a))
    return(a)

def upload_data_mb(api=None,sensor1=None,sensor2=None,sensor3=None,sensor4=None):
    print("Uploading Sensor Data")
    a=url.urlopen('http://madblocks.tech/dashboard/upload_data.php?channel_api_key='+str(api)+
                  '&sensor1_name='+str(sensor1)+
                  '&sensor2_name='+str(sensor2)+
                  '&sensor3_name='+str(sensor3)+
                  '&sensor4_name='+str(sensor4))
    print(a)
    print("Sensor Data Uploaded")
    return

def read_data_mb(api=None):
    print("Reading Data")
    a=url.urlopen("http://madblocks.tech/dashboard/read_data.php?channel_api_key="+str(api)).read().decode().split("<br/>")[0].split(",")
    d=[]
    for i in range(2,len(a)):
        print(a[i][1:])
        d.append(a[i].split(":")[1][1:-1])
    return(d)
