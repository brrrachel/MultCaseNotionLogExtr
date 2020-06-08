CREATE DATABASE  IF NOT EXISTS `sakila` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sakila`;
-- MySQL dump 10.13  Distrib 8.0.20, for macos10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: sakila
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `address_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `street number` varchar(45) NOT NULL,
  PRIMARY KEY (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,'Marktstr.','Soltau','29614','','2008-06-20 15:41:00','3'),(2,'Hermann-Seidel-Str.','Dresden','1279','','2008-06-20 15:41:00','52'),(3,'Rathausstr.','Bickenbach','56291','','2008-06-20 15:41:00','2'),(4,'Am Schwarzenberg','Altenau','38707','','2008-06-20 15:41:00','4'),(5,'Wilhelmshavenerstr.','Nürnberg','90425','','2008-06-20 15:41:00','41'),(6,'Salzgasse','Münsingen','72525','','2008-06-20 15:41:00','12'),(7,'Bergstr.','Burgberg','87545','','2008-06-20 15:41:00','22'),(8,'Römerhügel','Soltau','29614','0165/6551241','2008-06-20 15:41:00','141'),(9,'Kevelaerer Straße','Heidekamp','23858','0150/4939179','2008-06-20 15:41:00','188'),(10,'Genholter Straße','Bickenbach','56291','0178/2365868','2008-06-20 15:41:00','83'),(11,'Markusstraße','Altenau','38707','0165/1254617','2008-06-20 15:41:00','44'),(12,'Am Bach','Soltau','29614','0173/8774761','2008-06-20 15:41:00','53'),(13,'Ludwigsteinstraße','Soltau','29614','0165/4084812','2008-06-20 15:41:00','54'),(14,'Waldescher Straße','Münsingen','72525','0175/6271904','2008-06-20 15:41:00','170'),(15,'Alter Münsterweg','Münsingen','72525','0153/3991220','2008-06-20 15:41:00','153'),(16,'Heilmannring','Münsingen','72525','0175/5672449','2008-06-20 15:41:00','68'),(17,'St.-Castor-Straße','Wolfsheim','55578','0164/2482386','2008-06-20 15:41:00','168'),(18,'Eltener Straße','Burgberg','87545','0167/1968485','2008-06-20 15:41:00','147b'),(19,'Im Rötchen','Wolfsheim','55578','0155/7870335','2008-06-20 15:41:00','45'),(20,'Nordhang','Altenau','38707','0177/8489524','2008-06-20 15:41:00','165'),(21,'Sterbecker Straße','Burgberg','87545','0179/6765347','2008-06-20 15:41:00','27'),(22,'Birkhahnweg','Bickenbach','56291','0175/4473531','2008-06-20 15:41:00','89'),(23,'Schelver Diek','Dresden','1279','0157/1293193','2008-06-20 15:41:00','29'),(24,'Unterdorfstraße','Burgberg','87545','0179/9246470','2008-06-20 15:41:00','175'),(25,'Dunkerhofstraße','Gütersloh','33330','0172/6246478','2008-06-20 15:41:00','45'),(26,'Lange Gasse','Ziegenhain','57632','0154/1835668','2008-06-20 15:41:00','185'),(27,'Bruch','Heidekamp','23858','0173/9108123','2008-06-20 15:41:00','142'),(28,'Hoverstraße','Dresden','1279','0163/5307117','2008-06-20 15:41:00','70'),(29,'Emmericher Straße','Ziegenhain','57632','0171/6405413','2008-06-20 15:41:00','62'),(30,'Junkergrund','Rodenäs','25924','0177/7129688','2008-06-20 15:41:00','177'),(31,'Am Kaisersgarten','Heidekamp','23858','0177/4266466','2008-06-20 15:41:00','43'),(32,'Wuppermannstraße','Altenau','38707','0157/8147373','2008-06-20 15:41:00','85'),(33,'Am Walde','Altenau','38707','0174/9530691','2008-06-20 15:41:00','95'),(34,'Auf dem Damm','Rodenäs','25924','0152/7392041','2008-06-20 15:41:00','118'),(35,'Im Höfchen','Wolfsheim','55578','0162/1892412','2008-06-20 15:41:00','111'),(36,'Dorfwiese','Rodenäs','25924','0163/5436120','2008-06-20 15:41:00','64'),(37,'Schlade','Hof an der Saale','95032','0154/8371110','2008-06-20 15:41:00','129'),(38,'Golostraße','Heidekamp','23858','0165/6621126','2008-06-20 15:41:00','22'),(39,'Auf der Huth','Dresden','1279','0162/5842370','2008-06-20 15:41:00','12'),(40,'Lederstraße','Soltau','29614','0153/9483564','2008-06-20 15:41:00','162'),(41,'Kufsteiner Straße','Altenau','38707','0153/8078534','2008-06-20 15:41:00','106'),(42,'Werningslebener Straße','Dresden','1279','0161/1477266','2008-06-20 15:41:00','22'),(43,'Helle Bieke','Soltau','29614','0163/8916036','2008-06-20 15:41:00','179'),(44,'Fischbacher Straße','Soltau','29614','0164/4000719','2008-06-20 15:41:00','173'),(45,'In der Bitze','Heidekamp','23858','0159/4103197','2008-06-20 15:41:00','118'),(46,'St. Sebastian','Altenau','38707','0157/2342222','2008-06-20 15:41:00','137'),(47,'Am Hochkreuz','Dresden','1279','0177/4222442','2008-06-20 15:41:00','66'),(48,'Büdinger Straße','Nürnberg','90425','0173/9403523','2008-06-20 15:41:00','150'),(49,'Mörfelder Landstraße','Dresden','1279','0176/9730078','2008-06-20 15:41:00','83'),(50,'Maria-Theresia-Straße','Dresden','1279','0150/6118651','2008-06-20 15:41:00','12'),(51,'Riedgaustraße','Wolfsheim','55578','0153/5620689','2008-06-20 15:41:00','185'),(52,'Niederndorfer Straße','Soltau','29614','0176/8241018','2008-06-20 15:41:00','194'),(53,'Am Mühlenweg','Gütersloh','33330','0157/5401840','2008-06-20 15:41:00','34'),(54,'Hangstraße','Dresden','1279','0173/2711011','2008-06-20 15:41:00','193a'),(55,'Wiesenpfad','Wolfsheim','55578','0175/8146424','2008-06-20 15:41:00','134'),(56,'Höhenstraße','Münsingen','72525','0155/7637123','2008-06-20 15:41:00','152'),(57,'Hanfackerweg','Ziegenhain','57632','0171/5021170','2008-06-20 15:41:00','102'),(58,'Anne-Frank-Straße','Soltau','29614','0151/7998726','2008-06-20 15:41:00','62'),(59,'Sterbecker Straße','Rodenäs','25924','0153/8131402','2008-06-20 15:41:00','98'),(60,'Märchenweg','Wolfsheim','55578','0158/7390738','2008-06-20 15:41:00','86'),(61,'Jan-von-Werth-Straße','Soltau','29614','0165/9756926','2008-06-20 15:41:00','93'),(62,'Nauheimer Straße','Ziegenhain','57632','0170/3645058','2008-06-20 15:41:00','82'),(63,'Bergmannstraße','Ziegenhain','57632','0169/3799397','2008-06-20 15:41:00','66'),(64,'Bennauerstraße','Soltau','29614','0156/3706383','2008-06-20 15:41:00','79'),(65,'Am Seifen','Nürnberg','90425','0175/6907889','2008-06-20 15:41:00','5'),(66,'Am Bildchen','Heidekamp','23858','0177/8774006','2008-06-20 15:41:00','156'),(67,'Eversumer Straße','Münsingen','72525','0153/8630466','2008-06-20 15:41:00','61'),(68,'Neckarstraße','Altenau','38707','0175/6361822','2008-06-20 15:41:00','155'),(69,'Blütenstraße','Heidekamp','23858','0152/6942079','2008-06-20 15:41:00','190'),(70,'Kurt-Tucholsky-Straße','Münsingen','72525','0164/5066667','2008-06-20 15:41:00','4'),(71,'Strippchens Hof','Soltau','29614','0170/8952483','2008-06-20 15:41:00','106'),(72,'Merodestraße','Altenau','38707','0169/1286156','2008-06-20 15:41:00','90'),(73,'Mörikeweg','Heidekamp','23858','0157/3648300','2008-06-20 15:41:00','36'),(74,'Kaiserallee','Rodenäs','25924','0160/1952648','2008-06-20 15:41:00','59'),(75,'Virchowstraße','Gütersloh','33330','0164/2056914','2008-06-20 15:41:00','57'),(76,'Schelmenbühl','Heidekamp','23858','0172/7015947','2008-06-20 15:41:00','80'),(77,'Wiedehagen','Heidekamp','23858','0176/7536897','2008-06-20 15:41:00','155'),(78,'Tutweg','Rodenäs','25924','0165/5125244','2008-06-20 15:41:00','76'),(79,'Bergkamp','Münsingen','72525','0152/7320231','2008-06-20 15:41:00','182'),(80,'Stahlenhauser Straße','Heidekamp','23858','0160/5945138','2008-06-20 15:41:00','47'),(81,'Kraneburgstraße','Gütersloh','33330','0170/1455237','2008-06-20 15:41:00','89'),(82,'Kahrstraße','Ziegenhain','57632','0163/5723229','2008-06-20 15:41:00','104'),(83,'Hödenbuschweg','Wolfsheim','55578','0153/7318976','2008-06-20 15:41:00','188'),(84,'Vor den Eichen','Wolfsheim','55578','0179/6661563','2008-06-20 15:41:00','165'),(85,'Afelskreuzstraße','Ziegenhain','57632','0161/8057744','2008-06-20 15:41:00','72'),(86,'Rundstraße','Burgberg','87545','0177/5538983','2008-06-20 15:41:00','68'),(87,'Josefshausstraße','Dresden','1279','0161/4903693','2008-06-20 15:41:00','144'),(88,'Am Kapellenberg','Dresden','1279','0159/9936425','2008-06-20 15:41:00','63'),(89,'Ortenaustraße','Ziegenhain','57632','0176/3077115','2008-06-20 15:41:00','191'),(90,'Marienthaler Straße','Rodenäs','25924','0178/7873808','2008-06-20 15:41:00','52'),(91,'Siegburger Straße','Heidekamp','23858','0172/5831798','2008-06-20 15:41:00','39'),(92,'Schultenstraße','Dresden','1279','0152/5418223','2008-06-20 15:41:00','81'),(93,'Lehmweg','Burgberg','87545','0162/6871693','2008-06-20 15:41:00','155'),(94,'In der Burg','Wolfsheim','55578','0152/3250351','2008-06-20 15:41:00','200'),(95,'Westfälische Straße','Altenau','38707','0173/4880095','2008-06-20 15:41:00','128'),(96,'Lippborger Straße','Hof an der Saale','95032','0150/1378542','2008-06-20 15:41:00','16'),(97,'Burgunder Straße','Rodenäs','25924','0162/7210356','2008-06-20 15:41:00','115'),(98,'Hörster','Gütersloh','33330','0157/1835809','2008-06-20 15:41:00','179'),(99,'Rohrkamp','Heidekamp','23858','0172/5893588','2008-06-20 15:41:00','171'),(100,'Ludwigsallee','Hof an der Saale','95032','0158/1282933','2008-06-20 15:41:00','175'),(101,'Platanenweg','Bickenbach','56291','0160/4413182','2008-06-20 15:41:00','138'),(102,'An den Höfen','Bickenbach','56291','0159/4361742','2008-06-20 15:41:00','7'),(103,'Agnesstraße','Rodenäs','25924','0164/2793166','2008-06-20 15:41:00','6'),(104,'Bövingen','Dresden','1279','0171/3506653','2008-06-20 15:41:00','175'),(105,'Kobergstraße','Wolfsheim','55578','0166/4282964','2008-06-20 15:41:00','11'),(106,'Ehrenstraße','Proschim','3130','0171/7489337','2008-06-20 15:41:00','108'),(107,'Am Mühlenfeld','Burgberg','87545','0178/7451958','2008-06-20 15:41:00','141');
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand` (
  `brand_id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` char(20) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand`
