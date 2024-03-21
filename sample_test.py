import requests
f = open('test.log', 'w+')
def saveResult(name, url, result):
    f.write('Test name:' + str(name) + '\n')
    f.write('Test URL:' + str(url) + '\n')
    f.write('Test result:' + str(result) + '\n')
    f.write('---------------------------------------------\n ')
    
    
def checkServiceForWord(url, keyword):
    result = False
    try:
        x = requests.get(url)
        print(x.text)
        if keyword in x.text:
            print("found keyword")
            result=True
    except:
        print("error")
        result= False
    return result


# Test 1
name = 'Test 1'
url = 'http://localhost:5000/’'
result = checkServiceForWord(url, 'hello')
saveResult(name, url, result)
# finish up
f.close()