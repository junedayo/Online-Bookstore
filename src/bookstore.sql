-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2024-06-16 13:03:41
-- サーバのバージョン： 10.4.32-MariaDB
-- PHP のバージョン: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `bookstore`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `admins`
--

CREATE TABLE `admins` (
  `ID` int(10) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `admins`
--

INSERT INTO `admins` (`ID`, `username`, `password`) VALUES
(1, 'Chris', '123456'),
(2, 'Antonis', 'qwerty'),
(3, 'Sofia', '000000'),
(4, 'Panos', '123123');

-- --------------------------------------------------------

--
-- テーブルの構造 `books`
--

CREATE TABLE `books` (
  `ISBN` varchar(12) NOT NULL,
  `title` varchar(30) NOT NULL,
  `author` varchar(30) NOT NULL,
  `publisher` varchar(30) NOT NULL,
  `genre` varchar(30) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(100) NOT NULL,
  `date` date DEFAULT NULL,
  `cover` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `books`
--

INSERT INTO `books` (`ISBN`, `title`, `author`, `publisher`, `genre`, `price`, `stock`, `date`, `cover`) VALUES
('01', 'Kafka on the Shore', 'Murakami Haruki', 'Vintage Books', 'Literature', 12.99, 10, '2002-09-12', 'kafka_on_the_shore.jpg'),
('02', '1Q84 Books 1 and 2', 'Murakami Haruki', 'Vintage Books', 'Literature', 13.99, 9, '2009-05-29', '1q84_1.jpg'),
('03', '1Q84 Book 3', 'Murakami Haruki', 'Vintage Books', 'Literature', 13.99, 1, '2010-04-10', '1q84_3.jpg'),
('04', 'Kokoro', 'Natsume Soseki', 'Vintage Books', 'Literature', 11.99, 4, '1914-08-11', 'kokoro.jpg'),
('05', 'Nakahara Chuuya Poems', 'Nakahara Chuuya', 'Gracewing', 'Poems', 16.99, 0, '2004-02-01', 'chuuya_poems.jpg'),
('06', '100 poems, 100 authors', '-', 'Penguin Classics', 'Poems', 12.99, 9, '2007-07-20', 'poems.jpg'),
('07', 'Goodnight Punpun Volume 1', 'Asano Inio', 'VIZ Media LLC', 'Manga', 16.99, 2, '2007-08-03', 'pun_1.jpg'),
('08', 'Goodnight Punpun Volume 2', 'Asano Inio', 'VIZ Media LLC', 'Manga', 16.99, 4, '2007-12-28', 'pun_2.jpg'),
('09', 'Goodnight Punpun Volume 3', 'Asano Inio', 'VIZ Media LLC', 'Manga', 16.99, 5, '2008-06-05', 'pun_3.jpg'),
('10', 'JOJO Stone Ocean Volume 1', 'Araki Hirohiko', 'VIZ Media LLC', 'Manga', 12.99, 23, '2008-04-18', 'stone_ocean_1.jpg'),
('11', 'JOJO Stone Ocean Volume 2', 'Araki Hirohiko', 'VIZ Media LLC', 'Manga', 12.99, 1, '2008-05-16', 'stone_ocean_2.jpg'),
('12', 'JOJO Stone Ocean Volume 3', 'Araki Hirohiko', 'VIZ Media LLC', 'Manga', 12.99, 21, '2008-06-18', 'stone_ocean_3.jpg'),
('13', 'Snow Country', 'Kawabata Yasunari', 'Knopf Doubleday Publishing Gro', 'Literature', 9.99, 25, '1948-11-05', 'snow_country.jpg');

-- --------------------------------------------------------

--
-- テーブルの構造 `buys`
--

CREATE TABLE `buys` (
  `Transaction_ID` int(100) NOT NULL,
  `Admin_ID` int(10) NOT NULL,
  `book_ISBN` varchar(12) NOT NULL,
  `quantity` int(30) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `buys`
--

INSERT INTO `buys` (`Transaction_ID`, `Admin_ID`, `book_ISBN`, `quantity`, `date`) VALUES
(2, 1, '13', 1, '2024-06-14'),
(3, 1, '13', 6, '2024-06-14'),
(4, 2, '13', 6, '2024-06-14'),
(5, 3, '13', 7, '2024-06-14'),
(6, 2, '13', 1, '2024-06-14'),
(7, 1, '13', 2, '2024-06-14'),
(8, 2, '13', 1, '2024-06-14'),
(9, 3, '13', 2, '2024-06-14'),
(10, 3, '13', 1, '2024-06-14'),
(11, 4, '13', 2, '2024-06-14'),
(12, 4, '13', 1, '2024-06-14'),
(13, 1, '13', 1, '2024-06-14'),
(35, 2, '13', 1, '2024-06-14'),
(36, 2, '02', 2, '2024-06-14'),
(37, 3, '03', 2, '2024-06-14'),
(38, 4, '02', 6, '2024-06-14'),
(39, 3, '03', 4, '2024-06-14'),
(40, 2, '12', 1, '2024-06-16'),
(41, 2, '12', 1, '2024-06-16'),
(42, 2, '06', 11, '2024-06-16'),
(43, 2, '11', 7, '2024-06-16'),
(44, 2, '10', 6, '2024-06-16'),
(45, 2, '12', 6, '2024-06-16');

-- --------------------------------------------------------

--
-- テーブルの構造 `customers`
--

CREATE TABLE `customers` (
  `id` int(12) NOT NULL,
  `name` varchar(30) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `country` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `street` varchar(30) NOT NULL,
  `street_num` varchar(3) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `customers`
--

INSERT INTO `customers` (`id`, `name`, `username`, `password`, `country`, `city`, `street`, `street_num`, `postal_code`, `phone`, `email`) VALUES
(1, 'babis', 'user', '123456789', 'greece', 'athens', 'babis', '51', '11242', '6985414123', 'babis@gmail.com'),
(2, 'Sofiaa', 'sofiaaa', '12345', 'greece', 'athens', 'miaou', '2', '35100', '6940884497', 'dndif@jfi.com'),
(3, 'sofia', 'sofini', '12345', 'greece', 'ath', 'ath', '2', '12345', '1234567890', 'sof@gmail.com'),
(4, 'test', 'test', '12345', 'sdvc', 'dsvgsdft', 'detf', '3', '12345', '1234565890', 'sdvg@gmail.com'),
(5, 'june', 'june', 'june', 'Greece', 'Athens', 'AAAA', '123', 'AB21', '293832934', 'june@gmail.com'),
(7, 'jotaro', 'jotaro', '123', 'Japan', 'MORIOH', 'JOJOJOJOJOJO', '2', '23788237', '48937934', 'jotaro@gmail.com'),
(8, 'jolyne', 'jolyne', 'jolyne', 'Japan', 'JAIL', 'Jojolili', '123', 'JJ11', '283829932', 'jolyne@gmail.com'),
(9, 'takis', 'patatakis', 'takis', 'PATATAKI', 'TAKICITY', 'TAKISTREET', '2', 'TATA1212', '7834678348', 'takispatatakis@gmail.com'),
(10, 'babis', 'babis', 'babis', 'Greece', 'BABITOWN', 'BB', '1', '21221', '3897278923', 'babb@gmail.com'),
(11, 'nick', 'nick', 'nick', 'Greece', 'Athens', 'JOJOJO', '2', '3232', '23763482', 'nick@gmail.com'),
(12, 'kon', 'kon', 'kon', 'Greece', 'Athens', 'Konstreet', '323', '3232', '87328237', 'kon@gmail.com'),
(13, 'kaori', 'kaori', 'kaori', 'Japan', 'Shimada', 'Nakashi', '111', '322AA', '9372382', 'kaori@gmail.com');

-- --------------------------------------------------------

--
-- テーブルの構造 `sells`
--

CREATE TABLE `sells` (
  `Transaction_ID` int(100) NOT NULL,
  `customer_id` int(10) NOT NULL,
  `book_ISBN` varchar(12) NOT NULL,
  `quantity` int(30) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `sells`
--

INSERT INTO `sells` (`Transaction_ID`, `customer_id`, `book_ISBN`, `quantity`, `date`) VALUES
(0, 9, '11', 1, '2024-06-03'),
(3, 3, '13', 1, '2024-06-05'),
(4, 3, '13', 1, '2024-06-13'),
(5, 3, '13', 1, '2024-05-14'),
(7, 3, '13', 1, '2024-06-12'),
(8, 3, '13', 1, '2024-06-08'),
(11, 3, '13', 1, '2024-06-10'),
(15, 3, '12', 1, '2024-06-15'),
(17, 3, '08', 1, '2024-06-04'),
(19, 3, '04', 1, '2024-06-01'),
(20, 3, '04', 1, '2024-06-03'),
(21, 3, '11', 1, '2024-06-12'),
(22, 3, '01', 1, '2024-06-08'),
(23, 5, '11', 2, '2024-06-01'),
(24, 5, '12', 2, '2024-06-14'),
(25, 5, '07', 4, '2024-06-14'),
(26, 5, '08', 2, '2024-06-14'),
(27, 5, '09', 2, '2024-06-09'),
(28, 3, '13', 2, '2024-06-05'),
(29, 5, '11', 1, '2024-06-06'),
(30, 5, '12', 1, '2024-06-02'),
(31, 5, '13', 1, '2024-06-12'),
(32, 5, '05', 1, '2024-06-12'),
(33, 5, '05', 2, '2024-06-08'),
(34, 5, '06', 1, '2024-06-08'),
(35, 5, '01', 1, '2024-06-12'),
(36, 5, '03', 2, '2024-06-12'),
(37, 5, '01', 2, '2024-06-01'),
(38, 5, '02', 1, '2024-06-09'),
(39, 5, '10', 1, '2024-06-04'),
(40, 5, '06', 1, '2024-06-06'),
(41, 8, '07', 1, '2024-06-10'),
(42, 8, '08', 1, '2024-06-10'),
(43, 8, '08', 1, '2024-06-12'),
(44, 8, '09', 1, '2024-06-12'),
(45, 8, '07', 2, '2024-06-15'),
(46, 8, '09', 2, '2024-06-15'),
(47, 8, '06', 2, '2024-06-08'),
(48, 8, '13', 2, '2024-06-05'),
(49, 9, '10', 1, '2024-06-03'),
(51, 9, '12', 1, '2024-06-03'),
(52, 5, '12', 1, '2024-06-16'),
(54, 5, '03', 1, '2024-06-16'),
(55, 5, '02', 1, '2024-06-16'),
(56, 5, '03', 1, '2024-06-16'),
(57, 5, '02', 1, '2024-06-16'),
(58, 9, '03', 1, '2024-06-02'),
(59, 9, '02', 1, '2024-06-16'),
(60, 9, '03', 1, '2024-06-16'),
(61, 9, '02', 1, '2024-06-11'),
(62, 9, '01', 1, '2024-06-16'),
(63, 9, '03', 1, '2024-06-11'),
(64, 9, '02', 1, '2024-06-01'),
(65, 10, '12', 2, '2024-06-16'),
(66, 10, '11', 1, '2024-06-16'),
(67, 11, '12', 2, '2024-06-16'),
(68, 11, '10', 1, '2024-06-16'),
(69, 2, '11', 1, '2024-06-16'),
(70, 2, '10', 1, '2024-06-16'),
(71, 4, '12', 1, '2024-06-16'),
(72, 4, '10', 1, '2024-06-16'),
(73, 4, '11', 1, '2024-06-16'),
(74, 12, '12', 2, '2024-06-16'),
(75, 12, '11', 2, '2024-06-16'),
(76, 12, '10', 1, '2024-06-16'),
(77, 13, '10', 1, '2024-06-16'),
(78, 13, '11', 1, '2024-06-16'),
(79, 7, '10', 1, '2024-06-16'),
(80, 7, '11', 1, '2024-06-16'),
(81, 7, '12', 1, '2024-06-16');

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`ID`);

--
-- テーブルのインデックス `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`ISBN`);

--
-- テーブルのインデックス `buys`
--
ALTER TABLE `buys`
  ADD PRIMARY KEY (`Transaction_ID`),
  ADD KEY `book_ISBN` (`book_ISBN`),
  ADD KEY `Admin_ID` (`Admin_ID`);

--
-- テーブルのインデックス `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `sells`
--
ALTER TABLE `sells`
  ADD PRIMARY KEY (`Transaction_ID`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `book_ISBN` (`book_ISBN`) USING BTREE;

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `admins`
--
ALTER TABLE `admins`
  MODIFY `ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- テーブルの AUTO_INCREMENT `buys`
--
ALTER TABLE `buys`
  MODIFY `Transaction_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- テーブルの AUTO_INCREMENT `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- テーブルの AUTO_INCREMENT `sells`
--
ALTER TABLE `sells`
  MODIFY `Transaction_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;

--
-- ダンプしたテーブルの制約
--

--
-- テーブルの制約 `buys`
--
ALTER TABLE `buys`
  ADD CONSTRAINT `buys_ibfk_1` FOREIGN KEY (`book_ISBN`) REFERENCES `books` (`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `buys_ibfk_2` FOREIGN KEY (`Admin_ID`) REFERENCES `admins` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- テーブルの制約 `sells`
--
ALTER TABLE `sells`
  ADD CONSTRAINT `sells_ibfk_2` FOREIGN KEY (`book_ISBN`) REFERENCES `books` (`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sells_ibfk_3` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
