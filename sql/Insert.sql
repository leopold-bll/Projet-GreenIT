USE `bdd-green`;

DELETE FROM users;
DELETE FROM admins;
DELETE FROM quizz;
DELETE FROM question;


-- Utilisateurs
INSERT INTO `users` (id_user, `name`,`username`,`email`,`password`,`score`) VALUES
  (1, 'Alice Dupont',  'alice',  'alice@example.com',  SHA2('passAlice',256),  0),
  (2, 'Bob Martin',    'bmartin','bob@example.com',    SHA2('passBob',256),    0),
  (3, 'Charlie Admin', 'charlie','admin@example.com',  SHA2('passAdmin',256),  0);


-- Charlie devient admin
INSERT INTO `admins` (`id_user`) VALUES (3);

-- Quiz IT For Green
INSERT INTO `quizz` (id_quizz, `name`,`category`) VALUES
  (1, 'Eco-réseaux et protocoles','IT For Green'),
  (2, 'Matériel basse consommation','IT For Green'),
  (3, 'Data centers verts','GreenIT'),
  (4, 'Recyclage de serveurs','GreenIT');

-- Questions pour le premier quiz (id_quizz = 1)
INSERT INTO `question` (`quizz_id`,`question`,`answer1`,`answer2`, correct_answer_is_1) VALUES
  (1, 'Quel protocole HTTP est le plus économe en bande passante ?', 'HTTP/1.0', 'HTTP/2', False),
  (1, 'Quelle technique réduit la consommation CPU ?', 'Mise en cache', 'Compression à la volée', True);

-- Questions pour le quiz « Data centers verts » (id_quizz = 3)
INSERT INTO `question` (`quizz_id`,`question`,`answer1`,`answer2`, correct_answer_is_1) VALUES
  (3, 'Quel pays est pionnier des data centers refroidis par eau de mer ?', 'Suède', 'Canada', True),
  (3, 'Quelle énergie verte alimente ces centres ?', 'Éolien', 'Charbon', True);
  
  
  SELECT * FROM users;
  SELECT * FROM admins;
  SELECT * FROM quizz;
  SELECT * FROM question;

