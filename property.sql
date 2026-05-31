DROP DATABASE IF EXISTS property_sales;
CREATE DATABASE IF NOT EXISTS property_sales;
USE property_sales;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- PROPERTIES TABLE
CREATE TABLE IF NOT EXISTS properties (
    id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    suburb VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    original_price FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    car_spaces INT NOT NULL,
    size_sqft INT NOT NULL,
    seller_id VARCHAR(10) NOT NULL,
    image TEXT NOT NULL,
    features TEXT,
    created_at DATETIME,

    FOREIGN KEY (seller_id)
        REFERENCES users(id)
);

-- BOOKMARKS TABLE
CREATE TABLE IF NOT EXISTS bookmarks (
    id VARCHAR(10) PRIMARY KEY,
    user_id VARCHAR(10) NOT NULL,
    property_id VARCHAR(10) NOT NULL,
    notes TEXT,
    created_at DATETIME,

    FOREIGN KEY (user_id)
        REFERENCES users(id),

    FOREIGN KEY (property_id)
        REFERENCES properties(id)
);

-- ENQUIRIES TABLE
CREATE TABLE IF NOT EXISTS enquiries (
    id VARCHAR(10) PRIMARY KEY,
    property_id VARCHAR(10) NOT NULL,
    buyer_id VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at DATETIME,

    FOREIGN KEY (property_id)
        REFERENCES properties(id),

    FOREIGN KEY (buyer_id)
        REFERENCES users(id)
);

-- OFFERS TABLE
CREATE TABLE IF NOT EXISTS offers (
    id VARCHAR(10) PRIMARY KEY,
    property_id VARCHAR(10) NOT NULL,
    buyer_id VARCHAR(10) NOT NULL,
    amount FLOAT NOT NULL,
    message TEXT,
    status VARCHAR(50) NOT NULL,
    created_at DATETIME,

    FOREIGN KEY (property_id)
        REFERENCES properties(id),

    FOREIGN KEY (buyer_id)
        REFERENCES users(id)
);

-- DOCUMENTS TABLE
CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id VARCHAR(10) NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size VARCHAR(50),
    file_type VARCHAR(50) DEFAULT 'PDF',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (property_id)
        REFERENCES properties(id)
        ON DELETE CASCADE
);



-- USERS

