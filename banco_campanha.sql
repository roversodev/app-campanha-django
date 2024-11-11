-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (arm64)
--
-- Host: localhost    Database: banco_campanha
-- ------------------------------------------------------
-- Server version	8.0.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appCampanha_assunto`
--

DROP TABLE IF EXISTS `appCampanha_assunto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_assunto` (
  `id_assunto` int NOT NULL AUTO_INCREMENT,
  `assuntoT` longtext NOT NULL,
  `data_criacao` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `solucionado` varchar(24) DEFAULT NULL,
  `motivo_finalizacao` longtext,
  `data_finalizacao` datetime(6) DEFAULT NULL,
  `atendente_id` bigint DEFAULT NULL,
  `finalizado_por_id` bigint DEFAULT NULL,
  `area_de_atuacao_id` bigint DEFAULT NULL,
  `clienteEscolhido_id` int NOT NULL,
  PRIMARY KEY (`id_assunto`),
  KEY `appCampanha_assunto_atendente_id_d6a24a8f_fk_appCampan` (`atendente_id`),
  KEY `appCampanha_assunto_finalizado_por_id_af83feda_fk_appCampan` (`finalizado_por_id`),
  KEY `appCampanha_assunto_area_de_atuacao_id_7e8eafd2_fk_appCampan` (`area_de_atuacao_id`),
  KEY `appCampanha_assunto_clienteEscolhido_id_83922dc2_fk_appCampan` (`clienteEscolhido_id`),
  CONSTRAINT `appCampanha_assunto_area_de_atuacao_id_7e8eafd2_fk_appCampan` FOREIGN KEY (`area_de_atuacao_id`) REFERENCES `appCampanha_atuacao` (`id`),
  CONSTRAINT `appCampanha_assunto_atendente_id_d6a24a8f_fk_appCampan` FOREIGN KEY (`atendente_id`) REFERENCES `appCampanha_customuser` (`id`),
  CONSTRAINT `appCampanha_assunto_clienteEscolhido_id_83922dc2_fk_appCampan` FOREIGN KEY (`clienteEscolhido_id`) REFERENCES `appCampanha_eleitor` (`id_usuario`),
  CONSTRAINT `appCampanha_assunto_finalizado_por_id_af83feda_fk_appCampan` FOREIGN KEY (`finalizado_por_id`) REFERENCES `appCampanha_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_assunto`
--

LOCK TABLES `appCampanha_assunto` WRITE;
/*!40000 ALTER TABLE `appCampanha_assunto` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_assunto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_atuacao`
--

