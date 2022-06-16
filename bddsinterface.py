# See TODO file
# # c:\Users\15144\Desktop\PythonTutorial_Module\0000-APP_StreamLit\Bugs&Updates.txt
#change unique to pd.unique



#Change the order back to INDICATOR_ID at the beginning and label at end

#For the global / run button 
        #use a container, this container will hold the run button
        #Create the run just before running the data table 
        #When push run the data call.
        #  ==> (Actuall this might not change anything because everything else is made to run...)
            #I guess everyting should be put under that run button    
            
        # !!! Try with a TOKEN example, might need some restructuring to show structure

#Add a search option to search the indicator labels 


#Another issue is the indicators wihtout labels ==> Should probably return to a 
#format with indicator code in the select indicator

#!!! Huge data fuck up with creating a dict of label:id because some id do not have label
    #That means that only the last na label will have a indicator ID associated with it
    #The best thing is to use id:label to prevent that and go back with a scheme of searching for indicator ID and not labels
    
    
    

# import os
# os.getcwd()
# os.chdir('C:\\Users\\15144\\Desktop\\PythonTutorial_Module\\0000-APP_StreamLit\\bdds_interface_app\\')

import streamlit as st
import getuisdata as gu
# from st_aggrid import AgGrid as AgG
from io import BytesIO
import zipfile

# import pandas as pd
#import pandas_profiling

#from streamlit_pandas_profiling import st_profile_report

# import listindicconyear.py as licy

# %% CONFIG stuff
#Use wide form still mobile friendly
# st.set_page_config(page_title="UIS-UNESCO data slicer", layout="wide")
# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config

# Hide/show footer and burger widget
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#TITLE
st.markdown("# UIS-UNESCO DATASETS")
#st.markdown("## Custom Bulk Exporter")

#Adding empty container to position dataTable on top
    #This is required because the code to produce it requires input from botton that would otherwize appear
    #on top of the table

# %% CONTAINERS
#Container for indicator selector
exp_sel_indic = st.expander("Select Indicators", expanded=False)
cont_sel_indic = exp_sel_indic.container()
# with sel_indic("Select Indicator")

#Search indicator container
cont_search_indic = st.container()

#Container for data table
cont_subset = st.container()

cont_update_data = st.container()

# cont_test_stuff = st.container()

    
# %% DATA IMPORT; moved to getuisdata for code clarity
# Get archive label : name
archive_dict = gu.get_archives_list()
# st.write(archive_dict)


# SELECTOR from archive list
sel_archive = st.sidebar.selectbox('Dataset', archive_dict)
# Return label to acronym necessary for instantiation
sel_archive = archive_dict[sel_archive]    

sel_geotype = st.sidebar.radio('National or Regional data', ["Country", "Region"])

# instantiate class
my_archive = gu.inst_archive(sel_archive)
# getting data selected by user
dict_tables = gu.getData(my_archive)
# st.write(dict_tables)


# with cont_test_stuff:
#     st.write(sorted(dict_tables["COUNTRY"].COUNTRY_ID))

# %% TEST cached dataset and var creation
# df, dict_country, dict_indic, lst_count_lab, lst_indic_lab, geo, year, indic, meta = gu.varCreation(sel_geotype, my_archive, dict_tables)
df_c, dict_country_c, dict_indic_c, lst_count_lab_c, lst_indic_lab_c, geo_c, year_c, indic_c, meta_c, df_r, dict_country_r, dict_indic_r, lst_count_lab_r, lst_indic_lab_r, geo_r, year_r, indic_r, meta_r = gu.varCreation(my_archive, dict_tables)

if sel_geotype =="Country":
    df = df_c
    dict_country = dict_country_c
    dict_indic = dict_indic_c
    lst_count_lab = lst_count_lab_c
    lst_indic_lab = lst_indic_lab_c
    geo = geo_c
    year = year_c
    indic = indic_c
    meta = meta_c
    
elif sel_geotype =="Region":
    df = df_r
    dict_rountry = dict_country_r
    dict_indic = dict_indic_r
    lst_rount_lab = lst_count_lab_r
    lst_indic_lab = lst_indic_lab_r
    geo = geo_r
    year = year_r
    indic = indic_r
    meta = meta_r


    # %% SELECTION year

if df is None:
    st.markdown("### ***No regional data for the dataset selected***")
    st.sidebar.caption("No regional data for the dataset selected")