INSERT INTO users
(id, username, password_hash, email, firstname, surname, phone, role)
VALUES
('U001', 'admin1', 'scrypt:32768:8:1$eXZW3Ul8bh4nRqzd$abcc42450facc8f379bc1664ec9a175031b2abd6e16fcc7d5fca182322b45ecb37e86961e6e58f8218712a1f15b1eac5aab9131ad345f69d88093d609c89bcc6', 'admin1@gmail.com', 'John', 'Smith', '0400000001', 'admin'),
('U002', 'seller1', 'scrypt:32768:8:1$QQfsgQDzeurgAN8T$c318ff15d8cef27c5f6026376b59646470550c5d8404d141e23f62fe408d6d3e69bca8dd7829ae2c2c7603c3d292e165a58f3ef251bbf646f3705fd310f00337', 'seller1@gmail.com', 'Michael', 'Brown', '0400000002', 'seller'),
('U003', 'seller2', 'scrypt:32768:8:1$m7oYYmTxdxCqabpU$69d743c335b7d7219f0f6fe3badf27e05e8cd067b78bfc6f3954304d3584ff0d15a40a332fdf0f11afcd3d2172ce5e015de6ad28d9290d9839e1d5423dfb8af0', 'seller2@gmail.com', 'David', 'Wilson', '0400000003', 'seller'),
('U004', 'buyer1', 'scrypt:32768:8:1$zbjl6UGAiAB9U5AG$1d6de0eb3c42e83f34e9c59f315dd773b9b4831f00e7797d2b73acbfc4c6805d544d625b79b89a719dc1880457c515e7eba010fe14e30c31dce7e9616618716e', 'buyer1@gmail.com', 'Emma', 'Taylor', '0400000004', 'buyer'),
('U005', 'buyer2', 'scrypt:32768:8:1$27vGoJTVSgpct6RJ$47fa3883e4c68a3498d9ba0d489ad1282fba8bee0c91b98b02ac6d2d4e546028092a0b57e5c1823f31eb52ca2185e2bd50d1ffb3fe0ad81f00c0143a29c9acbf', 'buyer2@gmail.com', 'Olivia', 'Johnson', '0400000005', 'buyer'),
('U006', 'buyer3', 'scrypt:32768:8:1$zbjl6UGAiAB9U5AG$1d6de0eb3c42e83f34e9c59f315dd773b9b4831f00e7797d2b73acbfc4c6805d544d625b79b89a719dc1880457c515e7eba010fe14e30c31dce7e9616618716e', 'buyer3@gmail.com', 'Sophia', 'White', '0400000006', 'buyer'),
('U007', 'seller3', 'scrypt:32768:8:1$QQfsgQDzeurgAN8T$c318ff15d8cef27c5f6026376b59646470550c5d8404d141e23f62fe408d6d3e69bca8dd7829ae2c2c7603c3d292e165a58f3ef251bbf646f3705fd310f00337', 'seller3@gmail.com', 'Daniel', 'Martin', '0400000007', 'seller'),
('U008', 'buyer4', 'scrypt:32768:8:1$27vGoJTVSgpct6RJ$47fa3883e4c68a3498d9ba0d489ad1282fba8bee0c91b98b02ac6d2d4e546028092a0b57e5c1823f31eb52ca2185e2bd50d1ffb3fe0ad81f00c0143a29c9acbf', 'buyer4@gmail.com', 'James', 'Clark', '0400000008', 'buyer'),
('U009', 'buyer5', 'scrypt:32768:8:1$zbjl6UGAiAB9U5AG$1d6de0eb3c42e83f34e9c59f315dd773b9b4831f00e7797d2b73acbfc4c6805d544d625b79b89a719dc1880457c515e7eba010fe14e30c31dce7e9616618716e', 'buyer5@gmail.com', 'Lucas', 'Walker', '0400000009', 'buyer'),
('U010', 'seller4', 'scrypt:32768:8:1$m7oYYmTxdxCqabpU$69d743c335b7d7219f0f6fe3badf27e05e8cd067b78bfc6f3954304d3584ff0d15a40a332fdf0f11afcd3d2172ce5e015de6ad28d9290d9839e1d5423dfb8af0', 'seller4@gmail.com', 'Henry', 'Hall', '0400000010', 'seller'),
('U011', 'buyer6', 'scrypt:32768:8:1$27vGoJTVSgpct6RJ$47fa3883e4c68a3498d9ba0d489ad1282fba8bee0c91b98b02ac6d2d4e546028092a0b57e5c1823f31eb52ca2185e2bd50d1ffb3fe0ad81f00c0143a29c9acbf', 'buyer6@gmail.com', 'Mia', 'Allen', '0400000011', 'buyer'),
('U012', 'buyer7', 'scrypt:32768:8:1$zbjl6UGAiAB9U5AG$1d6de0eb3c42e83f34e9c59f315dd773b9b4831f00e7797d2b73acbfc4c6805d544d625b79b89a719dc1880457c515e7eba010fe14e30c31dce7e9616618716e', 'buyer7@gmail.com', 'Charlotte', 'Young', '0400000012', 'buyer'),
('U013', 'seller5', 'scrypt:32768:8:1$QQfsgQDzeurgAN8T$c318ff15d8cef27c5f6026376b59646470550c5d8404d141e23f62fe408d6d3e69bca8dd7829ae2c2c7603c3d292e165a58f3ef251bbf646f3705fd310f00337', 'seller5@gmail.com', 'Benjamin', 'King', '0400000013', 'seller'),
('U014', 'buyer8', 'scrypt:32768:8:1$27vGoJTVSgpct6RJ$47fa3883e4c68a3498d9ba0d489ad1282fba8bee0c91b98b02ac6d2d4e546028092a0b57e5c1823f31eb52ca2185e2bd50d1ffb3fe0ad81f00c0143a29c9acbf', 'buyer8@gmail.com', 'Ethan', 'Scott', '0400000014', 'buyer'),
('U015', 'admin2', 'scrypt:32768:8:1$ExHHWMXCtyPMAhYY$c228e01658c7f7fc25a39796dc0cb69c82132bb98c5836281d6fe9ed1accf1e857fac9104789dfb91f47f1ec483419c8f26c424be61dc924e6304425e88e8d6d', 'admin2@gmail.com', 'John', 'Cena', '0400000015', 'admin');


