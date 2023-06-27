from fastapi import FastAPI, HTTPException, Query
from typing import List,Optional
from pydantic import BaseModel
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware


import sqlite3
from uuid import uuid4
import bcrypt
import os

db = 'logis.db'



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# ----------------------------------------------------------------------------
# Models
#-----------------------------------------------------------------------------

class Status(BaseModel):
    Status: str

class Image(BaseModel):
    id: str
    url: str

class Listing(BaseModel):
    id: str
    ownerId: str
    name: str
    description: str
    phone: str
    address: str
    email: str
    images: List[Image]

class Order(BaseModel):
    id: str
    listingId: str
    customerId: str
    status: str
    createdAt: str
    message: str

class Review(BaseModel):
    id: str
    listingId: str
    customerId: str
    rating: str
    message: str

class User(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    role: str
    hashedPassword: str




class UserRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    role: str

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    role: str    

class SearchResults(BaseModel):
    id: str
    owner_id: str
    name: str
    description: str
    phone: str
    address: str
    email: str


# ----------------------------------------------------------------------------
# GET /Status
#-----------------------------------------------------------------------------
@app.get("/status", response_model=Status)
async def get_api_status():
    return {"Status": "UP"}


#- ---------------------------------------------------------------------------
# GET /uuid
#-----------------------------------------------------------------------------
@app.get("/uuid", response_model=List[str])
async def get_uuid(num : int):

    uuids = []
    for i in range(num):
        uuid = uuid4()
        uuids.append(str(uuid))
        
    return uuids

# ----------------------------------------------------------------------------
# GET /search
#-----------------------------------------------------------------------------

@app.get("/search")
async def search_listings(query: str):
    # fetch all items from the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM listings_fts WHERE listings_fts MATCH ?", (query,))
    rows = cursor.fetchall()

    listings = []
    for row in rows:
        listing = SearchResults(
            id=row[0],
            owner_id=row[1],
            name=row[2],
            description=row[3],
            phone=row[4],
            address=row[5],
            email=row[6]
        )
        listings.append(listing)

    cursor.close()
    conn.close()

    return listings

# ----------------------------------------------------------------------------
# GET /listings
#-----------------------------------------------------------------------------


@app.get("/listings", response_model=List[Listing])
async def get_all_listings(owner_id: Optional[str] = Query(None)):
    
    # fetch all items from the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    listings = []

    # create a function to fetch images from the image table and add them to the listing object
    def fetch_images(listing: Listing):
        cursor.execute("SELECT * FROM images WHERE listing_id = ?", (listing.id,))
        rows = cursor.fetchall()
        if not rows:
            print("No images found")
            return
        else:
            for row in rows:
                image = Image(
                    id=row[1],
                    url=row[2]
                )
                listing.images.append(image)

    # create a function to fetch listings from the database and add them to the listings object
    def fetch_listings():
        if owner_id is None:
            cursor.execute("SELECT * FROM listings")
        else:
            cursor.execute("SELECT * FROM listings WHERE owner_id = ?", (owner_id,))
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            listing = Listing(
                id=row[0],
                ownerId=row[1],
                name=row[2],
                description=row[3],
                phone=row[4],
                address=row[5],
                email=row[6],
                images=[]
            )
            fetch_images(listing)
            listings.append(listing)

    try:
        fetch_listings()
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to fetch listings")

    cursor.close()
    conn.close()

    return listings
# ----------------------------------------------------------------------------
# GET /listings/{id}
#-----------------------------------------------------------------------------


@app.get("/listings/{id}", response_model=Listing)
async def get_listing(id: str):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # create function to fetch listing from database
    def fetch_listing():
        cursor.execute("SELECT * FROM listings WHERE id = ?", (id,))
        row = cursor.fetchone()
        listing = Listing(
            id=row[0],
            ownerId=row[1],
            name=row[2],
            description=row[3],
            phone=row[4],
            address=row[5],
            email=row[6],
            images=[]
        )
        return listing
  
    
    # create function to fetch images from image table and add them to the listing object
    def fetch_images(listing: Listing):
        cursor.execute("SELECT * FROM images WHERE listing_id = ?", (listing.id,))
        rows = cursor.fetchall()
        for row in rows:
            image = Image(
                id=row[1],
                url=row[2]
            )
            listing.images.append(image)


    # fetch the listing from the database if fails raise an exception
    try:
        listing = fetch_listing()
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to fetch listing")
    
    # fetch the images from the database if fails raise an exception
    try:
        fetch_images(listing)
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to fetch images")
    


    
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

# ----------------------------------------------------------------------------
# POST /listings
#-----------------------------------------------------------------------------
@app.post("/listings", response_model=Listing)
async def create_listing(listing: Listing):
    
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()


    # Create a function to insert a Listing item into the database
    def insert_listing(listing: Listing):
        # Convert the Listing item to a tuple of values
        values = (
            listing.id,
            listing.ownerId,
            listing.name,
            listing.description,
            listing.phone,
            listing.address,
            listing.email
        )

        # Execute an INSERT query to add the Listing item to the table
        cursor.execute("INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?, ?)", values)

      
    # create a function to insert the images in listing into the images table
    def insert_images(listing: Listing):

        # loop through the images and insert them into the database
        for image in listing.images:
            values = (
                image.id,
                listing.id,
                image.url
            )
            cursor.execute("INSERT INTO images VALUES (?, ?, ?)", values)
            



    # insert the listing into the database if fails raise an exception
    try:
        
        insert_listing(listing)
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to insert listing")
    try:
        insert_images(listing)
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to insert image")
    # Commit and close the database connection
    conn.commit()
    cursor.close()
    conn.close()
   
    return listing

# ----------------------------------------------------------------------------
# DELETE /listings/{id}
#-----------------------------------------------------------------------------
@app.delete("/listings/{id}", response_model=str)
async def delete_listing(id: str):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()


    # create function to delete listing from database
    def delete_listing():
        cursor.execute("DELETE FROM listings WHERE id = ?", (id,))
        conn.commit()
        cursor.close()

    try:
        delete_listing()
    except:

        raise HTTPException(status_code=500, detail="Failed to delete listing")
    
    return id



# ----------------------------------------------------------------------------
# GET /orders
#-----------------------------------------------------------------------------

@app.get("/orders", response_model=List[Order])
async def get_all_orders(customer_id: Optional[str] = Query(None), owner_id: Optional[str] = Query(None)):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    orders = []

    # create function to fetch orders from database and add them to the orders object
    def fetch_orders():

        if customer_id is None:
            cursor.execute("SELECT * FROM orders")
        elif customer_id is not None:
            cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
        elif owner_id is not None:
            cursor.execute("SELECT * FROM orders WHERE listing_id IN (SELECT id FROM listings WHERE owner_id = ?)", (owner_id,))    
                
        rows = cursor.fetchall()

        for row in rows:
            order = Order(
                id=row[0],
                listingId=row[1],
                customerId=row[2],
                status=row[3],
                createdAt=row[4],
                message=row[5]
            )
            print(order)
            orders.append(order)
    try:
        fetch_orders()
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to fetch orders")
    cursor.close()
    conn.close()
        
    return orders

# ----------------------------------------------------------------------------
# GET /orders/{id}
#-----------------------------------------------------------------------------

@app.get("/orders/{id}", response_model=Order)
async def get_order(id: str):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    order = None

    # create function to fetch order from database and add them to the order object
    def fetch_order():
        cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
        row = cursor.fetchone()
        order = Order(
            id=row[0],
            listingId=row[1],
            customerId=row[2],
            status=row[3],
            createdAt=row[4],
            message=row[5]
        )
        return order

    try:
        order = fetch_order()
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to fetch order")
    

    if not order:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    

    cursor.close()
    conn.close()
    
    return order

# ----------------------------------------------------------------------------
# POST /orders
# ----------------------------------------------------------------------------

@app.post("/orders", response_model=Order)
async def create_order(order: Order):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # create function to insert order into database
    def insert_order(order: Order):
        
        values = (
            order.id,
            order.listingId,
            order.customerId,
            order.status,
            order.createdAt,
            order.message
        )
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", values)
        conn.commit()
        cursor.close()
    
    try:
        insert_order(order)
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to insert order")
    
    return order    

# ----------------------------------------------------------------------------
# DELETE /orders/{id}
#-----------------------------------------------------------------------------

@app.delete("/orders/{id}", response_model=str)
async def delete_order(id: str):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()


    # create function to delete order from database
    def delete_order():
        cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
        conn.commit()
        cursor.close()

    try:
        delete_order()
    except:

        raise HTTPException(status_code=500, detail="Failed to delete order")
    
    return id

# ----------------------------------------------------------------------------
# GET /reviews
#-----------------------------------------------------------------------------

@app.get("/reviews", response_model=List[Review])
async def get_all_reviews(listing_id: Optional[str] = Query(None), customer_id: Optional[str] = Query(None), owner_id: Optional[str] = Query(None)):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    reviews = []

    def fetch_reviews():
        try:
            if listing_id is None:
                cursor.execute("SELECT * FROM reviews")
            elif listing_id is not None:
                cursor.execute("SELECT * FROM reviews WHERE listing_id = ?", (listing_id,))    

            elif customer_id is not None:
                cursor.execute("SELECT * FROM reviews WHERE customer_id = ?", (customer_id,))    
            elif owner_id is not None:
                cursor.execute("SELECT * FROM reviews WHERE listing_id IN (SELECT id FROM listings WHERE owner_id = ?)", (owner_id,))    

            # Fetch all rows returned by the query
            rows = cursor.fetchall()

            # Process the fetched rows and create Review objects
            
            for row in rows:
                review = Review(
                    id=row[0],
                    listingId=row[1],
                    customerId=row[2],
                    rating=row[3],
                    message=row[4]
                )
                reviews.append(review)

            return reviews

        except Exception as e:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=500, detail="Failed to fetch reviews")
    fetch_reviews()
    cursor.close()
    conn.close()

    return reviews

