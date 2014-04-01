CREATE TABLE House
(
House_Id int NOT NULL AUTO_INCREMENT,
Address varchar(255),
Address_1 varchar(255),
Address_2 varchar(255),
Address_3 varchar(255),
Address_4 varchar(255),
County varchar(255),
Beds int,
Baths int,
Price int,
CONSTRAINT House_Id PRIMARY KEY (House_Id)
);


CREATE TABLE Flat
(
Flat_Id int NOT NULL AUTO_INCREMENT,
Address varchar(255),
Address_1 varchar(255),
Address_2 varchar(255),
Address_3 varchar(255),
Address_4 varchar(255),
County varchar(255),
Beds int,
Baths int,
Price int,
CONSTRAINT Flat_Id PRIMARY KEY (Flat_Id)
);

CREATE TABLE Apartment
(
Apartment_Id int NOT NULL AUTO_INCREMENT,
Address varchar(255),
Address_1 varchar(255),
Address_2 varchar(255),
Address_3 varchar(255),
Address_4 varchar(255),
County varchar(255),
Beds int,
Baths int,
Price int,
CONSTRAINT Apartment_Id PRIMARY KEY (Apartment_Id)
);

CREATE TABLE Studio
(
Studio_Id int NOT NULL AUTO_INCREMENT,
Address varchar(255),
Address_1 varchar(255),
Address_2 varchar(255),
Address_3 varchar(255),
Address_4 varchar(255),
County varchar(255),
Beds int,
Baths int,
Price int,
CONSTRAINT Studio_Id PRIMARY KEY (Studio_Id)
);


CREATE TABLE Rentals
(
Rental_Id int NOT NULL AUTO_INCREMENT,
Name varchar(255),
Area varchar(255),
Collection varchar(255),
County varchar(255),
Listing_id int,
Lat long,
Longitude long,
Link varchar(255),
Photo_url varchar(255),
Street varchar(255),
Rent int,
Summary varchar(255),

CONSTRAINT Rental_Id PRIMARY KEY (Rental_Id), UNIQUE (Listing_id )
);