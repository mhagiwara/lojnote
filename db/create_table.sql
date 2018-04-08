USE lojnote;

CREATE TABLE `users` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `alias` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `time_created` DATETIME DEFAULT NULL,
    `active` TINYINT(1) NOT NULL,
    `profile` TEXT,
    PRIMARY KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `posts` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT(11) NOT NULL,
    `body` TEXT,
    `time_created` DATETIME DEFAULT NULL,
    `time_updated` DATETIME DEFAULT NULL,
    PRIMARY KEY `id` (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
