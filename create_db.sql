CREATE DATABASE DatabaseBD;
USE DatabaseBD;
CREATE TABLE Faixa_Etaria (
    ID_Faixa_Etaria INT AUTO_INCREMENT,
    Intervalo VARCHAR(255) NOT NULL,
    PRIMARY KEY (ID_Faixa_Etaria)
); 
CREATE TABLE CRE ( 
    ID_CRE int AUTO_INCREMENT,
    Numero_de_Matriculas int NOT NULL,
    Numero_de_Escolas int NOT NULL,
    PRIMARY KEY(ID_CRE)
); 
CREATE TABLE Bairro ( 
    ID_Bairro int AUTO_INCREMENT,
    Nome varchar(255) NOT NULL,
    ID_CRE int,
    PRIMARY KEY(ID_Bairro),
    FOREIGN KEY (ID_CRE) REFERENCES CRE(ID_CRE)
); 
CREATE TABLE Escola ( 
    ID_Bairro int,
    ID_Escola int AUTO_INCREMENT,
    Nome varchar(255) NOT NULL,
    Endereco varchar(255) NOT NULL,
    PRIMARY KEY(ID_Escola),
    FOREIGN KEY (ID_Bairro) REFERENCES Bairro(ID_Bairro)
); 
CREATE TABLE Analfabetismo (
    ID_Bairro int,
    ID_Faixa_Etaria int,
    FOREIGN KEY (ID_Bairro) REFERENCES Bairro(ID_Bairro),
    FOREIGN KEY (ID_Faixa_Etaria) REFERENCES Faixa_Etaria(ID_Faixa_Etaria)
);