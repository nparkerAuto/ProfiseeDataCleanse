import os, glob
import pandas as pd
import datetime
from DataCleanseHelper import prof_char_dict, prof_abbrev_dict, sap_abbrev_dict 
from DataCleanseHelper import format1_cleanse, format2_cleanse, format3_cleanse

format1={"203_CORN":"M_SEED_CORN", "203_SOYB":"M_SEED_SOYBEANS", "203_CNLA":"M_SEED_CANOLA","203_SUNF":"M_SEED_SUNFLOWER"}
format2={"203_FLAX":"M_SEED_FLAX","203_GRSS":"M_SEED_GRASS","203_TRCL":"M_SEED_TRITICALE", "203_RYE":"M_SEED_RYE", "203_OTHR":"M_SEED_OTHER", "203_PEAS":"M_SEED_PEAS", "203_ALFL":"M_SEED_ALFALFA", "203_COTN": "M_SEED_COTTON","203_DURM":"M_SEED_DURUM","203_NVYB":"M_SEED_NAVY_BEANS", "203_SGRB":"M_SEED_SUGAR_BEETS", "203_GRBR":"M_SEED_GRASS","203_GRKB":"M_SEED_GRASS","203_GRPT":"M_SEED_GRASS","203_GRFS":"M_SEED_GRASS","203_GRRY":"M_SEED_GRASS","203_GROR":"M_SEED_GRASS","203_GRWT":"M_SEED_GRASS","203_GRTI":"M_SEED_GRASS","203_GRBG":"M_SEED_GRASS","203_GRCN":"M_SEED_GRASS"}
format3={"203_BRLY":"M_SEED_BARLEY", "203_WHET":"M_SEED_WHEAT", "203_OATS":"M_SEED_OATS", "203_SORG":"M_SEED_SORGHUM", "203_WHTS":"M_SEED_WHEAT","203_WHTC":"M_SEED_WHEAT","203_WHTW":"M_SEED_WHEAT","203_WHTW":"M_SEED_WHEAT","203_WHSW":"M_SEED_WHEAT",}
itemID={"203":"SEED"}

df_import=pd.read_excel('C:\\Users\\Nora.Parker\\Documents\\SampleFile_4.xlsx')


char_output=[]	
for index, row in df_import.iterrows():
	noun = itemID[str(row["ItemIDPart1"])]
	legacy_num=row["AGRISItemID"]
	
	#checking to see if desc follows standards
	try:
		if row["Name"][4] == " ":
			#If standards are followed then unique ID is made to map to SAP characteristics
			nounID=row["ItemIDPart1"]
			nounMod=row["Name"][:4]
			prodID=str(nounID)+"_"+nounMod
			if prodID in format1:
				char_output_1=format1_cleanse(row, noun, nounMod, legacy_num, format1[prodID])
				char_output+=char_output_1
			elif prodID in format2:
				char_output_1=format2_cleanse(row, noun, nounMod, legacy_num, format2[prodID])
				char_output+=char_output_1
			elif prodID in format3:
				char_output_1=format3_cleanse(row, noun, nounMod, legacy_num, format3[prodID])
				char_output+=char_output_1
		else:
			pass
	except IndexError:
		char_output+= [{"Legacy Number":legacy_num, "Characteristic":row["Name"], "Characteristic Description":"DOES NOT FOLLOW FORMAT: INDEX NAME","Short Description (SAP)": "DOES NOT FOLLOW FORMAT", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT"}]

x = datetime.datetime.now()
dateString=str(x.year)+str(x.month)+str(x.day)
updateFileName="Profisee_Desc_OutPut_"+dateString
pd.DataFrame.from_dict(char_output).to_csv(f"C:\\Users\\Nora.Parker\\Documents\\{updateFileName}.csv")
