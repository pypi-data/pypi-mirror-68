import pyodbc
import json

def run_script(server, uid, pwd, connect_to_db, sql):
    return_code = 0

    # connect to datasource
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+connect_to_db+';UID='+uid+';PWD='+ pwd)
    
    # create cursor associated with connection
    cursor = conn.cursor()
    command = "EXEC master.dbo.DbExec @DbNamePattern = ?, @SQL = ?"
    try:
        cursor.execute(command, (connect_to_db, sql))
        try:
            result = cursor.fetchall()
            result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in result]
            print(json.dumps(result))
        except pyodbc.ProgrammingError:
            print("(No results)")  

        print("Command has been run successfully")        
        conn.commit()
    except ValueError:
        print("Error !!!!! %s", sys.exc_info()[0])
        return_code = -1
    finally:
        # close and delete cursor
        cursor.close()
        del cursor

        # close Connection
        conn.close()

    return return_code
    

def run_file_script(server, uid, pwd, connect_to_db, script_path):
    return_code = 0

    # connect to datasource
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+connect_to_db+';UID='+uid+';PWD='+ pwd)
    
    # create cursor associated with connection
    cursor = conn.cursor()
    command = "EXEC master.dbo.DbExec @DbNamePattern = ?, @SQL = ?"
    try:
        cursor.execute(command, (connect_to_db, script_path))
        try:
            result = cursor.fetchall()
            result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in result]
            print(json.dumps(result))
        except pyodbc.ProgrammingError:
            print("(No results)")  

        print("Command has been run successfully")
        conn.commit()
    except ValueError:
        print("Error !!!!! %s", sys.exc_info()[0])
        return_code = -1
    finally:
        # close and delete cursor
        cursor.close()
        del cursor

        # close Connection
        conn.close()

    return return_code