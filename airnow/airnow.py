import requests

def AirNow():
    #read zip code
    with open("ZipCodes.txt", "r") as f:
        zipCodes = f.read().split("\n")

    # Setup param
    params = {'API_KEY': '####',
                    'zipCode': 'zipcode',
                    'date': '2017-10-19',
                    'distance': '25',
                    'format': 'application/json'}

    URL = "http://www.airnowapi.org/aq/forecast/zipCode/"

    results = []

    for zipCode in zipCodes:
        params['zipCode'] = zipCode
        json_response = requests.get(URL, params).json()

        output = (str(zipCode)+","+
                  str(json_response[0]['StateCode'])+","+
                  str(json_response[0]['ReportingArea']) + "," +
                  str(json_response[0]['Latitude']) + "," +
                  str(json_response[0]['Longitude']) + "," +
                  str(json_response[0]['AQI']))
        print(output)
        results.append(output)

    #Write result
    with open("OUTPUT_AQI.txt", "w") as f1:
        for result in results:
            f1.write(result+'\n')

AirNow()