--

LOCK TABLES `brand` WRITE;
/*!40000 ALTER TABLE `brand` DISABLE KEYS */;
INSERT INTO `brand` VALUES (1,'rental brand','2008-06-20 15:44:00'),(2,'BOSCH','2008-06-20 15:44:00'),(3,'WAGNER','2008-06-20 15:44:00'),(4,'MSV','2008-06-20 15:44:00'),(5,'Kroll','2008-06-20 15:44:00');
/*!40000 ALTER TABLE `brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `store_id` tinyint unsigned NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `address_id` smallint unsigned NOT NULL,
  `create_date` datetime NOT NULL,
  `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`),
  KEY `idx_fk_store_id` (`store_id`),
  KEY `idx_fk_address_id` (`address_id`),
  CONSTRAINT `fk_customer_address` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_customer_store` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table storing all customers. Holds foreign keys to the address table and the store table where this customer is registered.\\n\\nBasic information about the customer like first and last name are stored in the table itself. Same for the date the record was created and when the information was last updated.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `equipment_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `release_year` year DEFAULT NULL,
  `brand_id` tinyint unsigned NOT NULL,
  `rental_rate` decimal(4,2) NOT NULL DEFAULT '4.99',
  `replacement_cost` decimal(5,2) NOT NULL DEFAULT '19.99',
  `special_features` set('Trailers','Commentaries','Deleted Scenes','Behind the Scenes') DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`equipment_id`),
  KEY `idx_fk_brand_id` (`brand_id`),
  CONSTRAINT `fk_film_language` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`brand_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'Schwing-/Deltaschleifer',NULL,2005,1,9.60,79.99,NULL,'2008-06-20 15:47:00'),(2,'Fliesenhandkreissaege eintauchbar','180mm',2006,1,29.60,119.99,NULL,'2008-06-20 15:47:00'),(3,'Säbelsäge',NULL,2009,2,11.90,89.90,NULL,'2008-06-20 15:47:00'),(4,'Bohner- & Schleifmaschine',NULL,2012,1,33.20,639.99,NULL,'2008-06-20 15:47:00'),(5,'Stemmhammer',NULL,2010,1,26.90,99.99,NULL,'2008-06-20 15:47:00'),(6,'Teppichbodenentferner',NULL,2015,1,35.60,132.90,NULL,'2008-06-20 15:47:00'),(7,'Diamantbohrmaschine',NULL,2013,1,39.90,444.99,NULL,'2008-06-20 15:47:00'),(8,'Wand- und Deckenschleifer',NULL,2014,1,42.00,79.90,NULL,'2008-06-20 15:47:00'),(9,'Rand- und Kantenschleifer',NULL,2011,1,22.00,506.00,NULL,'2008-06-20 15:47:00'),(10,'Winkelschleifer',NULL,2015,1,13.60,54.60,NULL,'2008-06-20 15:47:00'),(11,'Stichsaege',NULL,2012,2,9.60,99.99,NULL,'2008-06-20 15:47:00'),(12,'Dampf-Tapetenabloeser',NULL,2004,3,12.60,88.99,NULL,'2008-06-20 15:47:00'),(14,'Steinsäge',NULL,2013,4,13.60,759.00,NULL,'2008-06-20 15:47:00'),(16,'Kreuzlinien Laser',NULL,2011,2,14.40,138.90,NULL,'2008-06-20 15:47:00'),(17,'Tacker',NULL,2015,2,13.60,86.70,NULL,'2008-06-20 15:47:00'),(18,'Heissluft-Pistole',NULL,2013,2,5.90,69.90,NULL,'2008-06-20 15:47:00'),(19,'Platten-/Klinkerschneider\"\"',NULL,2006,4,18.40,701.00,NULL,'2008-06-20 15:47:00'),(20,'Saugheber',NULL,2009,2,7.90,69.90,NULL,'2008-06-20 15:47:00');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `inventory_id` mediumint unsigned NOT NULL AUTO_INCREMENT,
  `equipment_id` smallint unsigned NOT NULL,
  `store_id` tinyint unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`),
  KEY `idx_fk_equipment_id` (`equipment_id`),
  KEY `idx_store_id_equipment_id` (`store_id`,`equipment_id`),
  KEY `fk_inventory_store_idx` (`store_id`),
  CONSTRAINT `fk_inventory_film` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_inventory_store` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `customer_id` smallint unsigned NOT NULL,
  `staff_id` tinyint unsigned NOT NULL,
  `rental_id` int DEFAULT NULL,
  `amount` decimal(5,2) NOT NULL,
  `payment_date` datetime NOT NULL,
  `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`),
  KEY `idx_fk_staff_id` (`staff_id`),
  KEY `idx_fk_customer_id` (`customer_id`),
  KEY `fk_payment_rental_idx` (`rental_id`),
  CONSTRAINT `fk_payment_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_payment_rental` FOREIGN KEY (`rental_id`) REFERENCES `rental` (`rental_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_payment_staff` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rental`
--

DROP TABLE IF EXISTS `rental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rental` (
  `rental_id` int NOT NULL AUTO_INCREMENT,
  `rental_date` datetime NOT NULL,
  `inventory_id` mediumint unsigned NOT NULL,
  `customer_id` smallint unsigned NOT NULL,
  `return_date` datetime DEFAULT NULL,
  `staff_id` tinyint unsigned DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_date` datetime NOT NULL,
  `order_confirmed_date` datetime DEFAULT NULL,
  `order_rejected_date` datetime DEFAULT NULL,
  `return_inspected_date` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`rental_id`),
  UNIQUE KEY `idx_rental` (`rental_date`,`inventory_id`,`customer_id`),
  KEY `idx_fk_inventory_id` (`inventory_id`),
  KEY `idx_fk_customer_id` (`customer_id`),
  KEY `idx_fk_staff_id` (`staff_id`),
  CONSTRAINT `fk_rental_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_rental_inventory` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_rental_staff` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rental`
--

LOCK TABLES `rental` WRITE;
/*!40000 ALTER TABLE `rental` DISABLE KEYS */;
/*!40000 ALTER TABLE `rental` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staff_id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `address_id` smallint unsigned NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `store_id` tinyint unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`staff_id`),
  KEY `idx_fk_address_id` (`address_id`),
  KEY `fk_staff_store_idx` (`store_id`),
  CONSTRAINT `fk_staff_address` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_staff_store` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Rommy','Schoenbach',8,'rommy_schoenbach@xyz.none',1,'2008-06-20 15:59:00'),(2,'Markwart','Holder',9,'markwart.holder@spam.none',1,'2008-06-20 15:59:00'),(3,'Ben','Ney',10,'ben-ney@internet.none',3,'2008-06-20 15:59:00'),(4,'Birglinde','Laas',11,'b_laas@company.none',4,'2008-06-20 15:59:00'),(5,'Heideliese','Schomaker',12,'heideliese_schomaker@company.none',1,'2008-06-20 15:59:00'),(6,'Harri','Olsen',13,'harri-olsen@company.none',1,'2008-06-20 15:59:00'),(7,'Dorlinde','Ohl',14,'dohl@web.none',6,'2008-06-20 15:59:00'),(8,'Sieghild','Schlenker',15,'s_@mail.none',6,'2008-06-20 15:59:00'),(9,'Gerhardt','Roeseler',16,'g_roeseler@mail.none',6,'2008-06-20 15:59:00'),(10,'Simpert','Oberst',17,'simpert_oberst@web.none',3,'2008-06-20 15:59:00'),(11,'Kirsten','Detzel',18,'k-detzel@internet.none',7,'2008-06-20 15:59:00'),(12,'Raimund','Niessen',19,'raimund1948@internet.none',3,'2008-06-20 15:59:00'),(13,'Siegberta','Siemers',20,'siegberta-siemers@xyz.none',4,'2008-06-20 15:59:00'),(14,'Olf','Juengling',21,'olf_@net.none',7,'2008-06-20 15:59:00'),(15,'Sieghardt','Scherbaum',22,'sieghardt_scherbaum@private.none',3,'2008-06-20 15:59:00'),(16,'Ian','Schupp',23,'ian-@company.none',2,'2008-06-20 15:59:00'),(17,'Mark','Barrenbruegge',24,'m.@host.none',7,'2008-06-20 15:59:00'),(18,'Raimunde','Nelle',25,'raimunde.@host.none',4,'2008-06-20 15:59:00'),(19,'Hermelinde','Osterkamp',26,'hermelinde_osterkamp@net.none',3,'2008-06-20 15:59:00'),(20,'Annette','Kuhnert',27,'annette@email.none',1,'2008-06-20 15:59:00');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store` (
  `store_id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `manager_staff_id` tinyint unsigned NOT NULL,
  `address_id` smallint unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`store_id`),
  UNIQUE KEY `idx_unique_manager` (`manager_staff_id`),
  KEY `idx_fk_address_id` (`address_id`),
  CONSTRAINT `fk_store_address` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_store_staff` FOREIGN KEY (`manager_staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES (1,1,1,'2008-06-20 16:00:00'),(2,2,2,'2008-06-20 16:00:00'),(3,3,3,'2008-06-20 16:00:00'),(4,4,4,'2008-06-20 16:00:00'),(5,5,5,'2008-06-20 16:00:00'),(6,6,6,'2008-06-20 16:00:00'),(7,7,7,'2008-06-20 16:00:00');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-08 18:51:37
