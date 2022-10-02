-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema psdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema psdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `psdb` DEFAULT CHARACTER SET utf8 ;
USE `psdb` ;

-- -----------------------------------------------------
-- Table `psdb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psdb`.`admin` (
  `username` VARCHAR(45) NOT NULL,
  `salt` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Data for table `psdb`.`admin`
-- -----------------------------------------------------
START TRANSACTION;
USE `psdb`;
INSERT INTO `psdb`.`admin` (`username`, `salt`, `password`) VALUES ('bob', 'a', 'Admin');

COMMIT;







