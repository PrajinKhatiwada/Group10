from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum


class UserRole(Enum):
    ADMIN  = 'admin'
    SELLER = 'seller'
    BUYER  = 'buyer'


class PropertyStatus(Enum):
    ACTIVE      = 'Active'
    UNDER_OFFER = 'Under Offer'
    SOLD        = 'Sold'
    WITHDRAWN   = 'Withdrawn'


class PropertyCategory(Enum):
    HOUSE     = 'House'
    APARTMENT = 'Apartment'


class EnquiryStatus(Enum):
    NEW       = 'New'
    RESPONDED = 'Responded'
    CLOSED    = 'Closed'


class OfferStatus(Enum):
    PENDING  = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'


@dataclass
class User:
    id: str
    username: str
    password_hash: str
    email: str
    firstname: str
    surname: str
    phone: str
    role: UserRole = UserRole.BUYER

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_seller(self):
        return self.role == UserRole.SELLER

    def is_buyer(self):
        return self.role == UserRole.BUYER

    def full_name(self):
        return f"{self.firstname} {self.surname}"


@dataclass
class Property:
    id: str
    title: str
    address: str
    suburb: str
    description: str
    price: float
    original_price: float
    category: PropertyCategory
    status: PropertyStatus
    bedrooms: int
    bathrooms: int
    car_spaces: int
    size_sqft: int
    seller_id: str
    image: str
    features: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def is_active(self):
        return self.status == PropertyStatus.ACTIVE


@dataclass
class Bookmark:
    id: str
    user_id: str
    property_id: str
    notes: str = ''
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Enquiry:
    id: str
    property_id: str
    buyer_id: str
    message: str
    status: EnquiryStatus = EnquiryStatus.NEW
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Offer:
    id: str
    property_id: str
    buyer_id: str
    amount: float
    message: str = ''
    status: OfferStatus = OfferStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
