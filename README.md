# **REST API for book exchange platform**

You can use Insomnia JSON file from root folder to have query examples.

### **Books**

##### GET

/books - returns all the book records that DB has.

/books/<book_id> - returns particular book record from DB.

##### POST

/books - add new book with information from JSON body. Available fields: name (mandatory),
author (mandatory), translator, genre, year, publisher, isbn.

##### PATCH

/books/<book_id> - update existing book record with information from JSON body. Available 
fields: name, author, translator, genre, year, publisher, isbn.

##### DELETE

/books/<book_id> - delete existing book record from DB. Also deletes all the
library and wishlist records that contain this book.

### **User**

##### GET

/users - returns all the user records that DB has.

/users/<user_id> - returns particular user record from DB.

##### POST

/users - add new user with information from JSON body. Available fields: username (mandatory),
group (mandatory). Alongside with user record new library record is created 
for this user. 

##### PATCH

/users/<user_id> - update existing user record with information from JSON body. 
Available fields: username, group, address_id (must be in DB already).

##### DELETE

/users/<user_id> - delete existing user record from DB. Also deletes user's library and 
wishlist records.

### **Address**

##### GET

/addr - returns all the address records that DB has.

/addr/<addr_id> - returns particular address record from DB.

##### POST

/addr - add new address with information from JSON body. Available fields: street_addr,
city, region, zip, country. All the fields are mandatory.

##### PATCH

/addr/<addr_id> - update existing address record with information from JSON body. Available fields: 
street_addr, city, region, zip, country.


##### DELETE

/addr/<addr_id> - delete existing address record from DB.

### **Library**

Libraries are created alongside with user and already have id and user_id.

##### GET

/users/<user_id>/library - returns particular user's library.

##### POST

/users/<user_id>/library - add new book to library. Only book_id field available.

##### PATCH

/users/<user_id>/library - you can hide or reveal user's library using this URL. Only 
hidden_lib field available.

/users/<user_id>/library/<book_id> - you can update particular book's status or hide/reveal
it in library. Available fields: status and hidden.

##### DELETE

/users/<user_id>/library/<book_id> - delete book from library.

### **Wishlist**

##### GET

/users/<user_id>/wishlist - returns particular user's wishlist.

##### POST

/users/<user_id>/wishlist - add new book to wishlist. Only book_id field available.

##### DELETE

/users/<user_id>/wishlist/<book_id> - delete book from wishlist.
