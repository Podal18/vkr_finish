-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3312
-- Время создания: Июн 03 2025 г., 23:22
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `diplom`
--

-- --------------------------------------------------------

--
-- Структура таблицы `applications`
--

CREATE TABLE `applications` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `experience` int DEFAULT NULL,
  `vacancy_id` int DEFAULT NULL,
  `resume_text` text,
  `status` enum('new','approved','rejected') DEFAULT 'new',
  `reviewed_by` int DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `applied_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `applications`
--

INSERT INTO `applications` (`id`, `user_id`, `full_name`, `age`, `experience`, `vacancy_id`, `resume_text`, `status`, `reviewed_by`, `reviewed_at`, `applied_at`) VALUES
(1, 1, 'Кирилл Федотов', 40, 1, 1, 'Работал три года на разных объектах. Семьянин', 'approved', 3, '2025-06-03 19:31:33', '2025-05-29 21:55:21'),
(2, 2, NULL, NULL, NULL, 3, 'Резюме бухгалтера', 'approved', NULL, NULL, '2025-05-29 21:55:21'),
(3, 1, NULL, NULL, NULL, 3, 'Повторная заявка', 'approved', 3, '2025-06-03 19:31:33', '2025-05-29 21:55:21'),
(4, 5, 'Иванов Иван Иваныч', 20, 0, 4, 'Знаю азы сантехники', 'rejected', 3, '2025-06-03 19:52:33', '2025-06-03 19:47:05'),
(5, 6, 'Борисов Георгий Витальевич', 50, 10, 2, 'Работал в компании \"У Палыча\"', 'rejected', 3, '2025-06-03 19:49:46', '2025-06-03 19:49:20'),
(6, 7, 'Доровских Василий', 42, 9, 1, 'Работал в нескольких компаниях', 'approved', 3, '2025-06-03 19:52:18', '2025-06-03 19:51:57'),
(7, 8, 'Подгорнова Александра', 20, 0, 3, 'Легка в обучении', 'approved', 3, '2025-06-03 20:41:06', '2025-06-03 20:40:52'),
(8, 9, 'Кимов Сергей Сергеевич', 22, 12, 2, 'работаю 24/7 есть машина жигули', 'approved', 3, '2025-06-03 21:43:26', '2025-06-03 21:42:54');

-- --------------------------------------------------------

--
-- Структура таблицы `attendance`
--

CREATE TABLE `attendance` (
  `id` int NOT NULL,
  `employee_id` int DEFAULT NULL,
  `date` date NOT NULL,
  `status` enum('present','late','absent') NOT NULL,
  `notes` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `attendance`
--

INSERT INTO `attendance` (`id`, `employee_id`, `date`, `status`, `notes`) VALUES
(1, 1, '2020-12-12', 'present', 'Работала 5 лет по специальности'),
(2, 2, '2025-06-01', 'absent', NULL),
(3, 2, '2025-05-31', 'present', NULL),
(4, 2, '2025-05-30', 'present', NULL),
(5, 2, '2025-05-29', 'absent', NULL),
(6, 2, '2025-05-28', 'present', NULL),
(7, 2, '2025-05-27', 'late', NULL),
(8, 2, '2025-05-26', 'present', NULL),
(9, 2, '2025-05-25', 'present', NULL),
(10, 2, '2025-05-24', 'absent', NULL),
(11, 2, '2025-05-23', 'present', NULL),
(12, 2, '2025-05-22', 'absent', NULL),
(13, 2, '2025-05-21', 'present', NULL),
(14, 2, '2025-05-20', 'late', NULL),
(15, 2, '2025-05-19', 'present', NULL),
(16, 2, '2025-05-18', 'present', NULL),
(17, 2, '2025-05-17', 'present', NULL),
(18, 2, '2025-05-16', 'present', NULL),
(19, 2, '2025-05-15', 'present', NULL),
(20, 2, '2025-05-14', 'present', NULL),
(21, 2, '2025-05-13', 'present', NULL),
(22, 2, '2025-05-12', 'present', NULL),
(23, 2, '2025-05-11', 'late', NULL),
(24, 2, '2025-05-10', 'absent', NULL),
(25, 2, '2025-05-09', 'present', NULL),
(26, 2, '2025-05-08', 'present', NULL),
(27, 2, '2025-05-07', 'present', NULL),
(28, 2, '2025-05-06', 'absent', NULL),
(29, 2, '2025-05-05', 'present', NULL),
(30, 2, '2025-05-04', 'present', NULL),
(31, 2, '2025-05-03', 'present', NULL),
(32, 3, '2025-06-01', 'present', NULL),
(33, 3, '2025-05-31', 'absent', NULL),
(34, 3, '2025-05-30', 'present', NULL),
(35, 3, '2025-05-29', 'present', NULL),
(36, 3, '2025-05-28', 'late', NULL),
(37, 3, '2025-05-27', 'present', NULL),
(38, 3, '2025-05-26', 'present', NULL),
(39, 3, '2025-05-25', 'present', NULL),
(40, 3, '2025-05-24', 'present', NULL),
(41, 3, '2025-05-23', 'present', NULL),
(42, 3, '2025-05-22', 'late', NULL),
(43, 3, '2025-05-21', 'present', NULL),
(44, 3, '2025-05-20', 'present', NULL),
(45, 3, '2025-05-19', 'late', NULL),
(46, 3, '2025-05-18', 'present', NULL),
(47, 3, '2025-05-17', 'absent', NULL),
(48, 3, '2025-05-16', 'present', NULL),
(49, 3, '2025-05-15', 'present', NULL),
(50, 3, '2025-05-14', 'present', NULL),
(51, 3, '2025-05-13', 'present', NULL),
(52, 3, '2025-05-12', 'late', NULL),
(53, 3, '2025-05-11', 'present', NULL),
(54, 3, '2025-05-10', 'present', NULL),
(55, 3, '2025-05-09', 'late', NULL),
(56, 3, '2025-05-08', 'present', NULL),
(57, 3, '2025-05-07', 'present', NULL),
(58, 3, '2025-05-06', 'present', NULL),
(59, 3, '2025-05-05', 'present', NULL),
(60, 3, '2025-05-04', 'late', NULL),
(61, 3, '2025-05-03', 'present', NULL),
(62, 4, '2025-06-01', 'present', NULL),
(63, 4, '2025-05-31', 'present', NULL),
(64, 4, '2025-05-30', 'late', NULL),
(65, 4, '2025-05-29', 'present', NULL),
(66, 4, '2025-05-28', 'present', NULL),
(67, 4, '2025-05-27', 'late', NULL),
(68, 4, '2025-05-26', 'present', NULL),
(69, 4, '2025-05-25', 'present', NULL),
(70, 4, '2025-05-24', 'present', NULL),
(71, 4, '2025-05-23', 'present', NULL),
(72, 4, '2025-05-22', 'present', NULL),
(73, 4, '2025-05-21', 'present', NULL),
(74, 4, '2025-05-20', 'present', NULL),
(75, 4, '2025-05-19', 'present', NULL),
(76, 4, '2025-05-18', 'present', NULL),
(77, 4, '2025-05-17', 'absent', NULL),
(78, 4, '2025-05-16', 'present', NULL),
(79, 4, '2025-05-15', 'absent', NULL),
(80, 4, '2025-05-14', 'present', NULL),
(81, 4, '2025-05-13', 'present', NULL),
(82, 4, '2025-05-12', 'present', NULL),
(83, 4, '2025-05-11', 'present', NULL),
(84, 4, '2025-05-10', 'present', NULL),
(85, 4, '2025-05-09', 'present', NULL),
(86, 4, '2025-05-08', 'present', NULL),
(87, 4, '2025-05-07', 'present', NULL),
(88, 4, '2025-05-06', 'present', NULL),
(89, 4, '2025-05-05', 'present', NULL),
(90, 4, '2025-05-04', 'present', NULL),
(91, 4, '2025-05-03', 'present', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `employees`
--

CREATE TABLE `employees` (
  `id` int NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `profession` varchar(100) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `passport_scan_path` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `employees`
--

INSERT INTO `employees` (`id`, `full_name`, `profession`, `photo_path`, `passport_scan_path`, `is_active`, `user_id`) VALUES
(1, 'Анна Смирнова', 'HR-специалист', 'C:\\Users\\\\kapra\\PycharmProjects\\diplom\\фото\\DHS_6327_w.jpg', NULL, 1, 1),
(2, 'Игорь Кузнецов', 'Инженер', 'C:\\\\Users\\\\kapra\\\\PycharmProjects\\\\diplom\\\\фото\\\\images.jpg', NULL, 1, 6),
(3, 'Мария Орлова', 'Бухгалтер', 'C:\\Users\\\\kapra\\PycharmProjects\\diplom\\фото\\DHS_6327_w.jpg', NULL, 0, 4),
(4, 'Сергей Петров', 'Прораб', 'C:\\\\Users\\\\kapra\\\\PycharmProjects\\\\diplom\\\\фото\\\\Foto-na-dokumenty-ot-pechaterfoto-3.jpg', NULL, 0, 3),
(5, 'test_user1', 'Инженер ПТО', NULL, NULL, 1, 5),
(6, 'test_user1', 'Инженер ПТО', NULL, NULL, 1, 2),
(7, 'Vasiliy', 'Инженер ПТО', 'C:/Users/kapra/OneDrive/Рабочий стол/49476038-2492844.jpg', 'C:/Users/kapra/OneDrive/Рабочий стол/49476038-2492844.jpg', 1, 7),
(8, 'Sasha', 'Бухгалтер', 'C:/Users/kapra/OneDrive/Изображения/image_1.jpg', NULL, 1, NULL),
(9, 'sergey', 'Прораб', 'C:/Users/kapra/PycharmProjects/diplom/фото/Foto-na-dokumenty-ot-pechaterfoto-3.jpg', 'C:/Users/kapra/PycharmProjects/diplom/фото/DHS_6327_w.jpg', 0, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `firings`
--

CREATE TABLE `firings` (
  `id` int NOT NULL,
  `employee_id` int DEFAULT NULL,
  `reason` text,
  `fired_by` int DEFAULT NULL,
  `fired_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `firings`
