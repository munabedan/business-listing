Table of Contents

1. [API specification](#api-specification)
   1. [Status](#status)
      - [Get api status](#get-api-status)
   2. [Listings](#listings)
      - [Get all listings](#get-all-listings)
      - [Get one listing](#get-one-listing)
      - [Create a listing](#create-a-listing)
      - [Delete a listing](#delete-a-listing)
   3. [Orders](#orders)
      - [Get all orders](#get-all-orders)
      - [Get one order](#get-one-order)
      - [Create an order](#create-an-order)
      - [Delete an order](#delete-an-order)
   4. [Reviews](#reviews)
      - [Get all reviews](#get-all-reviews)
      - [Get one review](#get-one-review)
      - [Create a review](#create-a-review)
      - [Delete a review](#delete-a-review)
   5. [Users](#users)
      - [Get all users](#get-all-users)
      - [Get one user](#get-one-user)
      - [Create a user](#create-a-user)
      - [Delete a user](#delete-a-user)
   6. [Authentication](#authentication)
      - [Authenticate user](#authenticate-user)
      - [Register user](#register-user)


API specification:

# Status


## Get api status
Returns the status of the API

**Endpoint:** `/status`

**Method:** `GET`

**Request body:**
```json
{
}
```

**Response:**
```json
{
  "Status":"UP"
}
```

Any other response means it is not working properly.



# Listings

## Get all listings

**Endpoint:** `/listings`

**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
[
    {
        "id": "1",
        "ownerId": "1",
        "name": "Listing 1",
        "description": "Description 1",
        "phone": "123456789",
        "address": "Address 1",
        "email":"example@gmail.com",
        "images": [
        {
            "id": "1",
            "url": "https://example.com/image1.jpg"
        },
        {
            "id": "2",
            "url": "https://example.com/image2.jpg"
        },
        {
            "id": "3",
            "url": "https://example.com/image3.jpg"
        }

    ]

    },
    ```
]
```

## Get one listing

**Endpoint:** `/listings/{id}`
**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    "ownerId": "1",
    "name": "Listing 1",
    "description": "Description 1",
    "phone": "123456789",
    "address": "Address 1",
    "email":"",
    "images": [
        {
            "id": "1",
            "url": "https://example.com/image1.jpg"
        },
        {
            "id": "2",
            "url": "https://example.com/image2.jpg"
        },
        {
            "id": "3",
            "url": "https://example.com/image3.jpg"
        }

    ]

}
```

## Create a listing

**Endpoint:** `/listings`
**Method:** `POST`

**Request body:**
```json
{   
    "ownerId": "1",
    "name": "Listing 1",
    "description": "Description 1",
    "phone": "123456789",
    "address": "Address 1",
    "email":"",
    "images": [
        {
            "id": "1",
            "url": "https://example.com/image1.jpg"
        },
        {
            "id": "2",
            "url": "https://example.com/image2.jpg"
        },
        {
            "id": "3",
            "url": "https://example.com/image3.jpg"
        }

    ]    
}
```

**Response:**
```json
{
    "id": "1",
    
}
```

## Delete a listing

**Endpoint:** `/listings/{id}`
**Method:** `DELETE`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    
}
```



# Orders

## Get all orders

**Endpoint:** `/orders`

**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
[
    {
        "id": "1",
        "listindId": "1",
        "customerId": "1",
        "status": "pending",
        "createdAt": "2021-01-01 00:00:00",
        "message": "Message 1"    
    }
]
```

## Get one order

**Endpoint:** `/orders/{id}`
**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    "listindId": "1",
    "customerId": "1",
    "status": "pending",
    "createdAt": "2021-01-01 00:00:00",
    "message": "Message 1"    
}
```

## Create an order

**Endpoint:** `/orders`

**Method:** `POST`

**Request body:**
```json
{
    "listindId": "1",
    "customerId": "1",
    "status": "pending",
    "createdAt": "2021-01-01 00:00:00",
    "message": "Message 1"    
}
```

**Response:**
```json
{
    "id": "1",
    "listindId": "1",
    "customerId": "1",
    "status": "pending",
    "createdAt": "2021-01-01 00:00:00",
    "message": "Message 1"    
}
```

## Delete an order

**Endpoint:** `/orders/{id}`
**Method:** `DELETE`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    "listindId": "1",
    "customerId": "1",
    "status": "pending",
    "createdAt": "2021-01-01 00:00:00",
    "message": "Message 1"    
}
```



# Reviews

## Get all reviews

**Endpoint:** `/reviews`

**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
[
    {
        "id": "1",
        "listindId": "1",
        "customerId": "1",
        "rating": "5",
        "message": "Message 1"    
    }
]
```

## Get one review

**Endpoint:** `/reviews/{id}`
**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    "listindId": "1",
    "customerId": "1",
    "rating": "5",
    "message": "Message 1"    
}
```

## Create a review

**Endpoint:** `/reviews`

**Method:** `POST`

**Request body:**
```json
{
    "listindId": "1",
    "customerId": "1",
    "rating": "5",
    "message": "Message 1"    
}
```

**Response:**
```json
{
    "id": "1",
    "listindId": "1",
    "customerId": "1",
    "rating": "5",
    "message": "Message 1"    
}
```

## Delete a review

**Endpoint:** `/reviews/{id}`

**Method:** `DELETE`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    "listindId": "1",
    "customerId": "1",
    "rating": "5",
    "message": "Message 1"    
}
```

# Images

## Get an image

**Endpoint:** `/images/{id}`

**Method:** `GET`

**Request body:**
```json
{

}
```

**Response:**
```json
{
    "id": "1",
    "url": "https://example.com/image1.jpg"
}
```

# Users




## Authentication

**Endpoint:** `/auth`

**Method:** `POST`

**Request body:**
```json
{
    "email": "",
    "password": ""
}
```

**Response**
```json
{
    "token": ""
}
```

## Register user

**Endpoint:** `/users`

**Method:** `POST`

**Request body:**
```json
{
    "firstName": "",
    "lastName": "",
    "email": "",
    "password": "",
    "role": ""
}
```

**Response**
```json
{
    "id": "",
    "firstName": "",
    "lastName": "",
    "email": "",
    "role": ""
}
```





