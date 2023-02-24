import sqlite3
from datetime import datetime

class seshata:

    journal_con = str()
    post_contents = str()
    last_post_id = int()

    def create(new_name):
        """ This function creates a new database. Usage: seshata.create(your_db_name) """
        con = sqlite3.connect(new_name + ".db")
        cur = con.cursor()
        cur.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, title, time, text)")
        cur.execute("CREATE TABLE images(id INTEGER PRIMARY KEY, name, img, post_key)")
        print("Created journal named " + new_name + ".")


    def open(name):
        """ This function opens a connection to an existing database. Call this before writing to or updating
        an existing journal. Usage: seshata.open(your_db_name) """
        con = sqlite3.connect(name + ".db")
        seshata.journal_con = (name + ".db")
        return(seshata.journal_con)

    def write():
        """ This function allows you to write a post in an in-terminal text editor, then returns the results as seshata.post_contents.
        Usage: seshata.write() """
        import os
        import subprocess
        import tempfile

        content = ''
        fdes = -1
        path = None
        fp = None
        try:
            fdes, path = tempfile.mkstemp(suffix='.txt', text=True)
            fp = os.fdopen(fdes, 'w+')
            fdes = -1
            fp.write(content)
            fp.close()
            fp = None

            editor = (os.environ.get('VISUAL') or
                      os.environ.get('EDITOR') or
                      'nano')
            subprocess.check_call([editor, path])

            fp = open(path, 'r')
            seshata.post_contents = fp.read().rstrip()
            return seshata.post_contents
        finally:
            if fp is not None:
                fp.close()
            elif fdes >= 0:
                os.close(fdes)
            if path is not None:
                try:
                    os.unlink(path)
                except OSError:
                    pass

    def post(title):
        """ This function posts the text you wrote using the write() method to the database you've connected to.
        Usage: seshata.post(your_post_title) """
        try:
            con = sqlite3.connect(seshata.journal_con)
            cursor = con.cursor()
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            sqlite_insert_post_query = """ INSERT INTO posts
                                      (title, time, text) VALUES (?, ?, ?)"""

            data_tuple = (title, dt_string, seshata.post_contents)

            cursor.execute(sqlite_insert_post_query, data_tuple)
            con.commit()
            print("Posted successfully to your database")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)


    def view_all():
        """ This function allows you to view all of the posts in the database you're connected to.
        Usage: seshata.view_all() """

        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        post_nums = []
        img_list = []
        joined = cursor.execute("SELECT name,post_key FROM images INNER JOIN posts ON images.post_key=posts.id")
        for thing in joined:
            img_list.append(thing)

        post_key = cursor.execute("SELECT * FROM posts")

        for post in post_key:
            print('Post:')
            print(post)
            print('Images:')
            for img_entry in img_list:
                if img_entry[1] == str(post[0]):
                    print(img_entry)


    def view_all_images():
        """ This function prints all of your connected database's image titles and their associated post IDs.
        Usage: seshata.view_all_images() """
        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        img_list = cursor.execute("SELECT name,post_key FROM images")
        for img in img_list:
            print(img)

    def viewID(post_id):
        """ This function prints the post text, title, and any associated images given a specific post ID.
        Usage: seshata.viewID(your_post_id) """
        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        str_ID = str(post_id)
        post_list = cursor.execute("SELECT * FROM posts WHERE id=" + str_id)
        for info in post_list:
            print(info)

    def viewTitle(post_title):
        """ This function prints all post information given a specific post title.
        Usage: seshata.viewTitle(your_post_title) """
        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        # Wrap strings in "'", otherwise SQL interprets strings as column names
        post_list = cursor.execute("SELECT * FROM posts WHERE posts.title='" + post_title + "'")
        for info in post_list:
            print(info)

    def search(search_term):
        """ This function searches the text field of your posts' content for a given search term.
        Usage: seshata.search(your_search_term) """
        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        search_results = cursor.execute("SELECT * FROM posts WHERE posts.text LIKE '%" + search_term + "%'")
        for result in search_results:
            print(result)

    def image(img_title):
        """ This function displays a specified image in your terminal. Usage: seshata.image(your_image_title) """
        import climage

        # Converts the image so it can print in the console
        output = climage.convert(img_title)

        print(output)

    def edit(title):
        import os
        import subprocess
        import tempfile

        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        post_to_edit = cursor.execute("SELECT text FROM posts WHERE posts.title='" + title + "'")
        for x in post_to_edit:
            content = (x[0])
        fdes = -1
        path = None
        fp = None
        try:
            fdes, path = tempfile.mkstemp(suffix='.txt', text=True)
            fp = os.fdopen(fdes, 'w+')
            fdes = -1
            fp.write(content)
            fp.close()
            fp = None

            editor = (os.environ.get('VISUAL') or
                      os.environ.get('EDITOR') or
                      'nano')
            subprocess.check_call([editor, path])

            fp = open(path, 'r')
            seshata.post_contents = fp.read().rstrip()
            cursor.execute('''UPDATE posts SET text = ? WHERE title = ?''', (seshata.post_contents, title))
            con.commit()
            print('Updated post!')
        finally:
            if fp is not None:
                fp.close()
            elif fdes >= 0:
                os.close(fdes)
            if path is not None:
                try:
                    os.unlink(path)
                except OSError:
                    pass

    def delete(title):
        """ This function deletes a post given its title. Usage: seshata.delete(your_post_title)"""
        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()
        cursor.execute("DELETE FROM posts WHERE title = '" + title + "'")
        print("This will permanently delete " + title + " from the database. Are you sure?")
        user_response = input("y/n ")
        if user_response == "y":
            con.commit()
            print('Post deleted.')
        else:
            print("Post not deleted.")

    def append(img_name, filename):
        """ This function inserts a new image into the Images table of the database.
        Usage: seshata.append(your_image_name, your_filename) """
        seshata.insertBLOB(img_name, filename)

    def attach(img_name, filename, post_id):
        """ This function both inserts a new image into the Images table of the database and associates it with a specific post ID.
        Usage: seshata.append(your_image_name, your_filename, your_post_id) """
        seshata.insertBLOB2(img_name, filename, post_id)


    # HELPER FUNCTIONS BELOW

    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def insertBLOB(name, photo):
        try:
            con = sqlite3.connect(seshata.journal_con)
            cursor = con.cursor()

            post_key = seshata.get_last_post_id()
            print(post_key)

            # insert query
            sqlite_insert_blob_query = """ INSERT INTO images
                                      (name, img, post_key) VALUES (?, ?, ?)"""

            # Convert to binary data to store in the database
            empPhoto = seshata.convertToBinaryData(photo)

            data_tuple = (name, empPhoto, post_key)

            cursor.execute(sqlite_insert_blob_query, data_tuple)
            con.commit()
            print("Image and file inserted successfully as a BLOB into a table")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)


    def insertBLOB2(name, photo, post_key):
        try:
            con = sqlite3.connect(seshata.journal_con)
            cursor = con.cursor()

            sqlite_insert_blob_query = """ INSERT INTO images
                                      (name, img, post_key) VALUES (?, ?, ?)"""

            # Convert to binary data to store in the database
            empPhoto = seshata.convertToBinaryData(photo)

            data_tuple = (name, empPhoto, post_key)

            cursor.execute(sqlite_insert_blob_query, data_tuple)
            con.commit()
            print("Image and file inserted successfully as a BLOB into a table")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)


    def get_last_post_id():
        con = sqlite3.connect(seshata.journal_con)
        cursor = con.cursor()

        post_key = cursor.execute("SELECT id FROM posts ORDER BY id DESC LIMIT 1")
        post_key_readable = str(post_key.fetchone())

        import re
        post_key_cleaned_list = re.findall(r"\b\d+(?:\.\d+)?\b",post_key_readable)
        post_key_cleaned = post_key_cleaned_list[0]
        return post_key_cleaned
