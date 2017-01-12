CREATE DATABASE PCD_Database;
USE PCD_Database;

create table Candidate( 
  CID INT NOT NULL,
  YEAR INT, 
  PRIMARY KEY ( CID )
);

create table Nominee(
  NID INT NOT NULL,
  NAME VARCHAR(100) NOT NULL,
  PRIMARY KEY( NID )
);

create table Cand_Nom(
  NID INT,
  CID INT,
  FOREIGN KEY( NID ) references Nominee(NID),
  FOREIGN KEY( CID ) references Candidate(CID)
);

create table President(
  CID INT,
  DOB DATE NOT NULL,
  BIRTHPLACE VARCHAR(100),
  HOMESTATE VARCHAR(100),
  HOMECITY VARCHAR(100),
  FOREIGN KEY( CID ) references Candidate(CID)
);

create table Campaign (
  CID INT,
  EXPENSES INT,
  SLOGAN VARCHAR(100),
  FOREIGN KEY( CID ) references Candidate(CID)
);

create table Party( 
  PID INT NOT NULL,
  P_NAME VARCHAR(100),
  PRIMARY KEY( PID )
);

create table Affiliated(
  PID INT,
  CID INT,
  FOREIGN KEY( PID ) references Party(PID),
  FOREIGN KEY( CID ) references Candidate(CID)
);

create table Ballot(
  CID INT,
  POPULAR INT,
  ELECTORAL INT,
  POLLS INT,
  FOREIGN KEY( CID ) references Candidate(CID)
);
