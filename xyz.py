
import mysql.connector
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
from random import randint
from datetime import timedelta
from datetime import date
import math


nounc_string = ""



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="qtdatabase"
)


# print(mydb)
# mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM market")

# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x)
croptype=''
crop_reg_status_text="ABD"
AreaString = ""
YieldString = ""
todate = ""
fromdate = ""

def updateToDate(to_date):
   todate = to_date
   print("Todate",todate)
def updateFromDate(from_date):
   fromdate = from_date
   print("FromDate",fromdate)

def get_initial_crop_demand_data():
   mycursor = mydb.cursor()
   mycursor.execute("select CropType, Acerage from demanddata GROUP BY CropType")
   data_df = pd.DataFrame(mycursor.fetchall())
   data_df.columns = ['CropType','Acerage']   
   return data_df
def get_Current_crop_demand_data():
   mycursor = mydb.cursor()
   mycursor.execute("select CropType, Acreage from currentcropdemand GROUP BY CropType")
   data_df = pd.DataFrame(mycursor.fetchall())
   data_df.columns = ['CropType','Acerage']   
   return data_df

def get_marketNames():
   mycursor = mydb.cursor()
   mycursor.execute("select Market, CropLatitude, CropLongitude from market")
   data_df = pd.DataFrame(mycursor.fetchall())
   data_df.columns = ['Market Name','Latitude', 'Longitude']   
   return data_df

def GetRandomUNC(CropSelected):
   getUNCqry = mydb.cursor()
   FalseString = "0"   
   getUNCqry.execute("select UNC from cropdatabase1 where CropType = '"+CropSelected+"' and Status_ = '"+FalseString+"'")
   data_df = pd.DataFrame(getUNCqry.fetchall())
   data_df.columns = ['UNC']
   unclist = data_df['UNC'].tolist()
   #print(unclist)
   unc = random.choice(unclist)
   return unc

    
def GetMObileNo():    
    n = 10
    mobnum = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
    return mobnum
   
def getnearmarket(longi, lati):
    markDistqry = mydb.cursor()   
   
    market_name = []
    dist = []
    markDistqry.execute("select *from market")
    n=0
    for row in markDistqry:
      #print(row)
      market_name.append(row[0])      
      M_lati = float(row[1])
      M_longi = float(row[2])      
      d= math.sqrt(((lati-M_lati)*(lati-M_lati))+((longi-M_longi)*(longi-M_longi)))
      dist.append(d)
      n=n+1
    
    #print(market_name,dist)
    near_market = market_name[0]
    min_dist=dist[0]
    for i in range(0,n):
       if min_dist > dist[i]:
         near_market = market_name[i]
         min_dist = dist[i]
         







    #print(near_market)
    return near_market



def updateCropDemand(croptype, Acres):
    #print(croptype,Acres)
    updatedAcreagestring = ""
    qry = mydb.cursor()
    qry_update_demand= mydb.cursor()
    #QSqlQueryModel *model = new QSqlQueryModel();
    qry.execute("select Acreage from currentcropdemand where CropType = '"+croptype+"'")
    for row in qry:
      updatedAcreag = float(row[0]) - float(Acres)
      updatedAcreag = round(updatedAcreag,1)
    #print(croptype,Acres,updatedAcreagestring)
    #qry_update_demand.execute("update currentcropdemand SET Acreage = '"+str(updatedAcreag)+"' where CropType = '"+croptype+"'");
    
def on_Get_Data_pushButton_clicked():
    croparea=0.0
    yield_ = 0.0
    trueString = "1"
    CropType = croptype
    FromDate = fromdate
    toDate = todate
    
    FromDatestring = fromdate.strftime("%Y-%m-%d")
    ToDateString = toDate.strftime("%Y-%m-%d")
    #print(FromDatestring,ToDateString)
    myquery = mydb.cursor()
    r = myquery.execute("SELECT * from cropdatabase1 where YieldDate BETWEEN '"+FromDatestring+"' and '"+ToDateString+"' and Status_ = '"+trueString+"'")
    #print("R=",r)
    for row in myquery:
      #print("Between dates",row)
      croparea = croparea+float(row[5])
      yield_ = yield_+float(row[7])
          
    AreaString = str(croparea)
    YieldString = str(yield_)
    #print("AREA and Yield",AreaString,YieldString)


         #   QDate tempDate = FromDate;
         #   QSqlQuery dateqry,datecountqry;

