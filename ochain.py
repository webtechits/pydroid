import numpy as np
import pandas as pd
import requests
import json 
import os
from datetime import datetime
#st.write(str(row[1])+"-"+str(row[3]))      
st.title('Daily Option Chain Tracker')
Indx_Name = st.selectbox(
    "Select INDEX",
    ("NIFTY", "BANKNIFTY")
)
if Indx_Name=="NIFTY":
    folder_loc="D:/tutorial/python/niftyoidata/"
else:
    folder_loc="D:/tutorial/python/niftybankoidata/"

if st.button("Update file","upd"):
    url="https://www.nseindia.com/api/option-chain-indices?symbol="+Indx_Name
    heada={'Accept-Encoding':'gzip, deflate, br', 'Accept-Language':'en-US,en;q=0.5', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    response =  requests.get(url, headers=heada) 
    #data = json.loads(response.text)
    time=datetime.today().strftime('%H_%M')
    if Indx_Name=="NIFTY":
        with open('niftyoidata/NIFTY_OC_'+time+'.json','w') as fout:
            fout.write(response.text)
    else:
        with open('niftybankoidata/NIFTYBANK_OC_'+time+'.json','w') as fout:
            fout.write(response.text)

MTYPE = st.sidebar.selectbox(
    "Select type",
    ("PCRTRAIL", "Timewise", "Spwise","Timewn", "Active")
)

if MTYPE=="PCRTRAIL":
    expiry=st.selectbox('Select expiry',['12-May-2022', '19-May-2022','26-May-2022'])
    combdf = pd.DataFrame() 
    if st.button("Update","upd"):
        for file in os.listdir(folder_loc):
            with open(folder_loc+file,'r') as f:
                data = json.loads(f.read()) 
                index_val=int(data['records']['underlyingValue'])
                opcdata= pd.json_normalize(data, ['records','data'],errors="ignore")
                ftopcdata=opcdata[(opcdata['expiryDate'] == expiry) & (opcdata['strikePrice'] > int(round(index_val,-2)-350)) & (opcdata['strikePrice'] < int(round(index_val,-2)+350))]
                opcdatashow=ftopcdata[['strikePrice', 'CE.openInterest', 'PE.openInterest', 'CE.changeinOpenInterest', 'PE.changeinOpenInterest']].astype(int).copy()
                opcdatashow.set_axis(['SP', 'CEOI', 'PEOI', 'CCEOI', 'CPEOI'], axis=1, inplace=True)
                tempdf = pd.DataFrame(columns=['TIME', Indx_Name, 'CEOI', 'PEOI','PCR', 'CCEOI', 'CPEOI','CPCR'])
                tempdf.loc[0,:]=[data['records']['timestamp'][11:], int(data['records']['underlyingValue']), opcdatashow['CEOI'].sum(),opcdatashow['PEOI'].sum(),(opcdatashow['PEOI'].sum()/opcdatashow['CEOI'].sum()),opcdatashow['CCEOI'].sum(),opcdatashow['CPEOI'].sum(),(opcdatashow['CPEOI'].sum()/opcdatashow['CCEOI'].sum())]
                combdf=combdf.append(tempdf)   
        st.dataframe(combdf, width=900, height=600)


      


    #streamlit run opchain.py
