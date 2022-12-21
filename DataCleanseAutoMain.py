import pandas as pd
import time
import datetime
from AbbrevAndChar import prof_char_dict, prof_abbrev_dict, sap_abbrev_dict,findItem
from Formats import format1_cleanse, format2_cleanse, format3_cleanse, format_chem, format_Fert_Micro

format1=["203_CORN", "203_SOYB", "203_CNLA","203_SUNF","203_SWTC"]
format2=["203_FLAX","203_GRSS","203_TRCL", "203_RYE", "203_OTHR", "203_PEAS", "203_ALFL", "203_COTN","203_DURM","203_NVYB", "203_SGRB", "203_GRBR","203_GRKB","203_GRPT","203_GRFS","203_GRRY","203_GROR","203_GRWT","203_GRTI","203_GRBG","203_GRCN","203_GRPU"]
format3=["203_BRLY", "203_WHET", "203_OATS", "203_SORG", "203_WHTS","203_WHTC","203_WHTW","203_WHSW","203_SGSD"]

itemID={"203":"SEED", "200":"FERT_BULK", "201":"CHEM", "202":"FERT_MICRO", "143":"FEED"}

start_time = time.time()

df_import=pd.read_excel('C:\\Users\\NParker\\Documents\\SampleFile_5.xlsx')

char_output=[]
counter=0
cleansedCounter=0
	
for index, row in df_import.iterrows():
    counter+=1
    noun = itemID[str(row["ItemIDPart1"])]
    legacy_num=row["AGRISItemID"]
	
    #checking to see if desc follows standards
    try:
        if noun=="SEED":
            if row["Name"][4] == " ":
                #If standards are followed then unique ID is made to map to SAP characteristics
                nounID=row["ItemIDPart1"]
                nounMod=row["Name"][:4]
                prodID=str(nounID)+"_"+nounMod
                
                noun,noun_Mod,sap_class=findItem(nounMod)
                
                if prodID in format1:
                    char_output_1=format1_cleanse(row, noun, noun_Mod, legacy_num, sap_class)
                    if not char_output_1[0]["Characteristic Description"].startswith("DOES"):
                        cleansedCounter+=1
                    char_output+=char_output_1
                elif prodID in format2:
                    char_output_1=format2_cleanse(row, noun, noun_Mod, legacy_num, sap_class)
                    if not char_output_1[0]["Characteristic Description"].startswith("DOES"):
                        cleansedCounter+=1
                    char_output+=char_output_1
                elif prodID in format3:
                    char_output_1=format3_cleanse(row, noun, noun_Mod, legacy_num, sap_class)
                    if not char_output_1[0]["Characteristic Description"].startswith("DOES"):
                        cleansedCounter+=1
                    char_output+=char_output_1
            else:
                char_output+= [{"Legacy Number":legacy_num, "Characteristic":row["Name"], "Characteristic Description":"DOES NOT FOLLOW FORMAT: NOUN NOT FOUND","Short Description (SAP)": "DOES NOT FOLLOW FORMAT", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
        if noun=="FERT_MICRO":
            sap_class="M_FERT_MICRO_DRY"
            if row["ProductType"]=='052':
                sap_class='M_FERT_MICRO_LIQ'
            char_output_1=format_Fert_Micro(row, legacy_num,sap_class)
            if not char_output_1[0]["Characteristic Description"].startswith("DOES"):
                cleansedCounter+=1
            char_output+=char_output_1
        if noun=="FERT_BULK":
            pass
        if noun=="CHEM":
            char_output_1=format_chem(row, legacy_num)
            if not char_output_1[0]["Characteristic Description"].startswith("DOES"):
                cleansedCounter+=1
            char_output+=char_output_1
        if noun=="FEED":
            pass
    except IndexError:
        char_output+= [{"Legacy Number":legacy_num, "Characteristic":row["Name"], "Characteristic Description":"DOES NOT FOLLOW FORMAT: INDEX ERROR","Short Description (SAP)": "DOES NOT FOLLOW FORMAT", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]
       

x = datetime.datetime.now()
dateString=str(x.year)+str(x.month)+str(x.day)+"-"+str(x.second)
updateFileName="Profisee_Desc_OutPut_"+dateString
pd.DataFrame.from_dict(char_output).to_excel(f"C:\\Users\\NParker\\Documents\\OutputFiles\\{updateFileName}.xlsx")
print("My program took", int(time.time() - start_time), "seconds to run")
print(f"Out of {counter} entries {cleansedCounter} were fully cleansed ({int(((cleansedCounter)/counter)*100)}%)")
