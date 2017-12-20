#!/usr/bin/python
 
import psycopg2
from config import config

class User:
    """User class"""
    def createNewUser(self, user_id, similar_user, similarity_score):
        '''
            Create or insert new user to the UserSimiliarity table.
        '''
        sql = """INSERT INTO USERSIMILARITY(USER_HANDLE,SIMILAR_USER, SIMILARITY_SCORE)
                 VALUES(%s,%s,%s) RETURNING USER_HANDLE;"""
        
        if(not (self.checkUserExist(user_id)== None)):
            user_handle = self.updateUser(user_id, similar_user, similarity_score);
        else:
            conn = None
            user_handle = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (user_id,similar_user, similarity_score))
                # get the generated id back
                user_handle = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        
        return user_handle

    def updateUser(self, user_id, similar_user, similarity_score):
        '''
            Update User Similarity table
        '''
        sql = """UPDATE USERSIMILARITY SET SIMILAR_USER = %s, SIMILARITY_SCORE = %s WHERE USER_HANDLE = %s;"""
        conn = None
        user_handle = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, [similar_user, similarity_score, user_id])
            # get the generated id back
            user_handle = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        
        return user_handle

    def checkUserExist(self, user_id):
        '''
            Determine if a user exists or not
        '''
        sql = """SELECT USER_HANDLE FROM USERSIMILARITY WHERE USER_HANDLE = %s;"""
        conn = None
        user_handle = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, [user_id])
            # get the generated id back
            user_handle = cur.fetchone()[0]

            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        
        return user_handle


        
    
