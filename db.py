import psycopg2


class DatBase:

    def  __init__(self):
        self.connection =psycopg2.connect(
            host='127.0.0.1',
            user='postgres',
            password='132465798',
            dbname='vsp_studentassistant'
        )
        self.cursor = self.connection.cursor()


    def add_note(self,data,semester,type_note):
        with self.connection:
            self.data = data
            self.semester = semester
            self.type_note = type_note
            query = f"INSERT INTO semester_{semester}_common  (subject,first_date,name_creator,id_creator,second_date,text_note,id_photo,id_doc,type_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'{type_note}')"
            self.cursor.executemany(query,[data])
            self.connection.commit()

    def add_note_other(self,data,name_note):
        with self.connection:
            self.data = data
            self.name_note = name_note
            query = f"INSERT INTO other_notes (date_note,name_creator,id_creator,text_note,id_photo,id_doc,name_note) VALUES (%s,%s,%s,%s,%s,%s,'{name_note}')"
            self.cursor.executemany(query,[data])
            self.connection.commit()


    def check_count(self,subject,semester,type_note):
        with self.connection:
            self.semester = semester
            self.subject = subject
            query = f"SELECT * FROM semester_{semester}_common WHERE (subject = '{subject}') AND (type_note = '{type_note}') ORDER BY second_date"
            self.cursor.execute(query,subject)
            row = self.cursor.fetchall()
            return row


    def check_date(self,subject,semester,type_note):
        with self.connection:
            self.semester = semester
            self.subject = subject
            self.type_note = type_note
            query = f"SELECT second_date FROM semester_{semester}_common WHERE (subject = '{subject}') AND (type_note = '{type_note}') ORDER BY second_date"
            self.cursor.execute(query, subject)
            row = self.cursor.fetchall()
            return row


    def check_date_del_vse(self,semester,note_id):
        with self.connection:
            self.semester = semester
            self.note_id = note_id
            self.cursor.execute(f"SELECT * FROM semester_{semester}_common WHERE note_id ={note_id}")
            row = self.cursor.fetchall()
            return row
    def select_subject_date(self,subject,date_subject,type_note,semester):
        with self.connection:
            self.subject = subject
            self.date_subject = date_subject
            self.type_note =type_note
            self.semester = semester
            self.cursor.execute(f"SELECT * FROM semester_{semester}_common WHERE (subject = '{subject}') AND (second_date = '{date_subject}') AND (type_note = '{type_note}')")
            row = self.cursor.fetchall()
            return row

    def del_vse_subject(self,note_id,semester):
        with self.connection:
            self.semester = semester
            self.note_id = note_id
            self.cursor.execute(f"DELETE FROM semester_{semester}_common WHERE note_id ={note_id}")
            self.connection.commit()

    def delete_subject_date(self,subject,date_subject,type_note,semester):
        with self.connection:
            self.subject = subject
            self.date_subject = date_subject
            self.type_note =type_note
            self.semester = semester
            self.cursor.execute(f"DELETE FROM semester_{semester}_common WHERE (subject = '{subject}') AND (second_date = '{date_subject}') AND (type_note = '{type_note}')")
            self.connection.commit()

    def select_subject(self,semester):
        self.semester = semester
        with self.connection:
            self.cursor.execute(f"SELECT subject FROM semester_{semester}_subject ")
            row = self.cursor.fetchall()
            return row

    def select_name_note(self):
        with self.connection:
            self.cursor.execute(f"SELECT name_note FROM other_notes ")
            row = self.cursor.fetchall()
            return row

    def select_all_other_notes(self,name_note):
        self.name_note = name_note
        with self.connection:
            self.cursor.execute(f"SELECT * FROM other_notes WHERE name_note = '{name_note}' ")
            row = self.cursor.fetchall()
            return row



    def delete_other_note(self,name_note):
        self.name_note = name_note
        with self.connection:
            self.cursor.execute(f"DELETE FROM other_notes WHERE name_note = '{name_note}' ")
            self.connection.commit()






class Add_semester_db:

    def  __init__(self):
        self.connection =psycopg2.connect(
            host='127.0.0.1',
            user='postgres',
            password='132465798',
            dbname='vsp_studentassistant'
        )
        self.cursor = self.connection.cursor()

    def create_semester_subject(self,num_sem):
        with self.connection:
            self.num_sem = num_sem
            query = (f"CREATE TABLE semester_%s_subject (subject_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,subject varchar(100))")
            self.cursor.execute(query,[num_sem])
            self.connection.commit()

    def add_subject(self,num_sem,data):
        with self.connection:
            self.num_sem = num_sem
            self.data = data
            query = f"INSERT INTO semester_{num_sem}_subject (subject) VALUES ('{data}')"
            self.cursor.execute(query)
            self.connection.commit()


    def sem_vse(self,data):
        with self.connection:
            self.data = data
            query = f"INSERT INTO semester_vse (semester) VALUES ('{data}')"
            self.cursor.execute(query)
            self.connection.commit()


    def create_common(self,num_sem):
        with self.connection:
            self.num_sem = num_sem
            query = (f"CREATE TABLE semester_%s_common (note_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,subject character varying(75),first_date timestamp without time zone,name_creator character varying(100) ,id_creator character varying(100) ,second_date date,text_note character varying(2000),id_photo character varying ,id_doc character varying,type_note character varying)")
            self.cursor.execute(query,[num_sem])
            self.connection.commit()


    def select_last_semester(self):
        with self.connection:
            self.cursor.execute(
                f"SELECT semester FROM semester_vse ORDER BY semester DESC LIMIT 1")
            row = self.cursor.fetchall()
            return row

    def select_all_semester(self):
        with self.connection:
            self.cursor.execute(
                f"SELECT semester FROM semester_vse ORDER BY semester")
            row = self.cursor.fetchall()
            return row


    def delete_all_table(self,semester):
        with self.connection:
            self.semester = semester
            self.cursor.execute(f"DROP TABLE IF EXISTS semester_{semester}_common,semester_{semester}_subject")

    def delete_semester_from_vse(self,number_semester):
        with self.connection:

            self.number_semester = number_semester
            self.cursor.execute(f"DELETE FROM semester_vse WHERE semester = '{number_semester}'")
            self.connection.commit()

    def delete_all_subject(self,number_semester):
        with self.connection:

            self.number_semester = number_semester
            self.cursor.execute(f"DELETE FROM semester_{number_semester}_subject")
            self.connection.commit()


    def update_semester_vse(self, number_semester_old,number_semester_new):
        with self.connection:
            self.number_semester_new = number_semester_new
            self.number_semester_old = number_semester_old
            self.cursor.execute(f"UPDATE semester_vse SET semester = {number_semester_new} WHERE semester = {number_semester_old}")
            self.connection.commit()


    def update_name_table_subject(self, number_semester_old,number_semester_new):
        with self.connection:
            self.number_semester_new = number_semester_new
            self.number_semester_old = number_semester_old
            self.cursor.execute(f"ALTER TABLE semester_{number_semester_old}_subject RENAME TO semester_{number_semester_new}_subject")
            self.connection.commit()


    def update_name_table_common(self, number_semester_old,number_semester_new):
        with self.connection:
            self.number_semester_new = number_semester_new
            self.number_semester_old = number_semester_old
            self.cursor.execute(f"ALTER TABLE semester_{number_semester_old}_common RENAME TO semester_{number_semester_new}_common")
            self.connection.commit()