DROP TABLE IF EXISTS `appCampanha_atuacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_atuacao` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_atuacao`
--

LOCK TABLES `appCampanha_atuacao` WRITE;
/*!40000 ALTER TABLE `appCampanha_atuacao` DISABLE KEYS */;
INSERT INTO `appCampanha_atuacao` VALUES (1,'INSS'),(2,'Jurídico');
/*!40000 ALTER TABLE `appCampanha_atuacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_customuser`
--

DROP TABLE IF EXISTS `appCampanha_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `is_first_login` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_customuser`
--

LOCK TABLES `appCampanha_customuser` WRITE;
/*!40000 ALTER TABLE `appCampanha_customuser` DISABLE KEYS */;
INSERT INTO `appCampanha_customuser` VALUES (1,'pbkdf2_sha256$870000$mHeUQVexKJxQ4N8eStEd6p$4V5dg2ctqHgmDF4FR76qXSjMe1y2AdneIFjX+76lFbQ=','2024-11-01 14:11:34.000000',1,'admin','admin','admin','admin@soufariadesa.com.br',1,1,'2024-11-01 14:10:46.000000','',0),(2,'pbkdf2_sha256$870000$SZUas1UfteuZE6MVYCGNMu$ZZTGI7MUjYjqGE7+XkSCuUfSqSOlRVAHkbpVDIVnyb0=',NULL,1,'Vitor','Vitor','Roverso','vitorroverso@hotmail.com',1,1,'2024-11-01 14:11:20.000000','',1);
/*!40000 ALTER TABLE `appCampanha_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_customuser_atuacoes`
--

DROP TABLE IF EXISTS `appCampanha_customuser_atuacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_customuser_atuacoes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `atuacao_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `appCampanha_customuser_a_customuser_id_atuacao_id_84397620_uniq` (`customuser_id`,`atuacao_id`),
  KEY `appCampanha_customus_atuacao_id_4a06443f_fk_appCampan` (`atuacao_id`),
  CONSTRAINT `appCampanha_customus_atuacao_id_4a06443f_fk_appCampan` FOREIGN KEY (`atuacao_id`) REFERENCES `appCampanha_atuacao` (`id`),
  CONSTRAINT `appCampanha_customus_customuser_id_a38b360f_fk_appCampan` FOREIGN KEY (`customuser_id`) REFERENCES `appCampanha_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_customuser_atuacoes`
--

LOCK TABLES `appCampanha_customuser_atuacoes` WRITE;
/*!40000 ALTER TABLE `appCampanha_customuser_atuacoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_customuser_atuacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_customuser_groups`
--

DROP TABLE IF EXISTS `appCampanha_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `appCampanha_customuser_g_customuser_id_group_id_cadbe4c0_uniq` (`customuser_id`,`group_id`),
  KEY `appCampanha_customuser_groups_group_id_536c6d9c_fk_auth_group_id` (`group_id`),
  CONSTRAINT `appCampanha_customus_customuser_id_059510b4_fk_appCampan` FOREIGN KEY (`customuser_id`) REFERENCES `appCampanha_customuser` (`id`),
  CONSTRAINT `appCampanha_customuser_groups_group_id_536c6d9c_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_customuser_groups`
--

