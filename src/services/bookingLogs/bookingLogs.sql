-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `bookingLogs` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bookingLogs`;

-- --------------------------------------------------------

DROP TABLE IF EXISTS `bookingLogs`;
CREATE TABLE IF NOT EXISTS `bookingLogs` (
  `bookingID` int(11) NOT NULL AUTO_INCREMENT,
  `accountID` int(32) NOT NULL,
  `startTime` TIMESTAMP NOT NULL,
  `endTime` TIMESTAMP NOT NULL,
  `price` double(6,2) NOT NULL,
  `roomID` int(32) NOT NULL,
  PRIMARY KEY (`bookingID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bookinglogs`
--

INSERT INTO `bookingLogs` (`bookingID`, `accountID`, `startTime`, `endTime`, `price`, `roomID`) VALUES
(1, 1, '2023-01-12 02:00:00', '2023-01-12 02:30:00', 20, 1);


-- --------------------------------------------------------

--
-- Table structure for table `coBooker`
--

DROP TABLE IF EXISTS `coBooker`;
CREATE TABLE IF NOT EXISTS `coBooker` (
  `accountID` int(11) NOT NULL,
  `bookingID` int(11) NOT NULL,
  `acceptStatus` char(13) NOT NULL,
  PRIMARY KEY (`accountID`, `bookingID`),
  KEY `FK_booking_id` (`bookingID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order_item`
--

INSERT INTO `coBooker` (`accountID`, `bookingID`, `acceptStatus`) VALUES
(2, 1, 'False'),
(3, 1, 'False');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_item`
--
ALTER TABLE `coBooker`
  ADD CONSTRAINT `FK_booking_id` FOREIGN KEY (`bookingID`) REFERENCES `bookingLogs` (`bookingID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
