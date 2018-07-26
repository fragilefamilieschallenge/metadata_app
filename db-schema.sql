-- MySQL dump 10.14  Distrib 5.5.56-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: FFMeta
-- ------------------------------------------------------
-- Server version	5.5.56-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data_type`
--

DROP TABLE IF EXISTS `data_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_type` (
  `id` char(30) NOT NULL,
  `name` char(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` text,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8669 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `measure`
--

DROP TABLE IF EXISTS `measure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measure` (
  `id` tinyint(1) NOT NULL,
  `name` char(100) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `raw`
--

DROP TABLE IF EXISTS `raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw` (
  `new_name` char(30) NOT NULL,
  `old_name` char(30) DEFAULT NULL,
  `varlab` text,
  `type` char(10) NOT NULL,
  `group` char(30) DEFAULT NULL,
  `q_group_N` int(11) DEFAULT NULL,
  `topic1` char(50) DEFAULT NULL,
  `umbrella1` char(50) DEFAULT NULL,
  `topic2` char(50) DEFAULT NULL,
  `umbrella2` char(50) DEFAULT NULL,
  `scope` char(10) DEFAULT NULL,
  `warning` int(11) DEFAULT NULL,
  `source` char(30) DEFAULT NULL,
  `respondent` char(30) DEFAULT NULL,
  `wave` tinyint(1) DEFAULT NULL,
  `section` char(1) DEFAULT NULL,
  `leaf` char(30) DEFAULT NULL,
  `q_group_list` text,
  `value1` varchar(20) DEFAULT NULL,
  `label1` varchar(200) DEFAULT NULL,
  `value2` varchar(20) DEFAULT NULL,
  `label2` varchar(200) DEFAULT NULL,
  `value3` varchar(20) DEFAULT NULL,
  `label3` varchar(200) DEFAULT NULL,
  `value4` varchar(20) DEFAULT NULL,
  `label4` varchar(200) DEFAULT NULL,
  `value5` varchar(20) DEFAULT NULL,
  `label5` varchar(200) DEFAULT NULL,
  `value6` varchar(20) DEFAULT NULL,
  `label6` varchar(200) DEFAULT NULL,
  `value7` varchar(20) DEFAULT NULL,
  `label7` varchar(200) DEFAULT NULL,
  `value8` varchar(20) DEFAULT NULL,
  `label8` varchar(200) DEFAULT NULL,
  `value9` varchar(20) DEFAULT NULL,
  `label9` varchar(200) DEFAULT NULL,
  `value10` varchar(20) DEFAULT NULL,
  `label10` varchar(200) DEFAULT NULL,
  `value11` varchar(20) DEFAULT NULL,
  `label11` varchar(200) DEFAULT NULL,
  `value12` varchar(20) DEFAULT NULL,
  `label12` varchar(200) DEFAULT NULL,
  `value13` varchar(20) DEFAULT NULL,
  `label13` varchar(200) DEFAULT NULL,
  `value14` varchar(20) DEFAULT NULL,
  `label14` varchar(200) DEFAULT NULL,
  `value15` varchar(20) DEFAULT NULL,
  `label15` varchar(200) DEFAULT NULL,
  `value16` varchar(20) DEFAULT NULL,
  `label16` varchar(200) DEFAULT NULL,
  `value17` varchar(20) DEFAULT NULL,
  `label17` varchar(200) DEFAULT NULL,
  `value18` varchar(20) DEFAULT NULL,
  `label18` varchar(200) DEFAULT NULL,
  `value19` varchar(20) DEFAULT NULL,
  `label19` varchar(200) DEFAULT NULL,
  `value20` varchar(20) DEFAULT NULL,
  `label20` varchar(200) DEFAULT NULL,
  `value21` varchar(20) DEFAULT NULL,
  `label21` varchar(200) DEFAULT NULL,
  `value22` varchar(20) DEFAULT NULL,
  `label22` varchar(200) DEFAULT NULL,
  `value23` varchar(20) DEFAULT NULL,
  `label23` varchar(200) DEFAULT NULL,
  `value24` varchar(20) DEFAULT NULL,
  `label24` varchar(200) DEFAULT NULL,
  `value25` varchar(20) DEFAULT NULL,
  `label25` varchar(200) DEFAULT NULL,
  `value26` varchar(20) DEFAULT NULL,
  `label26` varchar(200) DEFAULT NULL,
  `value27` varchar(20) DEFAULT NULL,
  `label27` varchar(200) DEFAULT NULL,
  `value28` varchar(20) DEFAULT NULL,
  `label28` varchar(200) DEFAULT NULL,
  `value29` varchar(20) DEFAULT NULL,
  `label29` varchar(200) DEFAULT NULL,
  `value30` varchar(20) DEFAULT NULL,
  `label30` varchar(200) DEFAULT NULL,
  `value31` varchar(20) DEFAULT NULL,
  `label31` varchar(200) DEFAULT NULL,
  `value32` varchar(20) DEFAULT NULL,
  `label32` varchar(200) DEFAULT NULL,
  `value33` varchar(20) DEFAULT NULL,
  `label33` varchar(200) DEFAULT NULL,
  `value34` varchar(20) DEFAULT NULL,
  `label34` varchar(200) DEFAULT NULL,
  `value35` varchar(20) DEFAULT NULL,
  `label35` varchar(200) DEFAULT NULL,
  `value36` varchar(20) DEFAULT NULL,
  `label36` varchar(200) DEFAULT NULL,
  `value37` varchar(20) DEFAULT NULL,
  `label37` varchar(200) DEFAULT NULL,
  `value38` varchar(20) DEFAULT NULL,
  `label38` varchar(200) DEFAULT NULL,
  `value39` varchar(20) DEFAULT NULL,
  `label39` varchar(200) DEFAULT NULL,
  `value40` varchar(20) DEFAULT NULL,
  `label40` varchar(200) DEFAULT NULL,
  `value41` varchar(20) DEFAULT NULL,
  `label41` varchar(200) DEFAULT NULL,
  `value42` varchar(20) DEFAULT NULL,
  `label42` varchar(200) DEFAULT NULL,
  `value43` varchar(20) DEFAULT NULL,
  `label43` varchar(200) DEFAULT NULL,
  `value44` varchar(20) DEFAULT NULL,
  `label44` varchar(200) DEFAULT NULL,
  `value45` varchar(20) DEFAULT NULL,
  `label45` varchar(200) DEFAULT NULL,
  `value46` varchar(20) DEFAULT NULL,
  `label46` varchar(200) DEFAULT NULL,
  `value47` varchar(20) DEFAULT NULL,
  `label47` varchar(200) DEFAULT NULL,
  `value48` varchar(20) DEFAULT NULL,
  `label48` varchar(200) DEFAULT NULL,
  `value49` varchar(20) DEFAULT NULL,
  `label49` varchar(200) DEFAULT NULL,
  `value50` varchar(20) DEFAULT NULL,
  `label50` varchar(200) DEFAULT NULL,
  `value51` varchar(20) DEFAULT NULL,
  `label51` varchar(200) DEFAULT NULL,
  `value52` varchar(20) DEFAULT NULL,
  `label52` varchar(200) DEFAULT NULL,
  `value53` varchar(20) DEFAULT NULL,
  `label53` varchar(200) DEFAULT NULL,
  `value54` varchar(20) DEFAULT NULL,
  `label54` varchar(200) DEFAULT NULL,
  `value55` varchar(20) DEFAULT NULL,
  `label55` varchar(200) DEFAULT NULL,
  `value56` varchar(20) DEFAULT NULL,
  `label56` varchar(200) DEFAULT NULL,
  `value57` varchar(20) DEFAULT NULL,
  `label57` varchar(200) DEFAULT NULL,
  `value58` varchar(20) DEFAULT NULL,
  `label58` varchar(200) DEFAULT NULL,
  `fp_fchild` tinyint(1) DEFAULT NULL,
  `fp_mother` tinyint(1) DEFAULT NULL,
  `fp_father` tinyint(1) DEFAULT NULL,
  `fp_PCG` tinyint(1) DEFAULT NULL,
  `fp_partner` tinyint(1) DEFAULT NULL,
  `fp_other` tinyint(1) DEFAULT NULL,
  `fp_none` tinyint(1) DEFAULT NULL,
  `survey` char(1) CHARACTER SET latin1 DEFAULT NULL,
  `qText` text CHARACTER SET latin1,
  `probe` text CHARACTER SET latin1,
  `measures` char(100) CHARACTER SET latin1 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `label` text,
  `value` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  CONSTRAINT `response_ibfk_1` FOREIGN KEY (`name`) REFERENCES `variable` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=718311 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `survey`
--

DROP TABLE IF EXISTS `survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `survey` (
  `id` char(1) CHARACTER SET latin1 NOT NULL,
  `name` char(100) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `topic` char(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `topic` (`topic`),
  CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`name`) REFERENCES `variable` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131802 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `umbrella`
--

DROP TABLE IF EXISTS `umbrella`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `umbrella` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` char(100) NOT NULL,
  `umbrella` char(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topic` (`topic`),
  CONSTRAINT `umbrella_ibfk_1` FOREIGN KEY (`topic`) REFERENCES `topic` (`topic`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=405 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `variable`
--

DROP TABLE IF EXISTS `variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `label` text CHARACTER SET utf8,
  `old_name` text,
  `data_type` text,
  `warning` int(11) DEFAULT NULL,
  `group_id` text,
  `group_subid` text,
  `data_source` text,
  `respondent` char(40) DEFAULT NULL,
  `wave` text,
  `scope` text,
  `section` text,
  `leaf` text,
  `measures` char(100) DEFAULT NULL,
  `probe` text,
  `qText` text,
  `fp_fchild` tinyint(1) DEFAULT NULL,
  `fp_mother` tinyint(1) DEFAULT NULL,
  `fp_father` tinyint(1) DEFAULT NULL,
  `fp_PCG` tinyint(1) DEFAULT NULL,
  `fp_partner` tinyint(1) DEFAULT NULL,
  `fp_other` tinyint(1) DEFAULT NULL,
  `survey` char(1) DEFAULT NULL,
  `focal_person` char(50) DEFAULT NULL,
  `survey2` char(100) DEFAULT NULL,
  `type` char(30) DEFAULT NULL,
  `wave2` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `measures` (`measures`),
  KEY `respondent` (`respondent`),
  KEY `survey` (`survey`),
  KEY `focal_person` (`focal_person`),
  KEY `survey2` (`survey2`)
) ENGINE=InnoDB AUTO_INCREMENT=102286 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `variable_bk`
--

DROP TABLE IF EXISTS `variable_bk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variable_bk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `label` text,
  `old_name` text,
  `data_type` text,
  `warning` int(11) DEFAULT NULL,
  `group_id` text,
  `group_subid` text,
  `data_source` text,
  `respondent` text,
  `wave` text,
  `scope` text,
  `section` text,
  `leaf` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31783 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wave`
--

DROP TABLE IF EXISTS `wave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wave` (
  `id` int(11) NOT NULL,
  `name` char(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-20 15:56:14
