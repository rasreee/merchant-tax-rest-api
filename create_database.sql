create database transactions;

create table transactions (
    id int primary key auto_increment, 
    merchant varchar(255), 
    amount decimal(10,2), 
    date datetime, 
    account_id int
);

create table accounts (
    id int primary key auto_increment, 
    name varchar(255),
    mask varchar(255)
);

insert into transactions
    (merchant, amount, date, account_id)
    values
    ('Amazon', 32.5, '2022-02-15', 1),
    ('Amazon', 51.33, '2022-02-14', 1),
    ('Geico', 300.02, '2022-02-10', 2),
    ('Amazon', 49.68, '2022-02-10', 2),
    ('Geico', 350.61, '2022-01-10', 2),
    ('Venmo', 45, '2022-01-02', 2),
    ('Venmo', 45, '2022-01-02', 3);

insert into accounts
    (name, mask)
    values
    ('Chime', '2323'),
    ('Treecard', '9922'),
    ('Chime', '2324');