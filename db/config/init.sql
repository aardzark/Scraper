CREATE DATABASE book_database;
\c book_database
CREATE TABLE public.books (
    title character varying(255),
    description character varying(10000),
    upc character varying(50),
    price numeric(10,2),
    tax numeric(10,2),
    stock integer,
    number_of_reviews integer
);