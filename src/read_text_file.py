import psycopg2

def text_file_to_list(file_path_name: str)->list:
    with open(file_path_name, 'r') as f:
        x = f.read().splitlines()

    items = [word.strip() for word in x]

    return items

def insert_1_dim_list(conn:psycopg2.connect, ls:list, col_name:str)-> None:
    cur = conn.cursor()

    for elem in values:
        cur.execute(
        '''INSERT INTO orientations (orientation) 
        VALUES (%(orientation)s);''',
        {'orientation': elem}
        
        )
        conn.commit()

if __name__ == '__main__':
    file_path_name = '../data/issues_list.txt'
    values = text_file_to_list(file_path_name)
    #col_name = 'issues'

    conn = psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')
    
    #insert_1_dim_list(conn, values, col_name)

    cur = conn.cursor()

    for elem in values:
        cur.execute(
        '''INSERT INTO issues (issue) 
        VALUES (%(issue)s);''',
        {'issue': elem}
        
        )
        conn.commit()
        
    conn.close()