# ----------------------------------------------------------------------------
# GET /reviews/{id}
#-----------------------------------------------------------------------------

@app.get("/reviews/{id}", response_model=Review)
async def get_review(id: str):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    review = None

    def fetch_review():

        try:
            # Execute the query to fetch reviews
            cursor.execute("SELECT * FROM reviews WHERE id = ?", (id,))

            # Fetch all rows returned by the query
            row = cursor.fetchone()

            # Process the fetched rows and create Review objects
            review = Review(
                id=row[0],
                listingId=row[1],
                customerId=row[2],
                rating=row[3],
                message=row[4]
            )
            
            return review
            

        except Exception as e:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=500, detail="Failed to fetch review")

    review = fetch_review()
    cursor.close()
    conn.close()

    return review    

# ----------------------------------------------------------------------------
# POST /reviews
# ----------------------------------------------------------------------------

@app.post("/reviews", response_model=Review)
async def create_review(review: Review):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    def insert_review(review: Review):
        values = (
            review.id,
            review.listingId,
            review.customerId,
            review.rating,
            review.message
        )
        cursor.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?)", values)
        conn.commit()
        cursor.close()

    try:
        insert_review(review)
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to insert review")

    cursor.close()
    conn.close()

    return review

# ----------------------------------------------------------------------------
# DELETE /reviews/{id}
#-----------------------------------------------------------------------------