LOCK TABLES `appCampanha_customuser_groups` WRITE;
/*!40000 ALTER TABLE `appCampanha_customuser_groups` DISABLE KEYS */;
INSERT INTO `appCampanha_customuser_groups` VALUES (1,2,1);
/*!40000 ALTER TABLE `appCampanha_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_customuser_user_permissions`
--

DROP TABLE IF EXISTS `appCampanha_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `appCampanha_customuser_u_customuser_id_permission_a70ff531_uniq` (`customuser_id`,`permission_id`),
  KEY `appCampanha_customus_permission_id_34ce7cee_fk_auth_perm` (`permission_id`),
  CONSTRAINT `appCampanha_customus_customuser_id_bf64d872_fk_appCampan` FOREIGN KEY (`customuser_id`) REFERENCES `appCampanha_customuser` (`id`),
  CONSTRAINT `appCampanha_customus_permission_id_34ce7cee_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_customuser_user_permissions`
--

LOCK TABLES `appCampanha_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `appCampanha_customuser_user_permissions` DISABLE KEYS */;
INSERT INTO `appCampanha_customuser_user_permissions` VALUES (2,2,57),(3,2,58),(4,2,59),(5,2,60),(6,2,61),(7,2,62),(8,2,63),(1,2,64);
/*!40000 ALTER TABLE `appCampanha_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_dataretorno`
--

DROP TABLE IF EXISTS `appCampanha_dataretorno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_dataretorno` (
  `id_dataretorno` int NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `hora` time(6) NOT NULL,
  `notificacao_enviada_dia` tinyint(1) NOT NULL,
  `notificacao_enviada_30min` tinyint(1) NOT NULL,
  `atendente_id` bigint DEFAULT NULL,
  `cliente_id` int NOT NULL,
  PRIMARY KEY (`id_dataretorno`),
  KEY `appCampanha_datareto_atendente_id_cd7029b4_fk_appCampan` (`atendente_id`),
  KEY `appCampanha_datareto_cliente_id_bec931d5_fk_appCampan` (`cliente_id`),
  CONSTRAINT `appCampanha_datareto_atendente_id_cd7029b4_fk_appCampan` FOREIGN KEY (`atendente_id`) REFERENCES `appCampanha_customuser` (`id`),
  CONSTRAINT `appCampanha_datareto_cliente_id_bec931d5_fk_appCampan` FOREIGN KEY (`cliente_id`) REFERENCES `appCampanha_eleitor` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_dataretorno`
--

LOCK TABLES `appCampanha_dataretorno` WRITE;
/*!40000 ALTER TABLE `appCampanha_dataretorno` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_dataretorno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_eleitor`
--

DROP TABLE IF EXISTS `appCampanha_eleitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_eleitor` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nome` longtext NOT NULL,
  `nomeS` longtext,
  `telefone` longtext,
  `cpf` longtext NOT NULL,
  `dataN` date NOT NULL,
  `genero` longtext,
  `data_criacao` datetime(6) NOT NULL,
  `atendente_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `appCampanha_eleitor_atendente_id_d2d3c737_fk_appCampan` (`atendente_id`),
  CONSTRAINT `appCampanha_eleitor_atendente_id_d2d3c737_fk_appCampan` FOREIGN KEY (`atendente_id`) REFERENCES `appCampanha_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_eleitor`
--

LOCK TABLES `appCampanha_eleitor` WRITE;
/*!40000 ALTER TABLE `appCampanha_eleitor` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_eleitor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_endereco`
--

DROP TABLE IF EXISTS `appCampanha_endereco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_endereco` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cep` longtext NOT NULL,
  `endereco` longtext NOT NULL,
  `numero` int DEFAULT NULL,
  `complemento` longtext,
  `bairro` longtext NOT NULL,
  `estado` longtext NOT NULL,
  `municipio` longtext NOT NULL,
  `tipo_endereco` varchar(20) NOT NULL,
  `principal` tinyint(1) NOT NULL,
  `eleitor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `appCampanha_endereco_eleitor_id_df6dac80_fk_appCampan` (`eleitor_id`),
  CONSTRAINT `appCampanha_endereco_eleitor_id_df6dac80_fk_appCampan` FOREIGN KEY (`eleitor_id`) REFERENCES `appCampanha_eleitor` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_endereco`
--

LOCK TABLES `appCampanha_endereco` WRITE;
/*!40000 ALTER TABLE `appCampanha_endereco` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_endereco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_observacao`
--

DROP TABLE IF EXISTS `appCampanha_observacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_observacao` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `descricao` longtext NOT NULL,
  `data_criacao` datetime(6) NOT NULL,
  `assunto_id` int NOT NULL,
  `atendente_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `appCampanha_observac_assunto_id_1ffd3760_fk_appCampan` (`assunto_id`),
  KEY `appCampanha_observac_atendente_id_bfc76ba2_fk_appCampan` (`atendente_id`),
  CONSTRAINT `appCampanha_observac_assunto_id_1ffd3760_fk_appCampan` FOREIGN KEY (`assunto_id`) REFERENCES `appCampanha_assunto` (`id_assunto`),
  CONSTRAINT `appCampanha_observac_atendente_id_bfc76ba2_fk_appCampan` FOREIGN KEY (`atendente_id`) REFERENCES `appCampanha_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_observacao`
--

LOCK TABLES `appCampanha_observacao` WRITE;
/*!40000 ALTER TABLE `appCampanha_observacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_observacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appCampanha_senha`
--

DROP TABLE IF EXISTS `appCampanha_senha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appCampanha_senha` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero` int NOT NULL,
  `data_criacao` datetime(6) NOT NULL,
  `atendida` tinyint(1) NOT NULL,
  `chamada` datetime(6) DEFAULT NULL,
  `atendente_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`),
  KEY `appCampanha_senha_atendente_id_67d7dbec_fk_appCampan` (`atendente_id`),
  CONSTRAINT `appCampanha_senha_atendente_id_67d7dbec_fk_appCampan` FOREIGN KEY (`atendente_id`) REFERENCES `appCampanha_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appCampanha_senha`
--

LOCK TABLES `appCampanha_senha` WRITE;
/*!40000 ALTER TABLE `appCampanha_senha` DISABLE KEYS */;
/*!40000 ALTER TABLE `appCampanha_senha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'staff');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add atuacao',6,'add_atuacao'),(22,'Can change atuacao',6,'change_atuacao'),(23,'Can delete atuacao',6,'delete_atuacao'),(24,'Can view atuacao',6,'view_atuacao'),(25,'Can add user',7,'add_customuser'),(26,'Can change user',7,'change_customuser'),(27,'Can delete user',7,'delete_customuser'),(28,'Can view user',7,'view_customuser'),(29,'Can add eleitor',8,'add_eleitor'),(30,'Can change eleitor',8,'change_eleitor'),(31,'Can delete eleitor',8,'delete_eleitor'),(32,'Can view eleitor',8,'view_eleitor'),(33,'Can add dataretorno',9,'add_dataretorno'),(34,'Can change dataretorno',9,'change_dataretorno'),(35,'Can delete dataretorno',9,'delete_dataretorno'),(36,'Can view dataretorno',9,'view_dataretorno'),(37,'Can add assunto',10,'add_assunto'),(38,'Can change assunto',10,'change_assunto'),(39,'Can delete assunto',10,'delete_assunto'),(40,'Can view assunto',10,'view_assunto'),(41,'Can add endereco',11,'add_endereco'),(42,'Can change endereco',11,'change_endereco'),(43,'Can delete endereco',11,'delete_endereco'),(44,'Can view endereco',11,'view_endereco'),(45,'Can add observacao',12,'add_observacao'),(46,'Can change observacao',12,'change_observacao'),(47,'Can delete observacao',12,'delete_observacao'),(48,'Can view observacao',12,'view_observacao'),(49,'Can add senha',13,'add_senha'),(50,'Can change senha',13,'change_senha'),(51,'Can delete senha',13,'delete_senha'),(52,'Can view senha',13,'view_senha'),(53,'Can add Notification',14,'add_notification'),(54,'Can change Notification',14,'change_notification'),(55,'Can delete Notification',14,'delete_notification'),(56,'Can view Notification',14,'view_notification'),(57,'Usuarios',7,'usuarios'),(58,'Assunto Lista',7,'assunto_lista'),(59,'Staff',7,'staff'),(60,'Cadastrar',7,'cadastrar'),(61,'Assunto',7,'assunto'),(62,'Solucao',7,'solucao'),(63,'Calendario',7,'calendario'),(64,'Home',7,'home');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_appCampanha_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_appCampanha_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `appCampanha_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-11-01 14:11:44.589138','2','Vitor',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]',7,1),(2,'2024-11-01 14:11:53.200616','1','admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',7,1),(3,'2024-11-01 14:11:59.296871','1','INSS',1,'[{\"added\": {}}]',6,1),(4,'2024-11-01 14:13:33.996252','2','Jurídico',1,'[{\"added\": {}}]',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(10,'appCampanha','assunto'),(6,'appCampanha','atuacao'),(7,'appCampanha','customuser'),(9,'appCampanha','dataretorno'),(8,'appCampanha','eleitor'),(11,'appCampanha','endereco'),(12,'appCampanha','observacao'),(13,'appCampanha','senha'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(14,'notifications','notification'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-11-01 14:10:13.429570'),(2,'contenttypes','0002_remove_content_type_name','2024-11-01 14:10:13.442261'),(3,'auth','0001_initial','2024-11-01 14:10:13.492399'),(4,'auth','0002_alter_permission_name_max_length','2024-11-01 14:10:13.505510'),(5,'auth','0003_alter_user_email_max_length','2024-11-01 14:10:13.508229'),(6,'auth','0004_alter_user_username_opts','2024-11-01 14:10:13.510352'),(7,'auth','0005_alter_user_last_login_null','2024-11-01 14:10:13.513411'),(8,'auth','0006_require_contenttypes_0002','2024-11-01 14:10:13.514048'),(9,'auth','0007_alter_validators_add_error_messages','2024-11-01 14:10:13.516255'),(10,'auth','0008_alter_user_username_max_length','2024-11-01 14:10:13.518569'),(11,'auth','0009_alter_user_last_name_max_length','2024-11-01 14:10:13.520816'),(12,'auth','0010_alter_group_name_max_length','2024-11-01 14:10:13.525688'),(13,'auth','0011_update_proxy_permissions','2024-11-01 14:10:13.529525'),(14,'auth','0012_alter_user_first_name_max_length','2024-11-01 14:10:13.531774'),(15,'appCampanha','0001_initial','2024-11-01 14:10:13.777358'),(16,'admin','0001_initial','2024-11-01 14:10:13.813245'),(17,'admin','0002_logentry_remove_auto_add','2024-11-01 14:10:13.819170'),(18,'admin','0003_logentry_add_action_flag_choices','2024-11-01 14:10:13.825241'),(19,'notifications','0001_initial','2024-11-01 14:10:13.946723'),(20,'sessions','0001_initial','2024-11-01 14:10:13.955023');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `level` varchar(20) NOT NULL,
  `unread` tinyint(1) NOT NULL,
  `actor_object_id` varchar(255) NOT NULL,
  `verb` varchar(255) NOT NULL,
  `description` longtext,
  `target_object_id` varchar(255) DEFAULT NULL,
  `action_object_object_id` varchar(255) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `public` tinyint(1) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `emailed` tinyint(1) NOT NULL,
  `data` longtext,
  `action_object_content_type_id` int DEFAULT NULL,
  `actor_content_type_id` int NOT NULL,
  `recipient_id` bigint NOT NULL,
  `target_content_type_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_notifi_action_object_conten_7d2b8ee9_fk_django_co` (`action_object_content_type_id`),
  KEY `notifications_notifi_actor_content_type_i_0c69d7b7_fk_django_co` (`actor_content_type_id`),
  KEY `notifications_notifi_target_content_type__ccb24d88_fk_django_co` (`target_content_type_id`),
  KEY `notifications_notification_unread_cce4be30` (`unread`),
  KEY `notifications_notification_timestamp_6a797bad` (`timestamp`),
  KEY `notifications_notification_public_1bc30b1c` (`public`),
  KEY `notifications_notification_deleted_b32b69e6` (`deleted`),
  KEY `notifications_notification_emailed_23a5ad81` (`emailed`),
  KEY `notificatio_recipie_8bedf2_idx` (`recipient_id`,`unread`),
  CONSTRAINT `notifications_notifi_action_object_conten_7d2b8ee9_fk_django_co` FOREIGN KEY (`action_object_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notifications_notifi_actor_content_type_i_0c69d7b7_fk_django_co` FOREIGN KEY (`actor_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notifications_notifi_recipient_id_d055f3f0_fk_appCampan` FOREIGN KEY (`recipient_id`) REFERENCES `appCampanha_customuser` (`id`),
  CONSTRAINT `notifications_notifi_target_content_type__ccb24d88_fk_django_co` FOREIGN KEY (`target_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
INSERT INTO `notifications_notification` VALUES (1,'info',1,'1','Bem-vindo ao nosso Sistema!',NULL,NULL,NULL,'2024-11-01 14:11:01.907043',1,0,0,NULL,NULL,7,1,NULL),(2,'info',1,'1','Para marcar como lida basta clicar em cima da notificação!',NULL,NULL,NULL,'2024-11-01 14:11:01.909020',1,0,0,NULL,NULL,7,1,NULL);
/*!40000 ALTER TABLE `notifications_notification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-01 11:14:14
