import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import unicodedata
from mdutils.mdutils import MdUtils
import configparser

def check_if_test_exists(i,tables, workbook_name):
    df = pd.read_excel(workbook_name, tables)
    tests = []
    for col in df.columns:
        if df[col][i]=='Yes':
            tests.append(col)
    return tests
    

def find_exact_desc(final_dict,value_given):
    for key,values in final_dict.items():
        if values==value_given:
            return(values)

def find_col_desc_exact(final_dict,value_given):
    for key,values in final_dict.items():
        if key==value_given:
            return(values)

def generate_schema_file(final_dict,table_names,workbook_name,folder_name_to_append):
    sc_name = workbook_name[:-5]+'_schema.yml'
    with open(sc_name,'w') as fout:
        fout.writelines("version: 2")
        fout.writelines("\n")
        fout.writelines("\n")
        fout.writelines("models:")
        fout.writelines("\n")
        for tables in table_names:
            if tables!='Table_Descriptions':
                model_name = '   - name: '+tables
                desc_model = find_exact_desc(final_dict,tables)
                final_desc = r"     description: '{{doc("+'"'+folder_name_to_append+"__"+str(desc_model)+'"'+r")}}'"
                fout.writelines(model_name)
                fout.writelines("\n")
                fout.writelines(final_desc)
                fout.writelines("\n")
                fout.writelines("\n")
                fout.writelines('   - columns: ')
                fout.writelines("\n")
                df = pd.read_excel(workbook_name, tables)
                for i in df.index:
                    raw_col_name = df['Column_Name'][i]
                    clean_col_name = unicodedata.normalize("NFKD",raw_col_name)
                    col_name = '         - name: '+clean_col_name
                    fout.writelines(col_name)
                    fout.writelines("\n")
                    raw_desc_name = df['Column_Description'][i]
                    clean_desc_name = unicodedata.normalize("NFKD",raw_desc_name)
                    dsc_name = find_col_desc_exact(final_dict,clean_desc_name)
                    col_desc = '           description: '+r"'{{doc("+'"'+folder_name_to_append+"__"+str(dsc_name)+'"'+r")}}'"
                    fout.writelines(col_desc)
                    fout.writelines("\n")
                    tests = check_if_test_exists(i,tables,workbook_name)
                    if tests:
                        fout.writelines('           tests:')
                        fout.writelines("\n")
                        for test in tests:
                            if test=='Unique Test':
                                fout.writelines('            - unique')
                            elif test=='Nullability Test':
                                fout.writelines('            - not_null')
                            fout.writelines("\n")
                    fout.writelines("\n")
                fout.writelines("\n")


