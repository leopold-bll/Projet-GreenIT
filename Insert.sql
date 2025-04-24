-- Utilisateurs
INSERT INTO `user` (`name`,`username`,`email`,`password`,`score`) VALUES
  ('Alice Dupont',  'alice',  'alice@example.com',  SHA2('passAlice',256),  0),
  ('Bob Martin',    'bmartin','bob@example.com',    SHA2('passBob',256),    0),
  ('Charlie Admin', 'charlie','admin@example.com',  SHA2('passAdmin',256),  0);

-- Charlie devient admin
INSERT INTO `admin` (`id_user`) VALUES (3);

-- Quiz IT For Green
INSERT INTO `quizz` (`name`,`category`) VALUES
  ('Eco-réseaux et protocoles','IT For Green'),
  ('Matériel basse consommation','IT For Green');

-- Quiz GreenIT
INSERT INTO `quizz` (`name`,`category`) VALUES
  ('Data centers verts','GreenIT'),
  ('Recyclage de serveurs','GreenIT');

-- Questions pour le premier quiz (id_quizz = 1)
INSERT INTO `question` (`quizz_id`,`question`,`answer1`,`answer2`) VALUES
  (1, 'Quel protocole HTTP est le plus économe en bande passante ?', 'HTTP/1.0', 'HTTP/2'),
  (1, 'Quelle technique réduit la consommation CPU ?', 'Mise en cache', 'Compression à la volée');

-- Questions pour le quiz « Data centers verts » (id_quizz = 3)
INSERT INTO `question` (`quizz_id`,`question`,`answer1`,`answer2`) VALUES
  (3, 'Quel pays est pionnier des data centers refroidis par eau de mer ?', 'Suède', 'Canada'),
  (3, 'Quelle énergie verte alimente ces centres ?', 'Éolien', 'Charbon');

