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
  `id` VARCHAR(45) NOT NULL,
  `username` VARCHAR(250) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `verificatie` VARCHAR(45) NOT NULL,
  `salt` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`, `username`, `email`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Data for table `psdb`.`admin`
-- -----------------------------------------------------
START TRANSACTION;
USE `psdb`;
INSERT INTO `psdb`.`admin` (`id`, `username`, `email`, `verificatie`, `salt`, `password`) VALUES ('1', 'bob','enero.mangal@gmail.com', '12345', 'a', 'Admin');

COMMIT;

