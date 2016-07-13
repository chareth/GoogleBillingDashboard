-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: localhost    Database: reporting
-- ------------------------------------------------------
-- Server version 5.7.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;
/*!40103 SET TIME_ZONE = '+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;
/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;

--
-- Table structure for table `Billing`
--

DROP TABLE IF EXISTS `Billing`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Billing` (
  `id`               INT(11)        NOT NULL AUTO_INCREMENT,
  `usage_date`       DATETIME       NOT NULL,
  `cost`             DOUBLE         NOT NULL,
  `project_id`       VARCHAR(16)    NOT NULL,
  `resource_type`    VARCHAR(128)   NOT NULL,
  `account_id`       VARCHAR(24)    NOT NULL,
  `usage_value`      DECIMAL(25, 4) NOT NULL,
  `measurement_unit` VARCHAR(16)    NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usage_date` (`usage_date`, `project_id`, `resource_type`)
)
  ENGINE =InnoDB
  AUTO_INCREMENT =125743
  DEFAULT CHARSET =utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Project`
--

DROP TABLE IF EXISTS `Project`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Project` (
  `id`             INT(11) NOT NULL AUTO_INCREMENT,
  `cost_center`    VARCHAR(100) DEFAULT NULL,
  `project_id`     VARCHAR(16) DEFAULT NULL,
  `project_name`   VARCHAR(100) DEFAULT NULL,
  `director`       VARCHAR(100) DEFAULT NULL,
  `director_email` VARCHAR(100) DEFAULT NULL,
  `contact_name`   VARCHAR(100) DEFAULT NULL,
  `contact_email`  VARCHAR(100) DEFAULT NULL,
  `alert_amount`   DOUBLE DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id_UNIQUE` (`project_id`),
  UNIQUE KEY `project_name_UNIQUE` (`project_name`)
)
  ENGINE =InnoDB
  AUTO_INCREMENT =983
  DEFAULT CHARSET =utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40101 SET SQL_MODE = @OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES = @OLD_SQL_NOTES */;

-- Dump completed on 2016-07-11 11:05:10
