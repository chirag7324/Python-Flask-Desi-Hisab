-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 31, 2021 at 06:41 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `budget_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `tblbankdeposit`
--

CREATE TABLE `tblbankdeposit` (
  `id` int(11) NOT NULL,
  `bid` int(11) DEFAULT NULL,
  `amount` decimal(18,2) DEFAULT NULL,
  `description` longtext,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblbanks`
--

CREATE TABLE `tblbanks` (
  `id` int(11) NOT NULL,
  `bank` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblborrow`
--

CREATE TABLE `tblborrow` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `trans_no` int(11) DEFAULT NULL,
  `description` longtext,
  `borrower` varchar(50) DEFAULT NULL,
  `lender` varchar(50) DEFAULT NULL,
  `bid` int(11) DEFAULT NULL,
  `ccid` int(11) DEFAULT NULL,
  `borrow_amount` decimal(18,2) DEFAULT NULL,
  `repay_amount` decimal(18,0) DEFAULT NULL,
  `balance` decimal(18,0) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `mode` varchar(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblcategory`
--

CREATE TABLE `tblcategory` (
  `id` int(11) NOT NULL,
  `category` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblccpayment`
--

CREATE TABLE `tblccpayment` (
  `id` int(11) NOT NULL,
  `ccid` int(11) DEFAULT NULL,
  `bid` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `mode` varchar(20) DEFAULT NULL,
  `amount` decimal(18,2) DEFAULT NULL,
  `description` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblcreditcard`
--

CREATE TABLE `tblcreditcard` (
  `id` int(11) NOT NULL,
  `credit_card` varchar(50) DEFAULT NULL,
  `total_credit` decimal(18,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblexpense`
--

CREATE TABLE `tblexpense` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `mode` varchar(50) DEFAULT NULL,
  `amount` decimal(18,2) DEFAULT NULL,
  `description` longtext,
  `bid` int(11) DEFAULT NULL,
  `ccid` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblincome`
--

CREATE TABLE `tblincome` (
  `id` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `description` longtext,
  `date` date DEFAULT NULL,
  `amount` decimal(18,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `month` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblrepay`
--

CREATE TABLE `tblrepay` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `trans_no` int(11) DEFAULT NULL,
  `description` longtext,
  `borrower` varchar(50) DEFAULT NULL,
  `lender` varchar(50) DEFAULT NULL,
  `bid` int(11) DEFAULT NULL,
  `ccid` int(11) DEFAULT NULL,
  `borrow_amount` decimal(18,2) DEFAULT NULL,
  `repay_amount` decimal(18,2) DEFAULT NULL,
  `balance` decimal(18,2) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `mode` varchar(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tblsaving`
--

CREATE TABLE `tblsaving` (
  `id` int(11) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `month` varchar(50) DEFAULT NULL,
  `inc_amount` decimal(18,2) DEFAULT NULL,
  `exp_amount` decimal(18,2) DEFAULT NULL,
  `saving` decimal(18,2) DEFAULT NULL,
  `nmonth` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbltransfer`
--

CREATE TABLE `tbltransfer` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `payee` varchar(50) DEFAULT NULL,
  `receiver` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `sending_amount` decimal(18,2) DEFAULT NULL,
  `rate` decimal(18,2) DEFAULT NULL,
  `received_amount` decimal(18,2) DEFAULT NULL,
  `description` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbluser`
--

CREATE TABLE `tbluser` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `firstname` varchar(20) DEFAULT NULL,
  `lastname` varchar(20) DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tblbankdeposit`
--
ALTER TABLE `tblbankdeposit`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblbanks`
--
ALTER TABLE `tblbanks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblborrow`
--
ALTER TABLE `tblborrow`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblcategory`
--
ALTER TABLE `tblcategory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblccpayment`
--
ALTER TABLE `tblccpayment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblcreditcard`
--
ALTER TABLE `tblcreditcard`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblexpense`
--
ALTER TABLE `tblexpense`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblincome`
--
ALTER TABLE `tblincome`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblrepay`
--
ALTER TABLE `tblrepay`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblsaving`
--
ALTER TABLE `tblsaving`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbltransfer`
--
ALTER TABLE `tbltransfer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbluser`
--
ALTER TABLE `tbluser`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tblbankdeposit`
--
ALTER TABLE `tblbankdeposit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblbanks`
--
ALTER TABLE `tblbanks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblborrow`
--
ALTER TABLE `tblborrow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblcategory`
--
ALTER TABLE `tblcategory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblccpayment`
--
ALTER TABLE `tblccpayment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblcreditcard`
--
ALTER TABLE `tblcreditcard`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblexpense`
--
ALTER TABLE `tblexpense`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblincome`
--
ALTER TABLE `tblincome`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblrepay`
--
ALTER TABLE `tblrepay`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbltransfer`
--
ALTER TABLE `tbltransfer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbluser`
--
ALTER TABLE `tbluser`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