-- PROPERTIES

INSERT INTO properties
(id, title, address, suburb, description, price, original_price,
category, status, bedrooms, bathrooms, car_spaces,
size_sqft, seller_id, image, features, created_at)
VALUES
('P001','Luxury Family House','12 Queen St','Brisbane','Modern luxury house',1200000,1300000,'House','Active',4,3,2,3200,'U002','house1.jpg','Pool,Garden,Garage',NOW()),
('P002','City Apartment','45 King St','Sydney','Apartment in city center',850000,900000,'Apartment','Active',2,2,1,1400,'U003','apt1.jpg','Balcony,Gym',NOW()),
('P003','Beachside Villa','9 Ocean Ave','Gold Coast','Beachfront villa',2200000,2400000,'House','Under Offer',5,4,3,4500,'U007','villa1.jpg','Pool,Ocean View',NOW()),
('P004','Modern Apartment','100 Main Rd','Melbourne','Luxury apartment',780000,820000,'Apartment','Sold',2,1,1,1200,'U010','apt2.jpg','Gym,Parking',NOW()),
('P005','Family Home','18 Lake Rd','Perth','Spacious family home',950000,1000000,'House','Active',3,2,2,2600,'U013','house2.jpg','Garden,Garage',NOW()),
('P006','Penthouse Suite','88 Sky Tower','Brisbane','Premium penthouse',3100000,3200000,'Apartment','Active',4,3,2,3800,'U002','penthouse.jpg','Pool,Gym,Spa',NOW()),
('P007','Suburban House','22 Green Ave','Adelaide','Affordable suburban home',620000,650000,'House','Withdrawn',3,2,2,2100,'U003','house3.jpg','Garage,Garden',NOW()),
('P008','Studio Apartment','77 River St','Canberra','Compact studio apartment',450000,500000,'Apartment','Active',1,1,1,800,'U007','studio.jpg','Gym',NOW()),
('P009','Luxury Mansion','5 Hilltop Dr','Brisbane','Massive luxury mansion',5500000,5700000,'House','Active',7,6,4,8500,'U010','mansion.jpg','Pool,Cinema,Gym',NOW()),
('P010','Town Apartment','66 George St','Sydney','Modern apartment',990000,1100000,'Apartment','Under Offer',3,2,1,1600,'U013','apt3.jpg','Balcony,Gym',NOW()),
('P011','Countryside House','3 Farm Rd','Toowoomba','Quiet countryside home',730000,760000,'House','Active',4,2,2,3000,'U002','house4.jpg','Garden,Fireplace',NOW()),
('P012','Waterfront Apartment','90 Bay St','Gold Coast','Apartment with water views',1250000,1300000,'Apartment','Sold',3,2,2,1900,'U003','apt4.jpg','Pool,Balcony',NOW()),
('P013','Eco Friendly Home','12 Solar Way','Brisbane','Eco smart house',1350000,1400000,'House','Active',4,3,2,3400,'U007','eco.jpg','Solar,Garage',NOW()),
('P014','Downtown Apartment','11 Central Ave','Melbourne','Luxury downtown apartment',870000,920000,'Apartment','Active',2,2,1,1300,'U010','apt5.jpg','Gym,Parking',NOW());


-- BOOKMARKS

