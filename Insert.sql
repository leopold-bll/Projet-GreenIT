-- Utilisateurs
INSERT INTO `user` (`name`,`username`,`email`,`password`,`score`)
VALUES
  ('Alice Dupont',  'alice',  'alice@example.com',  SHA2('passAlice',256),  0),
  ('Bob Martin',    'bmartin','bob@example.com',    SHA2('passBob',256),    0),
  ('Charlie Admin', 'charlie','admin@example.com',  SHA2('passAdmin',256),  0);

-- On fait de Charlie un administrateur
INSERT INTO `admin` (`id_user`)
VALUES
  (3);

-- Quiz
INSERT INTO `quizz` (`name`)
VALUES
  ('Quiz Mathématiques'),
  ('Quiz Histoire');

-- Questions pour "Quiz Mathématiques" (id_quizz = 1)
INSERT INTO `question` (`quizz_id`,`question`,`answer1`,`answer2`)
VALUES
  (1, 'Combien font 2 + 2 ?',      '3',  '4'),
  (1, 'Racine carrée de 9 ?',       '2',  '3');

-- Questions pour "Quiz Histoire" (id_quizz = 2)
INSERT INTO `question` (`quizz_id`,`question`,`answer1`,`answer2`)
VALUES
  (2, 'Qui a découvert l\'Amérique en 1492 ?', 'Christophe Colomb', 'Vasco de Gama'),
  (2, 'En quelle année a commencé la Révolution française ?', '1789', '1792');