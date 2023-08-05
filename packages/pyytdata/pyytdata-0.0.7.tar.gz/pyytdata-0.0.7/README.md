YouTubeDataApi_Wrapper 
======================
This is an youtube api v3 wrapper which is integrated in any python app basically in web app which recommend youtube videos

A simple client for youtube data api v3 

**Prerequisites**

Get the youtube data v3 api key from https://console.developers.google.com/apis/
Set environment variable API_KEY='Your YoutubeDatav3 API key' 
and also GOOGLE_APPLICATION_CREDENTIALS='path/to/json/file' 
Reference to set GOOGLE_APPLICATION_CREDENTIALS
https://cloud.google.com/docs/authentication/getting-started  

**Installation**
	
	   pip install pyytdata 

**using**


.. code-block:: python  

   import pyytdata

   # keyword is the query you want to search from youtube data api and maxlen is no. of     video   you want.

   p=pyytdata.PyYtData(keyword,maxlen) 				    
					
   #function call for titles of video	
					
   output=p.get_titles() 

   #function to open the specific video in web browser

   output=p.open_id(item_no)  



**Contributing**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

