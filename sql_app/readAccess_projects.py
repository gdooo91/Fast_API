import pandas
import pypyodbc #pyodbc 
import sqlite3

def fix_project_datatype(df):
    df['projectid'] = df['projectid'].astype(int)
    df['companyid'] = df['companyid'].astype(int)
    df['contactid'] = df['contactid'].astype(float)
    df['shiptoenduser'] = df['shiptoenduser'].astype(bool)
    df['enduser'] = df['enduser'].astype(int)
    df['endusecontactid'] = df['endusecontactid'].astype(float)
    df['employeeid'] = df['employeeid'].astype(int)
    df['purchaseordernumber'] = df['purchaseordernumber'].astype(str)
    df['saleid'] = df['saleid'].astype(float) ## (int)
    df['projecttotalbillingestimate'] = df['projecttotalbillingestimate'].astype(float)
    df['projectname'] = df['projectname'].astype(str)
    df['projecttypeid'] = df['projecttypeid'].astype(int)
    df['projectmodel'] = df['projectmodel'].astype(str)
    df['projectdescription'] = df['projectdescription'].astype(str)
    df['numberofaxis'] = df['numberofaxis'].astype(float) #(int)
    df['projectscanning'] = df['projectscanning'].astype(bool)
    df['projectscanwidth'] = df['projectscanwidth'].astype(str)
    df['projectserialnumber'] = df['projectserialnumber'].astype(str)
    df['projectbegindate'] = df['projectbegindate'].astype(str)
    df['projectenddate'] = df['projectenddate'].astype(str)
    df['projectduedate'] = df['projectduedate'].astype(str)
    df['probeorderdate'] = df['probeorderdate'].astype(str)
    df['partsorderdate'] = df['partsorderdate'].astype(str)
    df['projectshipdate'] = df['projectshipdate'].astype(str)
    df['projectinstalldate'] = df['projectinstalldate'].astype(str)
    df['projectclosed'] = df['projectclosed'].astype(bool)
    df['projectstatus'] = df['projectstatus'].astype(str)
    df['hand'] = df['hand'].astype(str)
    df['valvemodel'] = df['valvemodel'].astype(str)
    df['touchscreen'] = df['touchscreen'].astype(str)
    df['numberofprobes'] = df['numberofprobes'].astype(float) ##(int)
    df['projectreference'] = df['projectreference'].astype(str)
    return(df)

## before updating cursor.
def get_dt_col_names(df, cursor):
    ### Find the Columns Names in 'table_name' Table
    columns_names = [column[0] for column in cursor.description]
    
    ## Set Column Names to Data Frame Table
    if len(columns_names) == len(df.columns):   
        df.columns = columns_names
    return df

def Select_All(cursor, table_name):
    if cursor == None or cursor == "":
        return(-1)
    
    if table_name == None or table_name == "":
        return(-1)
    

    ## Save the contant of the table to a data frame
    cursor.execute('select * from ' + table_name)
    select_All = pandas.DataFrame((tuple(t) for t in cursor.fetchall()))

    return(get_dt_col_names(select_All, cursor))

def get_open_Projects (cursor):
    sqlCMD = 'select * from Project WHERE projectclosed = False'
    # print(sqlCMD)
    cursor.execute(sqlCMD)
    open_projects = pandas.DataFrame((tuple(t) for t in cursor.fetchall()))
    return(get_dt_col_names(open_projects, cursor))

## TODO: remove duplicates and retrun
def remove_duplicates(df1, df2, column_name):
    new_df = df2.copy(deep=True)
    id_to_remove = set(df1[column_name])  ## make a set of the POs ID

    for po in id_to_remove:
        index_list = new_df.query(str(column_name)+" == " + str(po)).index.tolist()
        new_df = new_df.drop(index=index_list)
        ### .drop(index=index_list, axis = 1, inplace = True)
    
    return new_df


# def main():
conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\othman\Documents\Database\NewOps_AUG_17_2021.accde;')
conn = pypyodbc.connect(conn_str, readonly=True)
cursor = conn.cursor()

project_df = get_open_Projects(cursor) # Select_All (cursor, "Project")
cursor.close()
project_df = fix_project_datatype(project_df)

conn = sqlite3.connect('db\Projects.db')
c = conn.cursor()
sqlite_Projects = Select_All(c, "projects")

if len(sqlite_Projects) == 0:
    project_df.to_sql('projects',conn, if_exists = 'append', index=False)
else :
    new_project_df = remove_duplicates(sqlite_Projects, project_df, 'projectid')

