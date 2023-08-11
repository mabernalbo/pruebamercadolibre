CREATE TABLE IF NOT EXISTS `meliarchivos`.`archivos` (
`idarchivo` VARCHAR(250) NOT NULL,
`nombrearchivo` VARCHAR(500) NULL,
`extension` VARCHAR(100) NULL,
`duenodelarchivo` VARCHAR(250) NULL,
`visibilidad` VARCHAR(100) NULL,
`enviocorreo` SMALLINT NULL,
`criticidad` VARCHAR(100) NULL,
PRIMARY KEY (`idarchivo`));