# Seshata
A simple, streamlined, console-based journal/database program written in Python. Allows for the storage of images as well as text in the SQL database (and can print stored images in the console).

<p align="center">
<img src="https://raw.githubusercontent.com/ian-nai/seshata/main/seshata.jpg" height="350" width="220">
</p>

## Usage

### Requirements
climage==0.1.3
```
pip install climage
```

###To write your first post:

```
import seshata

seshata.create('my_journal')

seshata.write() # An editor will open and allow you to type your post text.

seshata.post('my first post')

```

### To edit a post in an existing journal:

```
seshata.open('my_journal') 

seshata.edit('my first post')

```
### To append an image to a post and then view it in the console:

```
seshata.open('my_journal') 

seshata.attach('my image', 'img_1.jpeg', 1)

seshata.image('my image')

```
### Full list of callable functions:

#### create(new_name)
This function creates a new database. Usage: seshata.create(your_db_name)

#### open(name)
This function opens a connection to an existing database. Call this before writing to or updating
an existing journal. Usage: seshata.open(your_db_name)
       
#### write():
This function allows you to write a post in an in-terminal text editor, then returns the results as seshata.post_contents.
Usage: seshata.write()
        
#### post(title)
This function posts the text you wrote using the write() method to the database you've connected to.
Usage: seshata.post(your_post_title) 

#### append(img_name, filename)
This function inserts a new image into the Images table of the database.
Usage: seshata.append(your_image_name, your_filename)

#### attach(img_name, filename, post_id)
This function both inserts a new image into the Images table of the database and associates it with a specific post ID.
Usage: seshata.append(your_image_name, your_filename, your_post_id)

#### create(new_name)
This function creates a new database. Usage: seshata.create(your_db_name)

#### delete(title)
This function deletes a post given its title. Usage: seshata.delete(your_post_title)

#### edit(title)
This function allows you to edit an existing post given its title. Usage: seshata.edit(your_post_title)

#### search(search_term):
This function searches the text field of your posts' content for a given search term.
Usage: seshata.search(your_search_term)

#### image(img_title)
This function displays a specified image in your terminal. Usage: seshata.image(your_image_title)

#### open(name)
This function opens a connection to an existing database. Call this before writing/updating a post or appending/attaching an image.

#### view_all()
This function allows you to view all of the posts in the database you're connected to. 
Usage: seshata.view_all() 

#### view_all_images()
This function prints all of your connected database's image titles and their associated post IDs.
Usage: seshata.view_all_images()

#### viewID(post_id)
This function prints the post text, title, and any associated images given a specific post ID.
Usage: seshata.viewID(your_post_id)

#### viewTitle(post_title)
This function prints all post information given a specific post title.
Usage: seshata.viewTitle(your_post_title)



