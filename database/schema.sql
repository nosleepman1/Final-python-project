
CREATE DATABASE IF NOT EXISTS `gestion_incidents` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `gestion_incidents`;

-- 1. Table : utilisateur
DROP TABLE IF EXISTS `intervention`;
DROP TABLE IF EXISTS `incident`;
DROP TABLE IF EXISTS `utilisateur`;

CREATE TABLE `utilisateur` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `login` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(100) NOT NULL,
    `nom` VARCHAR(50) NOT NULL,
    `prenom` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `role` ENUM('UTILISATEUR', 'TECHNICIEN', 'ADMIN') NOT NULL DEFAULT 'UTILISATEUR',
    `service` VARCHAR(50) DEFAULT NULL,
    `date_creation` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Table : incident
CREATE TABLE `incident` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `titre` VARCHAR(150) NOT NULL,
    `description` TEXT NOT NULL,
    `priorite` ENUM('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE') NOT NULL DEFAULT 'MOYENNE',
    `statut` ENUM('OUVERT', 'EN_COURS', 'RESOLU', 'FERME', 'ANNULE') NOT NULL DEFAULT 'OUVERT',
    `date_creation` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `utilisateur_id` INT NOT NULL,
    CONSTRAINT `fk_incident_utilisateur` 
        FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur`(`id`) 
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 3. Table : intervention
CREATE TABLE `intervention` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `commentaire` TEXT NOT NULL,
    `duree_minutes` INT NOT NULL DEFAULT 0,
    `date_intervention` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `incident_id` INT NOT NULL,
    `technicien_id` INT NOT NULL,
    CONSTRAINT `fk_intervention_incident` 
        FOREIGN KEY (`incident_id`) REFERENCES `incident`(`id`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_intervention_technicien` 
        FOREIGN KEY (`technicien_id`) REFERENCES `utilisateur`(`id`) 
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- SEEDERS : Données de test

INSERT INTO `utilisateur` (`id`, `login`, `password`, `nom`, `prenom`, `email`, `role`, `service`) VALUES
(1, 'admin', 'admin123', 'DIOP', 'Amadou', 'admin@entreprise.sn', 'ADMIN', 'Direction'),
(2, 'tech1', 'tech123', 'NDIAYE', 'Fatou', 'fatou.ndiaye@entreprise.sn', 'TECHNICIEN', 'Support Informatique'),
(3, 'tech2', 'tech123', 'SOW', 'Moussa', 'moussa.sow@entreprise.sn', 'TECHNICIEN', 'Réseaux & Télécoms'),
(4, 'user1', 'user123', 'FALL', 'Awa', 'awa.fall@entreprise.sn', 'UTILISATEUR', 'Comptabilité'),
(5, 'user2', 'user123', 'BA', 'Ibrahima', 'ibrahima.ba@entreprise.sn', 'UTILISATEUR', 'Ressources Humaines');

INSERT INTO `incident` (`id`, `titre`, `description`, `priorite`, `statut`, `date_creation`, `utilisateur_id`) VALUES
(1, 'Imprimante RH hors service', 'L\'imprimante réseau du bureau RH n\'imprime plus les fiches de paie.', 'HAUTE', 'OUVERT', NOW() - INTERVAL 5 HOUR, 5),
(2, 'Écran noir poste comptabilité', 'Le PC de travail ne s\'allume plus après la coupure de courant d\'hier.', 'CRITIQUE', 'EN_COURS', NOW() - INTERVAL 12 HOUR, 4),
(3, 'Lenteur connexion Wi-Fi', 'Connexion très lente au 2ème étage lors des réunions.', 'MOYENNE', 'RESOLU', NOW() - INTERVAL 2 DAY, 5),
(4, 'Demande de souris sans fil', 'Besoin d\'une nouvelle souris ergonomique.', 'BASSE', 'FERME', NOW() - INTERVAL 4 DAY, 4);

INSERT INTO `intervention` (`id`, `commentaire`, `duree_minutes`, `date_intervention`, `incident_id`, `technicien_id`) VALUES
(1, 'Diagnostic en cours : vérification de l\'alimentation et test des barrettes RAM.', 45, NOW() - INTERVAL 6 HOUR, 2, 2),
(2, 'Redémarrage et mise à jour du firmware du point d\'accès Wi-Fi.', 30, NOW() - INTERVAL 1 DAY, 3, 3),
(3, 'Souris livrée et connectée au poste utilisateur.', 15, NOW() - INTERVAL 3 DAY, 4, 2);