def on_CropRegister_clicked(CropSelected):
   #print(CropSelected)
   unc = GetRandomUNC(CropSelected)
  #  uncString = str(unc)
   crop = ""
   acers = 0
   unc = 103
   mobileno = GetMObileNo()
   SownDate = datetime.date.today()
   print(unc,mobileno)
   latitude_get = random.uniform(16.0,20.0)
   if(latitude_get>19.0 and latitude_get<=20.0):
      longitude = random.uniform(78.0,80.0)
   elif(latitude_get>18.0 and latitude_get<=19.0):
      longitude = random.uniform(77.5,81.0)
   elif(latitude_get>17.0 and latitude_get<=18.0):
      longitude = random.uniform(77.4,81.5)
   elif(latitude_get>16.0 and latitude_get<=17.0):
      longitude = random.uniform(77.3,80.1)
   
   str_true = "1"
   str_false = "0"   
   getunc = mydb.cursor()     
   getunc.execute("SELECT *FROM cropdatabase1 Where UNC = '"+str(unc)+"'")
   #print("Status")
   unc_isavailable = list(getunc.fetchall())
   if not unc_isavailable:
      nounc_string = "NO Seed packet found with UNC No: "+str(unc)
      #print("nounc_string",nounc_string)
   else:
      if unc_isavailable:
         query1 = mydb.cursor()
         unc_record = query1.execute("SELECT *FROM cropdatabase1 Where UNC = '"+str(unc)+"' and Status_ = '"+str_false+"'")
         unc_record = getunc.fetchall()
         unc_record = list(unc_record)
         #print(unc_record)
         unc_record = unc_record[0]
         #print("unc_record",unc_record[1])

         yielddays = unc_record

         YieldDate = SownDate + timedelta(days=int(unc_record[8]))
         crop = unc_record[0]
         acers = unc_record[5]
         yield_ = unc_record[7]
         market_name = getnearmarket(longitude,latitude_get)

         longiString = str(round(longitude, 2))
         latiString = str(round(latitude_get, 2))
         mobileString = str(mobileno)
         yielddatestring = YieldDate.strftime("%Y-%m-%d")
         sowndateString = SownDate.strftime("%Y-%m-%d")
         #print("YieldDate",yielddays,YieldDate)
         update_values = mydb.cursor()
         #global crop_reg_status_text
         #update_values.execute("update cropdatabase1 SET MobileNo = '"+mobileString+"',Status_ = '"+str_true+"', SownDate = '"+sowndateString+"', CropLatitude ='"+latiString+"', CropLongitude = '"+longiString+"', YieldDate = '"+yielddatestring+"', Market = '"+market_name+"' where UNC = '"+str(unc)+"'")
         crop_reg_status_text = " Crop Registation is successfull.\n Seed Packet Number: "+str(unc)+".\n Mobile No : "+mobileString+".\n Crop Type:"+crop+".\n Crop Area:"+acers+" Hector.\n Crop Yield : "+yield_+".\n Expected market Arrival date: "+yielddatestring+".\n Nearest Market = "+market_name+".\n Location: "+latiString+","+longiString+"."
      else :
         crop_reg_status_text = "Already registered the crop with UNC No: "+str(unc)

   #print(crop_reg_status_text,crop,acers)
   updateCropDemand(crop,acers)
   on_Get_Data_pushButton_clicked()
   return crop_reg_status_text
      

   


InitialCropdemand_df = get_initial_crop_demand_data()
Current_crop_demand_df =  get_Current_crop_demand_data()
market_df = get_marketNames()
print("crop_reg_status_text",crop_reg_status_text)





Title_style = '<p style="font-family:sans-serif; color:Blue; font-size: 50px;">Demand Based Farming</p>'
header_style = '<p style="font-family:sans-serif; color:black; font-size: 20px;">Please enter the following data</p>'
st.markdown(Title_style, unsafe_allow_html=True)
st.markdown(header_style, unsafe_allow_html=True)


#st.title('Please enter the following data:')

fromdate, todate, initialdemand, currentdemand = st.columns([4,4,7,7], gap="small")

with fromdate:
  #  st.text('Market Arrival From Data')
   fromdate = st.date_input('Market Arrival From Data', datetime.date(2022, 7, 6), min_value=datetime.date(2020, 1,1), max_value=None, key=None, help=None, on_change=updateFromDate, args=(fromdate,), disabled=False, label_visibility="visible")
   st.text("Crop in Acres = {}".format(AreaString))
   seed_status = st.radio("Seed sown data", ('Seed sown', 'Seed unsown', 'Total seed'))
   st.button('Get Seed Data')

   st.text('Market Arrival data')
   CropSelected = st.selectbox('Crop Type',InitialCropdemand_df,on_change=on_CropRegister_clicked, args=(CropSelected,))
   croptype = CropSelected
   marketSelected = st.selectbox('Market Name',market_df)   
   st.button('Get crop location')
   
   

                                          

with todate:
   todate = st.date_input('Market Arrival To Data', datetime.date(2023, 7, 6), min_value=None, max_value=None, key=None, help=None, on_change=updateToDate, args=(todate,), disabled=False, label_visibility="visible")
   st.text("Yield in Tons = {}".format(YieldString))
   st.text('Crop demand data')
   st.button('Get initial demand   ')
   st.button('Get current demand') 
   st.markdown('##')
   Market_data = st.radio("Select Cropwise or Market wise", ('Marketwise', 'Cropwise'))
   #st.markdown('#')
   st.button('Get market arrival data')
   st.text("")
   #st.markdown('#')
   st.button('Crop registration')

#    def start_capture():
#     subprocess.run([f"{sys.executable}", "activity_check.py"])
# def run_cap():
#     st.button("Start Capturing",on_click=start_capture)
   
   
   
 
with initialdemand:
   st.text('Initial Crop Demand in Acers')
   st.dataframe(InitialCropdemand_df)
   print("{}",crop_reg_status_text)
   st.text("Crop Registration Status: {}.".format(crop_reg_status_text))
   #st.bar_chart(InitialCropdemand_df,x='0',y='1')
with currentdemand:
   st.text('Current Crop Demand in Acers')
   st.dataframe(Current_crop_demand_df)

crop_reg_status_text = on_CropRegister_clicked(CropSelected)



   

  
