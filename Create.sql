CREATE SCHEMA IF NOT EXISTS `bdd-green`;
USE `bdd-green`;


SET FOREIGN_KEY_CHECKS=0;
DROP TABLE if exists users;
DROP TABLE if exists admins;
DROP TABLE if exists quizz;
DROP TABLE if exists question;
DROP TABLE if exists category;
SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE `users` (
  `id_user`   INT AUTO_INCREMENT PRIMARY KEY,
  `name`      VARCHAR(100)    NOT NULL,
  `username`  VARCHAR(50)     NOT NULL UNIQUE,
  `email`     VARCHAR(100)    NOT NULL UNIQUE,
  `password`  VARCHAR(255)    NOT NULL,
  `score`     INT             NOT NULL DEFAULT 0
);

CREATE TABLE `admins` (
  `id_user` INT PRIMARY KEY,
  FOREIGN KEY (`id_user`) REFERENCES `users`(`id_user`) ON DELETE CASCADE
);

CREATE TABLE `quizz` (
  `id_quizz` INT AUTO_INCREMENT PRIMARY KEY,
  `name`     VARCHAR(100)    NOT NULL,
  `category` ENUM('IT For Green','GreenIT') NOT NULL
);

CREATE TABLE `question` (
  `id_question` INT AUTO_INCREMENT PRIMARY KEY,
  `quizz_id`    INT           NOT NULL,
  `question`    TEXT          NOT NULL,
  `answer1`     VARCHAR(255)  NOT NULL,
  `answer2`     VARCHAR(255)  NOT NULL,
  FOREIGN KEY (`quizz_id`) REFERENCES `quizz`(`id_quizz`) ON DELETE CASCADE
);