else:
    #SLICE selection
    # st.sidebar.markdown("**Slice selection**")
    
    #Year slider (returns a tuple)
    sel_year = st.sidebar.slider('Year range', min_value=int(min(year)), max_value=int(max(year)), step=1,
        value=(int(min(year)),int(max(year))
        ))
    #Update year slider tuple to represent a range from the user selection
    sel_year = list(range(sel_year[0],sel_year[1]+1))

    # %% SELECTION country

    #Adding state variable that trigger the call back fonctions for the indicator or geo multi-select
        #Call back are run before the whole app is refreshed, 
        #This means that once the app is refreshed these state are set to false so 
        #that the callback only runs when AddSearch is True, when triggered by the 
        #button "Add search list to selected items"
    if "AddSearch_indic" not in st.session_state: #first initialized
        st.session_state.AddSearch_indic = False
    st.session_state.AddSearch_indic = False

    if "AddSearch_reg" not in st.session_state: #first initialized
        st.session_state.AddSearch_reg = False
    st.session_state.AddSearch_reg = False         

    #Country/Region multi-select 
        #Country is built to use the country label, is then transformed back to iso-3 code to subset
    
    #Call back function for regional multi-select (adds search term)
    def callback_reg():
        if st.session_state.AddSearch_reg == True:
            st.session_state.Regionals = sorted(list(set(st.session_state.Regionals + search_list)))
    
    cont_geo = st.sidebar.container()                       #create container in sidebar
    exp_geo = cont_geo.expander("Select Country/Region")    #create expander in sidebar container
    
    with exp_geo:
        if sel_geotype == "Country":
            all_country = st.checkbox("Select all")         #checkbox for all country
            if all_country:
                # sel_geo = st.multiselect('National', lst_count_lab, lst_count_lab, key="Nationals")
                sel_geo = st.multiselect('Country', geo, geo, key="Nationals")
            else: 
                # sel_geo = st.multiselect('National', lst_count_lab, key="Nationals")
                sel_geo = st.multiselect('Country', geo, key="Nationals")
            # Modify sel_geo values to from label to iso-3 code, see dict_country dictionary
            # sel_geo = [dict_country[country] for country in sel_geo]
        elif sel_geotype == "Region":
            # sel_geo = st.multiselect('Region', geo, on_change = callback_reg, key="Regionals")
            all_region = st.checkbox("Select all")         #checkbox for all country
            if all_region:
                # sel_geo = st.multiselect('National', lst_count_lab, lst_count_lab, key="Nationals")
                sel_geo = st.multiselect('Region', geo,geo, key="Regionals")
            else: 
                # sel_geo = st.multiselect('National', lst_count_lab, key="Nationals")
                sel_geo = st.multiselect('Region', geo, key="Regionals")
            # Modify sel_geo values to from label to iso-3 code, see dict_country dictionary
            # sel_geo = [dict_country[country] for country in sel_geo]


    # %% SELECTION indicator
    # with cont_select_indic:
    #     st.write("test this shit")
        
    #Call back function for indicator multi-select (adds search terms)
    def callback_indic():
        if st.session_state.AddSearch_indic == True:
            st.session_state.Indicators = sorted(list(set(st.session_state.Indicators + search_list)))
    
    # cont_indic = st.sidebar.container()                     #Create containder in sidebar
    # exp_indic = cont_indic.expander("Select Indicator")     #create expander in sidebar container
    
    #Insert indic selector in container declared at the beginning of code
    with cont_sel_indic:
    # with exp_indic:
        sel_all_indic = st.checkbox("Select all indicators") #Check box for selecting all indics
        if sel_all_indic:
            # sel_indic = st.multiselect('Indicator', indic, indic, key="Indicators")
            sel_indic = st.multiselect('Indicator', indic, indic, on_change = callback_indic, key = "Indicators")
            # sel_indic = st.multiselect('Indicator', lst_indic_lab, lst_indic_lab, on_change = callback_indic, key = "Indicators")
            # sel_indic = [dict_indic[i] for i in sel_indic]  #Return indic_id necessary to call datasubset function
        else:
            # sel_indic = st.multiselect('Indicator', indic, key="Indicators")
            sel_indic = st.multiselect('Indicator', indic, on_change = callback_indic, key = "Indicators")
            # sel_indic = st.multiselect('Indicator', lst_indic_lab, on_change = callback_indic, key = "Indicators")
            # sel_indic = [dict_indic[i] for i in sel_indic]  #Return indic_id necessary to call datasubset function