INSERT INTO bookmarks
(id, user_id, property_id, notes, created_at)
VALUES
('BM001','U004','P001','Dream home',NOW()),
('BM002','U005','P002','Nice location',NOW()),
('BM003','U006','P003','Beach house',NOW()),
('BM004','U008','P004','Affordable',NOW()),
('BM005','U009','P005','Family property',NOW()),
('BM006','U011','P006','Luxury penthouse',NOW()),
('BM007','U012','P007','Good investment',NOW()),
('BM008','U014','P008','Small apartment',NOW()),
('BM009','U004','P009','Huge mansion',NOW()),
('BM010','U005','P010','Modern style',NOW()),
('BM011','U006','P011','Quiet area',NOW()),
('BM012','U008','P012','Waterfront',NOW()),
('BM013','U009','P013','Eco home',NOW()),
('BM014','U011','P014','Central location',NOW());


-- ENQUIRIES

INSERT INTO enquiries
(id, property_id, buyer_id, message, status, created_at)
VALUES
('E001','P001','U004','Is this property still available?','New',NOW()),
('E002','P002','U005','Can I schedule inspection?','Responded',NOW()),
('E003','P003','U006','Any negotiation possible?','Closed',NOW()),
('E004','P004','U008','Interested in apartment','New',NOW()),
('E005','P005','U009','Need more photos','Responded',NOW()),
('E006','P006','U011','Can I inspect this weekend?','Closed',NOW()),
('E007','P007','U012','What is final price?','New',NOW()),
('E008','P008','U014','Any parking included?','Responded',NOW()),
('E009','P009','U004','Luxury mansion enquiry','Closed',NOW()),
('E010','P010','U005','Can I make offer?','New',NOW()),
('E011','P011','U006','Interested buyer','Responded',NOW()),
('E012','P012','U008','Inspection request','Closed',NOW()),
('E013','P013','U009','Need more details','New',NOW()),
('E014','P014','U011','When was property built?','Responded',NOW());


-- OFFERS

INSERT INTO offers
(id, property_id, buyer_id, amount, message, status, created_at)
VALUES
('O001','P001','U004',1180000,'My first offer','Pending',NOW()),
('O002','P002','U005',830000,'Interested buyer','Accepted',NOW()),
('O003','P003','U006',2100000,'Cash buyer','Rejected',NOW()),
('O004','P004','U008',760000,'Quick settlement','Pending',NOW()),
('O005','P005','U009',930000,'Final offer','Accepted',NOW()),
('O006','P006','U011',3000000,'Luxury penthouse offer','Rejected',NOW()),
('O007','P007','U012',600000,'Good condition','Pending',NOW()),
('O008','P008','U014',430000,'Studio offer','Accepted',NOW()),
('O009','P009','U004',5400000,'Mansion offer','Rejected',NOW()),
('O010','P010','U005',960000,'Apartment bid','Pending',NOW()),
('O011','P011','U006',710000,'Countryside house offer','Accepted',NOW()),
('O012','P012','U008',1200000,'Waterfront apartment offer','Rejected',NOW()),
('O013','P013','U009',1300000,'Eco home offer','Pending',NOW()),
('O014','P014','U011',850000,'Downtown apartment offer','Accepted',NOW());


-- DOCUMENTS

INSERT INTO documents
(property_id, document_name, file_name, file_size, file_type)
VALUES
('P001','Floor Plan','floorplan1.pdf','450 KB','PDF'),
('P002','Contract','contract2.pdf','380 KB','PDF'),
('P003','Inspection Report','report3.pdf','500 KB','PDF'),
('P004','Title Deed','title4.pdf','290 KB','PDF'),
('P005','Property Brochure','brochure5.pdf','410 KB','PDF'),
('P006','Legal Document','legal6.pdf','620 KB','PDF'),
('P007','Inspection Checklist','check7.pdf','300 KB','PDF'),
('P008','Property Map','map8.pdf','270 KB','PDF'),
('P009','Ownership Papers','ownership9.pdf','540 KB','PDF'),
('P010','Finance Details','finance10.pdf','360 KB','PDF'),
('P011','Floor Layout','layout11.pdf','400 KB','PDF'),
('P012','Property Guide','guide12.pdf','350 KB','PDF'),
('P013','Building Report','building13.pdf','490 KB','PDF'),
('P014','Contract Agreement','contract14.pdf','450 KB','PDF');