@app.delete("/reviews/{id}", response_model=str)
async def delete_review(id: str):

    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    def delete_review():
        cursor.execute("DELETE FROM reviews WHERE id = ?", (id,))
        conn.commit()
        cursor.close()

    try:
        delete_review()
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to delete review")

    return id

# ----------------------------------------------------------------------------
# GET /images
#-----------------------------------------------------------------------------


# Define the directory where your images are stored
image_directory = 'images'


@app.get("/image/{filename}")
async def get_image(filename: str):
    try:
        # Construct the filepath
        filepath = os.path.join(image_directory, filename)

        # Open the file in binary mode and read its contents
        with open(filepath, 'rb') as file:
            content = file.read()

        # Create a response with the file content and content type set to image/jpeg
        return Response(content=content, media_type='image/jpeg')

    except IOError:
        # Raise a 404 error if the file is not found
        raise HTTPException(status_code=404, detail=f"File Not Found: {filename}")


# ----------------------------------------------------------------------------
# POST /user
# ----------------------------------------------------------------------------

@app.post("/user", response_model=str)
async def create_user(user: UserRequest):
    print(user)

    # Connect to the SQLite3 database
    conn = sqlite3.connect(db)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    def insert_user(user: UserRequest):

        # hash the password
        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
        

        values = (
            uuid4().hex,
            user.firstName,
            user.lastName,
            user.email,
            user.role,
            hashed_password.decode()
        )
        
        # insert the values into users table
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", values)
        conn.commit()
        cursor.close()


        return values[0]

    try:
        id = insert_user(user)
    except:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to insert user")

   
    # return code 200 if user is created successfully
    return id




# ----------------------------------------------------------------------------
# POST /auth
# ----------------------------------------------------------------------------

@app.post("/auth", response_model=AuthResponse)
async def authenticate_user(auth_request: AuthRequest):

    # authenticate user and return AuthResponse
    def authenticate_user(auth_request: AuthRequest):

        # Connect to the SQLite3 database
        conn = sqlite3.connect(db)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # fetch user from database
        cursor.execute("SELECT * FROM users WHERE email = ?", (auth_request.email,))
        row = cursor.fetchone()
        print(row)
        # check if user exists
        if not row:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # check if password is correct
        if not bcrypt.checkpw(auth_request.password.encode(), row[5].encode()):
            cursor.close()
            conn.close()

            raise HTTPException(status_code=401, detail="Invalid credentials")

        
        # create AuthResponse
        auth_response = AuthResponse(
            id=row[0],
            firstName=row[1],
            lastName=row[2],
            email=row[3],
            role=row[4]            
        )

      
        cursor.close()
        conn.close()
        return auth_response
    
    try:
        auth_response = authenticate_user(auth_request)
    except:
        
        raise HTTPException(status_code=500, detail="Failed to authenticate user")
    
    return auth_response

