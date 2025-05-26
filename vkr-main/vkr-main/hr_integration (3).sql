-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3312
-- Время создания: Май 27 2025 г., 00:52
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
-- База данных: `hr_integration`
--

-- --------------------------------------------------------

--
-- Структура таблицы `assignments`
--

CREATE TABLE `assignments` (
  `id` int NOT NULL,
  `employee_id` int NOT NULL,
  `project_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `assignments`
--

INSERT INTO `assignments` (`id`, `employee_id`, `project_id`, `start_date`, `end_date`) VALUES
(1, 1, 1, '2024-05-01', NULL),
(3, 11, 5, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `discipline`
--

CREATE TABLE `discipline` (
  `id` int NOT NULL,
  `employee_id` int NOT NULL,
  `violation_type` varchar(100) DEFAULT NULL,
  `violation_date` date DEFAULT NULL,
  `comments` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `discipline`
--

INSERT INTO `discipline` (`id`, `employee_id`, `violation_type`, `violation_date`, `comments`) VALUES
(1, 1, 'Опоздание', '2024-05-10', 'Прибыл на объект на 30 минут позже'),
(2, 2, 'Прогул', '2024-04-22', 'Отсутствовал без уважительной причины'),
(3, 1, 'Опоздание', '2024-05-10', 'Опоздание на 30 минут'),
(10, 9, 'Нарушение ТБ', '2024-05-15', NULL),
(11, 10, 'Опоздание', '2024-06-01', NULL),
(12, 11, 'Прогул', '2024-05-20', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `documents`
--

CREATE TABLE `documents` (
  `id` int NOT NULL,
  `employee_id` int NOT NULL,
  `doc_type` varchar(100) DEFAULT NULL,
  `doc_number` varchar(100) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `documents`
--

INSERT INTO `documents` (`id`, `employee_id`, `doc_type`, `doc_number`, `issue_date`, `expiry_date`) VALUES
(1, 1, 'Удостоверение сварщика', 'SW123456', '2023-01-01', '2026-01-01'),
(2, 1, 'Медсправка', 'MD123456', '2024-01-10', '2025-01-10'),
(3, 2, 'Допуск по электробезопасности', 'EL654321', '2023-02-01', '2025-02-01'),
(4, 2, 'Медсправка', 'MD654321', '2024-03-15', '2025-03-15'),
(5, 9, 'Удостоверение сварщика', NULL, NULL, '2025-06-01'),
(6, 10, 'Допуск по электробезопасности', NULL, NULL, '2024-12-31'),
(7, 11, 'Удостоверение прораба', NULL, NULL, '2025-03-15');

-- --------------------------------------------------------

--
-- Структура таблицы `employees`
--

CREATE TABLE `employees` (
  `id` int NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `profession_id` int DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_by` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `employees`
--

INSERT INTO `employees` (`id`, `full_name`, `birth_date`, `profession_id`, `status`, `created_by`) VALUES
(1, 'Иванов Иван Иванович', '1985-03-10', 1, 'active', 1),
(2, 'Петров Пётр Петрович', '1990-06-25', 2, 'active', 1),
(3, 'Сидоров Сидор Сидорович', '1978-11-02', 3, 'inactive', 1),
(9, 'hrr', '2000-01-01', 3, 'active', 15),
(10, 'saff', '2000-01-01', 3, 'active', 16),
(11, 'fore', '2000-01-01', 2, 'active', 17),
(12, 'admm', '2000-01-01', 1, 'inactive', 18),
(41, 'Александра Подгорнова', '2000-01-01', 2, 'active', 20);

-- --------------------------------------------------------

--
-- Структура таблицы `logs`
--

CREATE TABLE `logs` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  `employee_id` int DEFAULT NULL,
  `log_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `logs`
--

INSERT INTO `logs` (`id`, `user_id`, `action`, `employee_id`, `log_date`) VALUES
(1, 15, 'Добавлен сотрудник', 1, '2025-05-22 15:49:50'),
(2, 2, 'Добавлен сотрудник', 2, '2025-05-22 15:49:50'),
(3, 17, 'Назначен сотрудник на объект', 1, '2025-05-22 15:49:50');

-- --------------------------------------------------------

--
-- Структура таблицы `professions`
--

CREATE TABLE `professions` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `required_documents` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `professions`
--

INSERT INTO `professions` (`id`, `name`, `required_documents`) VALUES
(1, 'Сварщик', 'Удостоверение сварщика, Медсправка'),
(2, 'Электрик', 'Допуск по электробезопасности, Медсправка'),
(3, 'Прораб', 'Удостоверение прораба, Медсправка');

-- --------------------------------------------------------

--
-- Структура таблицы `projects`
--

CREATE TABLE `projects` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `projects`
--

INSERT INTO `projects` (`id`, `name`, `address`) VALUES
(1, 'ЖК Северный Ветер', 'Москва, ул. Строителей, 12'),
(3, 'Реутов Парк', 'ш. Энтузиастов, 5'),
(4, 'name_object', 'adress_object'),
(5, 'name object 2', 'adress object 2');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `name`, `description`) VALUES
(1, 'HR', 'Специалист по кадрам'),
(2, 'Foreman', 'Прораб на объекте'),
(3, 'SafetyEngineer', 'Инженер по охране труда'),
(4, 'Admin', 'Администратор системы');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password_hash`, `role_id`) VALUES
(1, 'hr_user', '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5', 1),
(2, 'foreman_user', 'пароль_в_чистом_виде', 2),
(3, 'safety_user', 'пароль_в_чистом_виде', 3),
(15, 'hrr', '558f0192396182d608911e5d91d53684a85607ba84d73fb8533403117ccf8b94', 1),
(16, 'saff', '762add2f8fff945c5fd60d508de70ee5fa1509a231624e64744991ce6a9efb12', 3),
(17, 'fore', 'affe69d75e6778ca751245a5e0705e5e29df0735d4947a4f0fa5b217eec669b0', 2),
(18, 'admm', '7378e12d73a79bc6e1f5ab1967fc07a2dad3e652d40f13a5f66a5eebaab91d97', 4),
(20, 'Podal18', '688787d8ff144c502c7f5cffaafe2cc588d86079f9de88304c26b0cb99ce91c6', 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `assignments`
--
ALTER TABLE `assignments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `project_id` (`project_id`);

--
-- Индексы таблицы `discipline`
--
ALTER TABLE `discipline`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Индексы таблицы `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Индексы таблицы `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profession_id` (`profession_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Индексы таблицы `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `professions`
--
ALTER TABLE `professions`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `assignments`
--
ALTER TABLE `assignments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `discipline`
--
ALTER TABLE `discipline`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT для таблицы `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `professions`
--
ALTER TABLE `professions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `assignments`
--
ALTER TABLE `assignments`
  ADD CONSTRAINT `assignments_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`),
  ADD CONSTRAINT `assignments_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);

--
-- Ограничения внешнего ключа таблицы `discipline`
--
ALTER TABLE `discipline`
  ADD CONSTRAINT `discipline_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`);

--
-- Ограничения внешнего ключа таблицы `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`);

--
-- Ограничения внешнего ключа таблицы `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`profession_id`) REFERENCES `professions` (`id`),
  ADD CONSTRAINT `employees_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `logs`
--
ALTER TABLE `logs`
  ADD CONSTRAINT `logs_ibfk_2` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`),
  ADD CONSTRAINT `logs_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
