-- phpMyAdmin SQL Dump
-- version 5.2.3-2.fc44
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 28/07/2026 às 18:14
-- Versão do servidor: 11.8.8-MariaDB
-- Versão do PHP: 8.5.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `cadastro`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `estudantes_manha`
--

CREATE TABLE `estudantes_manha` (
  `COL 1` varchar(40) DEFAULT NULL,
  `COL 2` varchar(30) DEFAULT NULL,
  `COL 3` varchar(8) DEFAULT NULL,
  `COL 4` varchar(5) DEFAULT NULL,
  `COL 5` varchar(30) DEFAULT NULL,
  `COL 6` varchar(18) DEFAULT NULL,
  `COL 7` varchar(16) DEFAULT NULL,
  `COL 8` varchar(29) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Despejando dados para a tabela `estudantes_manha`
--

INSERT INTO `estudantes_manha` (`COL 1`, `COL 2`, `COL 3`, `COL 4`, `COL 5`, `COL 6`, `COL 7`, `COL 8`) VALUES
('Nome', 'Curso', 'Seriacao', 'Turma', 'Deficiencia', 'Especificação ', 'Situação ', ''),
('ALICIA LINO COSTA', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'C', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('ALYCIA SILVA MARCELINO', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'D', 'Distúrbios de aprendizagem', 'TDAH', 'S/L', ''),
('ANA FLAVIA MOURA CADENA DOS SANTOS', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'D', 'Distúrbios de aprendizagem', 'TDAH', 'S/L', ''),
('BRAYAN DOS SANTOS INACIO', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'A', 'Deficiência intelectual', 'SÍNDROME DE DOWN', 'SRM', ''),
('ENZO RAFAEL PEITER', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'C', 'Deficiência física', 'PC', 'SRM', ''),
('GABRYELLE ZYLA SOUZA', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'C', 'Distúrbios de aprendizagem', 'TDAH  /TOD', 'SRM', ''),
('HENRIQUE FERNANDES CAMPOS', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'A', 'Distúrbios de aprendizagem', 'S/L', 'S/L', ''),
('ISAAC RODRIGUES DA ROSA', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'C', 'Distúrbios de aprendizagem', 'TDA', 'SRM', ''),
('LUCAS GABRIEL DA SILVA LUIZ', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'A', 'Distúrbios de aprendizagem', 'TDAH/DISLEXIA', 'SRM', ''),
('LUIZA AVANCINI', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'B', 'Distúrbios de aprendizagem', 'S/L', 'S/L', ''),
('NICOLAS NATHAN RIBEIRO GOMES', 'ENSINO MEDIO IFA MAT/CNT', '1ª série', 'D', 'Distúrbios de aprendizagem', 'S/L', 'S/L', ''),
('PEDRO GUILHERME BONHOTI DOS SANTOS', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'B', 'Distúrbios de aprendizagem', 'TDA', 'SRM', ''),
('RENATO MARQUES ORTIZ', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'B', 'Baixa visão', 'BAIXA VISÃO', 'SEM CONTATO', ''),
('TÉO RAMOS', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'B', 'Distúrbios de aprendizagem', 'S/L', 'S/L', ''),
('WELLINGTON GUSTAVO COSTA DOS SANTOS LIMA', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'S/L', ''),
('LARISSA BATISTA DA SILVA', 'ENSINO MEDIO IFA LGG/CHS', '1ª série', 'A', 'Distúrbios de aprendizagem', 'TOD ', 'S/L', ''),
('ANDREW DOS ANJOS BUENO', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'A', 'Transtorno do Espectro Autista', 'TEA', 'ATA DESLIGAMENTO', ''),
('DAVI NERES ENGELMANN', 'ENSINO MEDIO IFA MAT/CNT', '2ª série', 'C', 'Deficiência intelectual', 'SÍNDROME DE NOONAN', 'SRM', ''),
('LAURA DUARTH MARQUES', 'TEC EM ADMINISTRACAO - ET GN', '2ª série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('MATEUS SCHNEIDER DROSDA', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'A', 'Transtorno do Espectro Autista', 'TEA', 'ATA', ''),
('MATHEUS MEMLAK BORGES VIEIRA', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'D', 'Transtornos Mentais/Comp', 'TDA', 'SRM', ''),
('MURILO LEONARDO GONCALVES MARTINS', 'TEC ALIMENTOS FIS-ET PA', '2ª Série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('PEDRO DA COSTA BORGES', 'TEC EM ADMINISTRACAO - ET GN', '2ª série', 'A', 'Transtornos Mentais/Comp', 'ESQUIZOFRENIA', 'ATA DESLIGAMENTO', 'Não frequenta sala de recurso'),
('RAFAELA RAZZOTTO BRUSCHI', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'ATA DESLIGAMENTO', ''),
('VINICIUS CARLOS PEREIRA ROSA', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'A', 'Transtorno do Espectro Autista', 'TEA', 'SRM', ''),
('VINICIUS SANTOS DA MAIA', 'TEC ALIMENTOS FIS-ET PA', '2ª Série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('VITORIA DE MORAIS PEREIRA', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SEM CONTATO', ''),
('LEONARDO ARAUJO NOVAES DE OLIVEIRA', 'ENSINO MEDIO IFA LGG/CHS', '2ª série', 'B', 'Distúrbios de aprendizagem', 'TDAH', 'ATA DESLIGAMENTO', ''),
('LUIZ MARCO ANTONIO DA SILVA PACHECO', 'TEC EM ADMINISTRACAO - ET GN', '2ª série', 'A', 'Distúrbios de aprendizagem', 'TGD', 'SRM', ''),
('GUSTAVO ALVES DE SOUZA', 'TEC ALIMENTOS FIS-ET PA', '2ª série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('ARTHUR VIEIRA SATURNINO DA SILVA', 'ENSINO MEDIO IF MAT/CNT', '3ª Série', 'C', 'Distúrbios de aprendizagem', 'TDAH', 'ATA DESLIGAMENTO', ''),
('CRISLAINE TORRES DE SOUZA', 'NOVO ENSINO MEDIO-PROFISSIONAL', '3ª Série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('DIEGO BROCK DE BRITO', 'NEM EPT IF TEC ADMINISTR-ET GN', '3ª Série', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'ATA DESLIGAMENTO', ''),
('THIAGO CANEDO MENDES', 'ENSINO MEDIO FGB', '3ª Série', 'C', 'Distúrbios de aprendizagem', 'TDAH', 'SRM', ''),
('ANDY MANUEL PEREZ MUCURA', 'ENSINO MEDIO FGB', '2ª série', 'A', 'Transtorno do Espectro Autista', 'TDAH', 'MATRICULAR', '');

-- --------------------------------------------------------

--
-- Estrutura para tabela `estudantes_tarde`
--

CREATE TABLE `estudantes_tarde` (
  `COL 1` varchar(42) DEFAULT NULL,
  `COL 2` varchar(22) DEFAULT NULL,
  `COL 3` varchar(8) DEFAULT NULL,
  `COL 4` varchar(5) DEFAULT NULL,
  `COL 5` varchar(30) DEFAULT NULL,
  `COL 6` varchar(20) DEFAULT NULL,
  `COL 7` varchar(17) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Despejando dados para a tabela `estudantes_tarde`
--

INSERT INTO `estudantes_tarde` (`COL 1`, `COL 2`, `COL 3`, `COL 4`, `COL 5`, `COL 6`, `COL 7`) VALUES
('Nome', 'Curso', 'Seriacao', 'Turma', 'Deficiencia', 'Especificação ', 'Situação '),
('KEMYLI ELOISE FERREIRA DOS SANTOS', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'A', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('DAVI DE ALMEIDA DOS SANTOS', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'A', 'Deficiência intelectual', 'Sem laudo', 'Familia convocada'),
('HELLEN VITORIA GUIERA DOS SANTOS', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'A', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('HELOIZE VITORIA RIBEIRO GOMES', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'B', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('ANA JULIA LHIAR DE MELO NOGUEIRA', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'B', 'Deficiência intelectual', 'Sem laudo', 'SRM JAQUE'),
('LUIZA CRISTINA FABRICIO FURLAN', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'A', 'Atraso Des. Neurospsicomotor', 'Síndrome de Moebius', 'SRM MONICA'),
('LUCAS SCHIMCHECK DO NASCIMENTO', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'C', 'Distúrbios de aprendizagem', 'TDAH', 'SRM JAQUE'),
('ANTHONY PROENÇA DOS SANTOS GONÇALVES', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM JAQUE'),
('MATHEUS GUSTAVO CAVALHEIRO', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'B', 'Distúrbios de aprendizagem', 'TDAH  E  DI', 'SRM JAQUE'),
('LUCAS HENRIQUE DA SILVA FERMIANO', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'B', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('DAVI FELIPE DE SOUZA DE LIMA', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'C', 'Transtorno do Espectro Autista', 'TEA', 'SRM JAQUE'),
('PAMELA DE LIMA MIRANDA', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'A', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('MIGUEL GOMES DA LUZ', 'ENS FUND 6/9 ANO-SERIE', '6º Ano', 'C', 'Distúrbios de aprendizagem', 'Sem laudo', 'Familia convocada'),
('ALICE HELENA BARBOSA MATEUS', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'B', 'Distúrbios de aprendizagem', 'DIXLEXIA DISCALCULIA', 'SRM MONICA'),
('PABLO MIGUEL DOMINGUES MARQUES', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'D', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('PÂMELA ESTER TAVEIRA DE OLIVEIRA', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'C', 'Distúrbios de aprendizagem', 'TDAH', 'SRM MONICA'),
('PIETRO SIMONIAN MENEZES', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'D', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('DAVIH LUCA DE OLIVEIRA', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'C', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('IRENE VITORIA DA MAIA PEREIRA PADILHA', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'B', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('JOAO VICTOR DIAS', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'E', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('DAVI ZILLI KANNINK', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'E', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('THALYSSON KAWAN VIEIRA DA SILVA', 'ENS FUND 6/9 ANO-SERIE', '7º Ano', 'B', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM MONICA'),
('EDUARDO OTAVIO ALVES FRANCA MIRANDA', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'A', 'Deficiência intelectual', 'DOWN', 'SRM MONICA'),
('ARIANE SOFIA FERREIRA', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'B', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('NATAN HENRIQUE FERREIRA SUTIL', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'A', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('AGHATA ALEXANDRA DOMINGUES', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'C', 'Distúrbios de aprendizagem', 'TDAH', 'Desligado (a)'),
('EDUARDO FELIX DRUCIAKI', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'C', 'Deficiência intelectual', 'TDAH', 'SRM MONICA'),
('OCTAVIO VICENTE SANTANA BUSSOLA', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM JAQUE'),
('YASMIN DE OLIVEIRA PONTES', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'A', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('DIOGO ALVES MACHADO', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'C', 'Distúrbios de aprendizagem', 'TEA ', 'SRM MONICA'),
('HELOYSE VICTORIA JUNGLES', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'B', 'Transtorno do Espectro Autista', 'TEA ', 'SRM MONICA'),
('WILLIAN FERREIRA RIOS', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'D', 'Transtornos Mentais/Comp', 'TOD', 'DESLIGADO'),
('GABRIELA VITÓRIA M. DE CARVALHO', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'D', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('NATAN HENRIQUE FERREIRA SUTIL', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'A', 'Distúrbios de aprendizagem', 'Sem laudo', 'SRM JAQUE'),
('OCTAVIO VICENTE SANTANA BUSSOLA', 'ENS FUND 6/9 ANO-SERIE', '8º Ano', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM JAQUE'),
('IGOR ADAMCZWSKI DOS SANTOS', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'Desligado (a)'),
('LIVIA MARIA LIMA DA COSTA', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'A', 'Distúrbios de aprendizagem', 'TDAH', 'SRM MONICA'),
('EMANUELE CASSULA DA SILVA', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'D', 'Distúrbios de aprendizagem', 'TDAH', 'SRM JAQUE'),
('JHONATAN VINICIUS LIRA DA SILVA', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'C', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('JOSÉ ANTONIO ROJAS VALENÇA', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'B', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('LOUISE SILVEIRA DO ROSARIO', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'C', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('MARIA EDUARDA MODESTO JOSE', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'C', 'Distúrbios de aprendizagem', 'TEA', 'SRM MONICA'),
('RHYAN CHRYSTIAN HEY', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'D', 'Transtorno do Espectro Autista', 'TEA', 'SRM MONICA'),
('MIGUEL HENRIQUE DE SOUZA DE LIMA', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'B', 'Transtorno do Espectro Autista', 'TEA', 'Investigar'),
('BENJAMIN FORTUNATO BRESSAN AVILLA NOGUEIRA', 'ENS FUND 6/9 ANO-SERIE', '9º Ano', 'B', 'Altas habilidades/Superdotação', 'TDAH', 'SRM MONICA');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
