create database a4p;
use a4p;
CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    claim_id VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    claim_type VARCHAR(50) NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
drop table claims;
show tables;
create table property_claims (policy_num varchar(20) primary key,ph_num double,staff_id varchar(20),inc_date date,inc_time time,address varchar(50),property_type varchar(20),damage_type varchar(20),country varchar(20),emg_cont double,descr varchar(100));
create table motor_claims (policy_num varchar(20) primary key,ph_num double,staff_id varchar(20),inc_date date,inc_time time,plate_no varchar(10),colour varchar(10),engine_no double , chasis_no varchar(17),km_reading double, variant_year varchar(30),address varchar(50),country varchar(20),descr varchar(100));
create table new_users(_name_ varchar(30), email varchar(30),ph_no double, country varchar(20), address varchar(50),pwd varchar(8));
desc motor_claims;