# %% SELECT metadata
    # #METADATA selection 
    # st.sidebar.markdown("**Optional selection**")
    
    # #Add country labels checkbox
    # if sel_geotype == "Country":     #Only show button for country data
    #     sel_c_label = st.sidebar.checkbox('Add Country Label')
    # #Add indicator labels checkbox
    # sel_i_label = st.sidebar.checkbox('Add Indicator Label')
    
    #Data-point metadata multi-select
    #check if there is metadata, if so, show the metadata selection
    if meta is None:
        st.sidebar.caption("No datapoint metadata for the selected dataset or at regional level")
        #radio button for meta 
    else:
        sel_meta = st.sidebar.radio("Add Metadata",
              ('None', 'Multiple Columns', 'Single column as a dictionary'))
    
    # %% SUBSET data
    
    # with cont_update_data:
    #     update_data = st.button("Update data")
    #     if update_data:
    #     # Creating subset (no label, no meta)
    a_subset = my_archive.subsetData(df, sel_year, sel_geo, sel_indic, geoType=sel_geotype)

    # #Adding country/indic labels to subset
    # if sel_geotype == "Country":    #If Country radio button selected 
    #     if sel_c_label:             #If Country label selected
    #             a_subset = my_archive.addLabel(a_subset, label_country, labelType = "Country")
        
    # if sel_i_label:     #If Indic label selected
    #     a_subset = my_archive.addLabel(a_subset, label_indic, labelType = "Indic")

    #Adding metadata to subset    
    if meta is not None:    #if meta df is not empty
        # Adding metadata according to user selection
        if sel_meta == "None": 
            # "None selected"
            pass
        elif sel_meta =="Multiple Columns":
            # "Multiple selected"
            a_subset = my_archive.allMetaMerge(dict_tables, a_subset, 
                        metaForm="Col")
        else:
            a_subset = my_archive.allMetaMerge(dict_tables, a_subset,
                        metaForm="Dict")
    
    #Table rendering
    with cont_subset:
        #Render table    
        st.dataframe(a_subset)
        # AgG(a_subset)
        
        #Write number of rows
        st.write(f'Observations in selection: {a_subset.shape[0]}')
    
    #since a_subset is under a button I need to initilize a session state 
    #to keep it in memory and pass it to the download function
    # if "a_subset" not in st.session_state: #first initialized
    #     st.session_state.a_subset = a_subset
    # st.session_state.a_subset = a_subset

# %% DOWNLOAD button
# Download button for downloading the dataset
    # !!!Change download name of file to dynamic(specificToDataset + date/min/sec)
        #The download button could be disabled until all parameters of subset are filled 
    st.download_button(
          label="Download data as CSV",
          data=gu.df_to_csv(a_subset),
          file_name=sel_archive+"_"+gu.fileDate()+".csv",
          mime='text/csv',
          #disabled = True
      )

# %% DOWNLOAD metadata (See dfzip module) ==> could be put in the getuisdata module... 
#Create an indicator codebood and add the option to download the labels + readme
    # # #checkbox to download metadata
    # st.sidebar.markdown("**Download metadata files**")
    
    # meta_file_lst = ['Country labels', 'Indicator labels', 'Readme']
    # sel_meta_file = st.sidebar.multiselect(
    #     'Select files',
    #       meta_file_lst)