--

INSERT INTO `firings` (`id`, `employee_id`, `reason`, `fired_by`, `fired_at`) VALUES
(2, 4, 'Нарушение трудовой дисциплины', 1, '2025-05-29 21:55:29'),
(3, 1, 'Уволен вручную', 1, '2025-06-01 10:32:36'),
(4, 1, 'Уволен вручную', 3, '2025-06-02 14:31:48'),
(5, 3, 'прогулы', 1, '2025-06-02 18:03:54'),
(6, 4, 'Опоздания', 3, '2025-06-03 19:53:34');

-- --------------------------------------------------------

--
-- Структура таблицы `logs`
--

CREATE TABLE `logs` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `logs`
--

INSERT INTO `logs` (`id`, `user_id`, `action`, `description`, `created_at`) VALUES
(2, 5, 'Регистрация', 'Зарегистрирован новый пользователь Ivan с ролью 4', '2025-05-31 00:53:12'),
(3, 5, 'Сброс пароля', 'Пользователь Ivan сбросил пароль', '2025-05-31 00:54:27'),
(4, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:12:08'),
(5, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:12:45'),
(6, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:12:53'),
(7, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:14:30'),
(8, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-01 09:16:00'),
(9, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:16:35'),
(10, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:17:36'),
(11, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:50:53'),
(12, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-01 09:57:49'),
(13, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 13:07:58'),
(14, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 14:24:27'),
(15, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 14:30:39'),
(16, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 14:31:24'),
(17, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 15:57:12'),
(18, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 16:02:59'),
(19, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 17:31:53'),
(20, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 18:04:30'),
(21, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 19:18:15'),
(22, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 19:19:46'),
(23, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 19:21:00'),
(24, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 19:21:46'),
(25, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-02 19:26:05'),
(26, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-02 19:26:47'),
(27, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-02 19:27:03'),
(28, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-02 19:27:21'),
(29, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-02 19:38:19'),
(30, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 19:29:47'),
(31, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 19:33:39'),
(32, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 19:39:10'),
(33, 5, 'Вход', 'Пользователь с ID 5 вошёл в систему', '2025-06-03 19:45:33'),
(34, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 19:47:25'),
(35, 6, 'Регистрация', 'Зарегистрирован новый пользователь Georgiy с ролью 4', '2025-06-03 19:48:14'),
(36, 6, 'Вход', 'Пользователь с ID 6 вошёл в систему', '2025-06-03 19:48:26'),
(37, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 19:49:37'),
(38, 6, 'Вход', 'Пользователь с ID 6 вошёл в систему', '2025-06-03 19:50:06'),
(39, 7, 'Регистрация', 'Зарегистрирован новый пользователь Vasiliy с ролью 4', '2025-06-03 19:51:20'),
(40, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 19:51:27'),
(41, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 19:52:09'),
(42, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-03 20:13:25'),
(43, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:15:45'),
(44, 1, 'Вход', 'Пользователь с ID 1 вошёл в систему', '2025-06-03 20:16:09'),
(45, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:20:04'),
(46, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 20:20:50'),
(47, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 20:22:17'),
(48, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 20:22:48'),
(49, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:25:13'),
(50, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:30:57'),
(51, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:31:11'),
(52, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 20:31:56'),
(53, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:32:08'),
(54, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:35:59'),
(55, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:36:21'),
(56, 7, 'Вход', 'Пользователь с ID 7 вошёл в систему', '2025-06-03 20:37:18'),
(57, 8, 'Регистрация', 'Зарегистрирован новый пользователь Sasha с ролью 4', '2025-06-03 20:38:23'),
(58, 8, 'Вход', 'Пользователь с ID 8 вошёл в систему', '2025-06-03 20:38:43'),
(59, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 20:41:03'),
(60, 8, 'Вход', 'Пользователь с ID 8 вошёл в систему', '2025-06-03 20:41:19'),
(61, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 20:41:43'),
(62, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-03 20:42:12'),
(63, 6, 'Вход', 'Пользователь с ID 6 вошёл в систему', '2025-06-03 20:52:21'),
(64, 6, 'Вход', 'Пользователь с ID 6 вошёл в систему', '2025-06-03 20:52:51'),
(65, 6, 'Вход', 'Пользователь с ID 6 вошёл в систему', '2025-06-03 20:57:26'),
(66, 6, 'Вход', 'Пользователь с ID 6 вошёл в систему', '2025-06-03 20:59:00'),
(67, 9, 'Регистрация', 'Зарегистрирован новый пользователь sergey с ролью 4', '2025-06-03 21:40:47'),
(68, 9, 'Вход', 'Пользователь с ID 9 вошёл в систему', '2025-06-03 21:41:06'),
(69, 3, 'Вход', 'Пользователь с ID 3 вошёл в систему', '2025-06-03 21:43:18'),
(70, 9, 'Вход', 'Пользователь с ID 9 вошёл в систему', '2025-06-03 21:44:28'),
(71, 9, 'Вход', 'Пользователь с ID 9 вошёл в систему', '2025-06-03 21:45:23'),
(72, 4, 'Вход', 'Пользователь с ID 4 вошёл в систему', '2025-06-03 21:45:40');

-- --------------------------------------------------------

--
-- Структура таблицы `motivation_actions`
--

CREATE TABLE `motivation_actions` (
  `id` int NOT NULL,
  `employee_id` int DEFAULT NULL,
  `action_type` enum('bonus','training','promotion') NOT NULL,
  `reason` text,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `motivation_actions`
--

INSERT INTO `motivation_actions` (`id`, `employee_id`, `action_type`, `reason`, `created_by`, `created_at`) VALUES
(1, 1, 'promotion', 'qwrty', 3, '2025-06-02 14:24:36'),
(2, 1, 'bonus', 'ЗА старательную работу', 3, '2025-06-02 18:05:14'),
(3, 4, 'promotion', 'test', 3, '2025-06-02 18:06:06'),
(4, 2, 'promotion', 'За успехи в работе', 3, '2025-06-03 19:53:07'),
(5, 9, 'promotion', 'заслужил', 3, '2025-06-03 21:44:05');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'Administrator'),
(2, 'Employee'),
(3, 'HR'),
(4, 'Candidat'),
(5, 'Uvolenni');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `login` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password_hash`, `role`, `created_at`) VALUES
(1, 'test_user1', 'hash1', 2, '2025-05-29 21:55:21'),
(2, 'test_user2', 'hash2', 4, '2025-05-29 21:55:21'),
(3, 'hr', 'hr', 3, '2025-05-29 22:24:50'),
(4, 'adm', 'adm', 1, '2025-05-29 22:25:17'),
(5, 'Ivan', '111', 5, '2025-05-31 00:53:11'),
(6, 'Georgiy', '123', 5, '2025-06-03 19:48:13'),
(7, 'Vasiliy', '123', 2, '2025-06-03 19:51:19'),
(8, 'Sasha', '123', 2, '2025-06-03 20:38:22'),
(9, 'sergey', 'qwerty123', 5, '2025-06-03 21:40:46');

-- --------------------------------------------------------

--
-- Структура таблицы `vacancies`
--

CREATE TABLE `vacancies` (
  `id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `employment_type` enum('ТК','ГПХ','Самозанятый') NOT NULL,
  `required_experience` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `vacancies`
--

INSERT INTO `vacancies` (`id`, `title`, `city`, `salary`, `employment_type`, `required_experience`, `is_active`) VALUES
(1, 'Инженер ПТО', 'Москва', '80000.00', 'ТК', 3, 1),
(2, 'Прораб', 'Санкт-Петербург', '90000.00', 'ГПХ', 5, 1),
(3, 'Бухгалтер', 'Казань', '70000.00', 'Самозанятый', 2, 1),
(4, 'Сантехник', 'Москва', '40000.00', 'Самозанятый', 0, 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `vacancy_id` (`vacancy_id`),
  ADD KEY `reviewed_by` (`reviewed_by`);

--
-- Индексы таблицы `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Индексы таблицы `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Индексы таблицы `firings`
--
ALTER TABLE `firings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `fired_by` (`fired_by`);

--
-- Индексы таблицы `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `motivation_actions`
--
ALTER TABLE `motivation_actions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`login`),
  ADD KEY `role` (`role`);

--
-- Индексы таблицы `vacancies`
--
ALTER TABLE `vacancies`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT для таблицы `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `firings`
--
ALTER TABLE `firings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT для таблицы `motivation_actions`
--
ALTER TABLE `motivation_actions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `vacancies`
--
ALTER TABLE `vacancies`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`vacancy_id`) REFERENCES `vacancies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `applications_ibfk_3` FOREIGN KEY (`reviewed_by`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `fk_employee_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `firings`
--
ALTER TABLE `firings`
  ADD CONSTRAINT `firings_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`),
  ADD CONSTRAINT `firings_ibfk_2` FOREIGN KEY (`fired_by`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `logs`
--
ALTER TABLE `logs`
  ADD CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `motivation_actions`
--
ALTER TABLE `motivation_actions`
  ADD CONSTRAINT `motivation_actions_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`),
  ADD CONSTRAINT `motivation_actions_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
