-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.64-MariaDB - MariaDB Server
-- Server OS:                    Linux
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table FFMeta.data_type
DROP TABLE IF EXISTS `data_type`;
CREATE TABLE IF NOT EXISTS `data_type` (
  `id` char(30) NOT NULL,
  `name` char(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.group
DROP TABLE IF EXISTS `group`;
CREATE TABLE IF NOT EXISTS `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` text,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.measure
DROP TABLE IF EXISTS `measure`;
CREATE TABLE IF NOT EXISTS `measure` (
  `id` tinyint(1) NOT NULL,
  `name` char(100) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.raw2
DROP TABLE IF EXISTS `raw2`;
CREATE TABLE IF NOT EXISTS `raw2` (
  `new_name` char(40) DEFAULT NULL,
  `old_name` char(40) DEFAULT NULL,
  `varlab` text,
  `group` char(30) DEFAULT NULL,
  `topics` char(120) DEFAULT NULL,
  `subtopics` char(120) DEFAULT NULL,
  `n_cities_asked` int(4) DEFAULT NULL,
  `q_group_N` int(11) DEFAULT NULL,
  `q_group_list` text,
  `type` char(30) DEFAULT NULL,
  `warning` char(200) CHARACTER SET latin1 DEFAULT NULL,
  `scale` char(100) CHARACTER SET latin1 DEFAULT NULL,
  `scope` char(10) DEFAULT NULL,
  `source` char(30) DEFAULT NULL,
  `respondent` char(30) DEFAULT NULL,
  `wave` char(30) CHARACTER SET latin1 DEFAULT NULL,
  `section` char(1) DEFAULT NULL,
  `leaf` char(30) DEFAULT NULL,
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
  `survey` char(100) DEFAULT NULL,
  `qtext` text CHARACTER SET latin1,
  `probe` text CHARACTER SET latin1,
  `in_FFC_file` char(20) CHARACTER SET latin1 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.response2
DROP TABLE IF EXISTS `response2`;
CREATE TABLE IF NOT EXISTS `response2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(40) DEFAULT NULL,
  `label` text,
  `value` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  CONSTRAINT `response2_ibfk_1` FOREIGN KEY (`name`) REFERENCES `variable3` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3843497 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.subtopics
DROP TABLE IF EXISTS `subtopics`;
CREATE TABLE IF NOT EXISTS `subtopics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subtopic` char(50) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=783 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.survey
DROP TABLE IF EXISTS `survey`;
CREATE TABLE IF NOT EXISTS `survey` (
  `id` char(1) CHARACTER SET latin1 NOT NULL,
  `name` char(100) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.topic
DROP TABLE IF EXISTS `topic`;
CREATE TABLE IF NOT EXISTS `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `topic` char(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `topic` (`topic`),
  CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`name`) REFERENCES `variable` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131070 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.topics
DROP TABLE IF EXISTS `topics`;
CREATE TABLE IF NOT EXISTS `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` char(50) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.umbrella
DROP TABLE IF EXISTS `umbrella`;
CREATE TABLE IF NOT EXISTS `umbrella` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` char(100) NOT NULL,
  `umbrella` char(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topic` (`topic`),
  CONSTRAINT `umbrella_ibfk_1` FOREIGN KEY (`topic`) REFERENCES `topic` (`topic`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=347 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.variable
DROP TABLE IF EXISTS `variable`;
CREATE TABLE IF NOT EXISTS `variable` (
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

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.variable3
DROP TABLE IF EXISTS `variable3`;
CREATE TABLE IF NOT EXISTS `variable3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(40) DEFAULT NULL,
  `label` text CHARACTER SET utf8,
  `old_name` char(40) CHARACTER SET utf8 DEFAULT NULL,
  `warning` char(200) DEFAULT NULL,
  `group_id` text,
  `data_source` char(20) DEFAULT NULL,
  `respondent` char(40) DEFAULT NULL,
  `n_cities_asked` int(11) DEFAULT NULL,
  `section` text,
  `leaf` text,
  `scale` char(100) DEFAULT NULL,
  `probe` text,
  `qText` text,
  `fp_fchild` tinyint(1) DEFAULT NULL,
  `fp_mother` tinyint(1) DEFAULT NULL,
  `fp_father` tinyint(1) DEFAULT NULL,
  `fp_PCG` tinyint(1) DEFAULT NULL,
  `fp_partner` tinyint(1) DEFAULT NULL,
  `fp_other` tinyint(1) DEFAULT NULL,
  `focal_person` char(50) DEFAULT NULL,
  `survey` char(100) DEFAULT NULL,
  `data_type` char(30) DEFAULT NULL,
  `wave` char(10) DEFAULT NULL,
  `topics` char(200) DEFAULT NULL COMMENT 'Calculated field - concatenation of topic1/topic2 suitable for search results.',
  `subtopics` char(200) DEFAULT NULL COMMENT 'Calculated field - concatenation of subtopic1/subtopic2 suitable for search results.',
  `in_FFC_file` char(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `survey2` (`survey`),
  KEY `measures` (`scale`),
  KEY `wave` (`wave`),
  KEY `respondent` (`respondent`),
  KEY `data_source` (`data_source`),
  KEY `data_type` (`data_type`),
  KEY `focal_person` (`focal_person`),
  KEY `topics` (`topics`),
  KEY `subtopics` (`subtopics`)
) ENGINE=InnoDB AUTO_INCREMENT=348995 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.variable_bk
DROP TABLE IF EXISTS `variable_bk`;
CREATE TABLE IF NOT EXISTS `variable_bk` (
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table FFMeta.wave
DROP TABLE IF EXISTS `wave`;
CREATE TABLE IF NOT EXISTS `wave` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `order_id` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