def generate_md_file(final_dict,folder_name_to_append):
    mdFile = MdUtils(file_name='columns',title='')
    end = r'{% enddocs %}'
    for keys,values in final_dict.items():
        start = r'{% docs '+folder_name_to_append+"__"+values+' %}'
        mdFile.write("\n"+start)
        mdFile.write("\n"+keys)
        mdFile.write("\n"+end+"\n")
    mdFile.create_md_file()
    with open('columns.md', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('columns.md', 'w') as fout:
        fout.writelines(data[4:])


def read_sheet_by_name(workbook_name,sheet_name):
    sheet_dict = {}
    df = pd.read_excel(workbook_name, sheet_name)
    for i in df.index:
        raw_col_name = df['Column_Name'][i]
        raw_col_desc = df['Column_Description'][i]
        col_name = unicodedata.normalize("NFKD",raw_col_name)
        col_desc = unicodedata.normalize("NFKD",raw_col_desc)
        sheet_dict[col_desc]= col_name
    return sheet_dict

def check_excel_file_format(table_names, workbook_name):
    val=0
    #Checking if Table Description Exist
    for tables in table_names:
    #Checking If Col Name and Col Description header are present
        df=pd.read_excel(workbook_name,tables)
        for col in df.columns:
            if col=='Column_Name':
                val = val+3
            elif col=='Column_Description':
                val = val+4
        if tables=='Table_Descriptions':            
            val = val+1
            a = 0
            total = 0
            for i in df.index:
                total = total+1
                if df['Column_Name'][i] in table_names:
                    a=a+1
            # print("df count ",a)
            # print("tablenames ",len(table_names))
            if a == (len(table_names)-1) and a==total:
                val = val+1
        
    check_val = len(table_names)*7+2
    if check_val==val:
        return True
    else:
        return False

def identify_duplicates_revamp(final_dict,table_names,workbook_name):
    rev_multidict = {}
    for keys, values in final_dict.items():
        rev_multidict.setdefault(values, set()).add(keys)
    print(rev_multidict)
    for keys, values in rev_multidict.items():
        if len(values)>1:
            targetkey = keys
            abc = values
            i=0
            for val in abc:
                if (i!=0):
                    temp = targetkey+"_"+str(i)
                    final_dict[val]=temp 
                i=i+1
    print(final_dict)
    return(final_dict)                           





def identify_duplicates(final_dict,table_names,workbook_name):
    rev_multidict = {}
    for keys, values in final_dict.items():
        rev_multidict.setdefault(values, set()).add(keys)
    print(rev_multidict)
    for keys, values in rev_multidict.items():
        if len(values)>1:
            targetkey = keys
            abc = values
            for val in abc:
                corres_table = ''
                for tables in table_names:
                    dff=pd.read_excel(workbook_name,tables)
                    for i in dff.index:
                        # print(dff['Column_Description'][i])
                        # print(len(dff['Column_Description'][i]))
                        if unicodedata.normalize("NFKD",dff['Column_Description'][i]) == val:
                            corres_table = tables
                            break                        
                # print("Corres_table ",corres_table)
                ddf = pd.read_excel(workbook_name,'Table_Descriptions')
                to_append = ''
                for i in ddf.index:
                    if unicodedata.normalize("NFKD",ddf['Column_Name'][i]) == corres_table:
                        to_append = "_"+unicodedata.normalize("NFKD",str(ddf['S.No'][i]))     
                # print(to_append) 
                final_name = targetkey+to_append
                # print(final_name)
                for key,values in final_dict.items():
                    if key == val:
                        # print('Key matched ',key)
                        final_dict[key]=final_name
    print(final_dict)
    return(final_dict)
                    

# config = configparser.ConfigParser()
# config.read('generator.properties')
# print(config.get('SchemaGenerator', 'model_name_to_append'))
# folder_name_to_append = config.get('SchemaGenerator','model_name_to_append')
# print(config.get('SchemaGenerator','workbook_location'))
# workbook_name = config.get('SchemaGenerator','workbook_location')
# workbook_name = 'test1.xlsx'


def create_md_schema_files(workbook_name,folder_name_to_append):
    xl = pd.ExcelFile(workbook_name)
    table_names = xl.sheet_names
    if check_excel_file_format(table_names,workbook_name):
        final_dict = {}
        finall_dict = {}
        for tables in table_names:
            final_dict.update(read_sheet_by_name(workbook_name,tables))    
        finall_dict = identify_duplicates_revamp(final_dict,table_names,workbook_name)
        print("-------------------------------------------------------------------------------------")
        print(finall_dict)
        generate_md_file(finall_dict,folder_name_to_append)
        generate_schema_file(finall_dict,table_names,workbook_name,folder_name_to_append)
    else:
        print("--------------------------Error------------------------------------------------------")
        print("Invalid File - Ensure you have entries for all the Tables in Table_Descriptions Sheet")
        print("-------------------------------------------------------------------------------------")
        print("The Sheet Name must match with the Column_Name given in the Table_Descriptions Sheet") 
        print("-------------------------------------------------------------------------------------")
        print("Each sheet must contain 'Column_Name' and 'Column_Description' Exact Replica as Headers in them")
        print("-------------------------------------------------------------------------------------")