# %% SEARCH indicators / regions

    with cont_search_indic:
        
        with st.expander("Search and add list of indicators/regions to your selection", expanded=False):
            if "radio_geo" not in st.session_state:
                st.session_state.radio_geo = None
                
            # st.sidebar.radio('Country or Region data', [
            if sel_geotype == "Country":
                st.session_state.radio_geo = "Indicator"
                sel_search_var = "INDICATOR_ID"
                # st.session_state.radio_geo
            elif sel_geotype == "Region":
                sel_search_var = st.radio('Pick search variable', ["INDICATOR_ID", "REGION_ID"], key="radio_geo")
                if sel_search_var == "Indicator":
                    sel_search_var = "INDICATOR_ID"
                else:
                    sel_search_var = "REGION_ID"
                    
        
            # st.write("Enter your search term separated by a comma")
            if sel_geotype == "Country":
                st.caption("Search INDICATOR_ID")
            searchTermList = st.text_input("Enter your search terms separated by a comma")
            searchTermList = searchTermList.replace(" ", "").split(",")
            #Should remove any trailing comma to ensure we don't pass an empty string as searche which returns 
            search_list = my_archive.searchList_II(searchTermList, df, sel_search_var)
        
        
            #Add search list call back function    
            def callback_search():
                st.session_state.radio_geo
                if st.session_state.radio_geo == "Indicator":
                    st.session_state.AddSearch_indic = True     #session state for triggering callback function
                    callback_indic()
                elif st.session_state.radio_geo == "Region":
                    st.session_state.AddSearch_reg = True       #session state for triggering callback function
                    callback_reg()
            
            st.button('Add search results to the selected items', on_click=callback_search, key="b_add_search_list")
            # st.session_state.AddSearch
            
            #st.write("Number of item matched: ", len(search_list))
            # st.write("Expand the pannel below to see your search results ")
            #check_search_results = st.checkbox("See search results")
            check_search_results = st.checkbox(f"See your {len(search_list)} search results")

            if check_search_results:
                st.write(search_list)
            
            
# %% Dataset profile (could be the reason why max memory is exceeded)
# # Build config file to change the max mem
# # https://docs.streamlit.io/library/advanced-features/configuration#set-configuration-options
# #REMOVE FOR NOW
# #pandas profile ; summary stats
# with st.expander("Summary statistics"):
#     pr = a_subset.profile_report(minimal=True)
#     st_profile_report(pr)


# %% REFERENCES
# !!! Put all in a container?
# Source
st.markdown("###### Data source: [***UNESCO-UIS Bulk Data Download (BDDS)***](https://apiportal.uis.unesco.org/bdds)")

# Other references
st.markdown("###### Back-end library (Python): [***uisdata.bdds***](https://test.pypi.org/project/uisdata/)")
st.markdown("###### Use-case using the back-end library (DataLore): [***uisdata.bdds SDG use-case***](https://datalore.jetbrains.com/notebook/FaD1hIZ0s0XKrlZcWTMYVW/UrrXOcYJWCstRNMNPvzzPF/)")


# %% Download labels as ZIP file
# !!! note issue producing the readMe because of the data call setup
#  
cont_label_files = st.sidebar.container()                           #create container in sidebar
exp_label_files = cont_label_files.expander("Download label files")    #create expander in sidebar container

with exp_label_files:
    if "REGION" in dict_tables:
        lab_country = dict_tables["COUNTRY"].to_csv().encode('utf-8')
        lab_indic = dict_tables["LABEL"].to_csv().encode('utf-8')
        lab_region = dict_tables["REGION"].to_csv().encode('utf-8')
        files_available = ['Country', 'Indicator', 'Region']
    else:
        lab_country = dict_tables["COUNTRY"].to_csv().encode('utf-8')
        lab_indic = dict_tables["LABEL"].to_csv().encode('utf-8')
        files_available = ['Country', 'Indicator']
    
    all_labels = st.checkbox(label='Select all label files', value=True)
    if all_labels:
        sel_meta_file = st.multiselect('Select label files',files_available, files_available)
    else:
        sel_meta_file = st.multiselect('Select label files',files_available)
    
    #List of files to download
    list_files = {}
    
    # if 'ReadMe' in sel_meta_file:
    #     list_files["ReadMe"]=readMe
    if 'Country' in sel_meta_file:
        list_files["Country"]=lab_country
    if 'Indicator' in sel_meta_file:
        list_files["Indicator"]=lab_indic
    if 'Region' in sel_meta_file:
        list_files["Region"]=lab_region
    
    # Create zip file
    in_memory=BytesIO()
    with zipfile.ZipFile(in_memory, 'w') as zipF:
        for fileName, file in dict.items(list_files):
            if isinstance(file, str):
                zipF.writestr(fileName+".md", file)
            else:
                # pass
                print(type(file))
                zipF.writestr(fileName+".csv", file)
    #            
    in_memory.seek(0)
    zipData = in_memory.read()
    
    #Name of file should include the date to make it unique
    st.download_button(
         label="Download label files as ZIP",
         data=zipData,
         file_name=f'zipData_{gu.fileDate()}.zip',
         mime='application/zip',
         #disabled = True
     )




