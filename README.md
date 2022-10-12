# AL-Hosn

<b>Required Modules:</b>
1. base64
2. calendar
3. datetime
4. os
5. sys
6. mysql.connector
7. webview
8. qrcode

create the database and table properties in mysql cmd using these code:

<b>Database:</b>

<code>CREATE DATABASE covid</code>

<b>Reports Table:</b>

<code>CREATE TABLE `Reports` (
  `em_id` varchar(20) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `statusdate` date DEFAULT NULL,
  `HistoryStatus` varchar(1) DEFAULT NULL,
  `HistoryDate` date DEFAULT NULL,
  `Vaccinated` tinyint(1) DEFAULT NULL,
  `Vaccination` varchar(10) DEFAULT NULL,
  `qr_code` blob,
  `liststatus` varchar(100) NULL,
  `listdate` varchar(1000) NULL
);</code>

<b>Users Table:</b>

<code>CREATE TABLE `Users` (
  `emirates_id` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `address` varchar(150) DEFAULT NULL
);</code>
