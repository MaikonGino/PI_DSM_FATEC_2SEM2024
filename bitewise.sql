-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 28/10/2024 às 02:38
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `bitewise`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `contagem_cliques`
--

CREATE TABLE `contagem_cliques` (
  `id_usuario` int(11) NOT NULL,
  `cliques_disponiveis` int(11) DEFAULT 0,
  `data_renovacao` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `contagem_cliques`
--

INSERT INTO `contagem_cliques` (`id_usuario`, `cliques_disponiveis`, `data_renovacao`) VALUES
(1, 15, '2024-10-28 01:33:45'),
(2, 10, '2024-10-28 01:33:45'),
(3, 8, '2024-10-28 01:33:45'),
(4, 12, '2024-10-28 01:33:45'),
(5, 5, '2024-10-28 01:33:45');

-- --------------------------------------------------------

--
-- Estrutura para tabela `historico_consultas`
--

CREATE TABLE `historico_consultas` (
  `id_consulta` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_receita` int(11) DEFAULT NULL,
  `data_consulta` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `historico_consultas`
--

INSERT INTO `historico_consultas` (`id_consulta`, `id_usuario`, `id_receita`, `data_consulta`) VALUES
(1, 1, 1, '2024-10-28 01:33:45'),
(2, 1, 2, '2024-10-28 01:33:45'),
(3, 2, 3, '2024-10-28 01:33:45'),
(4, 2, 1, '2024-10-28 01:33:45'),
(5, 3, 2, '2024-10-28 01:33:45'),
(6, 4, 4, '2024-10-28 01:33:45'),
(7, 5, 5, '2024-10-28 01:33:45');

-- --------------------------------------------------------

--
-- Estrutura para tabela `ingredientes`
--

CREATE TABLE `ingredientes` (
  `id_ingrediente` int(11) NOT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `unidade_medida` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `ingredientes`
--

INSERT INTO `ingredientes` (`id_ingrediente`, `nome`, `unidade_medida`) VALUES
(1, 'Farinha de trigo', 'gramas'),
(2, 'Ovos', 'unidades'),
(3, 'Leite', 'ml'),
(4, 'Açúcar', 'gramas'),
(5, 'Manteiga', 'gramas'),
(6, 'Sal', 'gramas'),
(7, 'Azeite', 'ml'),
(8, 'Cenoura', 'gramas'),
(9, 'Chocolate', 'gramas'),
(10, 'Abóbora', 'gramas');

-- --------------------------------------------------------

--
-- Estrutura para tabela `pagamentos`
--

CREATE TABLE `pagamentos` (
  `id_pagamento` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `valor` decimal(10,2) DEFAULT NULL,
  `data_pagamento` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `pagamentos`
--

INSERT INTO `pagamentos` (`id_pagamento`, `id_usuario`, `valor`, `data_pagamento`) VALUES
(1, 1, 29.99, '2024-10-28 01:33:45'),
(2, 2, 19.99, '2024-10-28 01:33:45'),
(3, 3, 49.99, '2024-10-28 01:33:45'),
(4, 4, 29.99, '2024-10-28 01:33:45'),
(5, 5, 39.99, '2024-10-28 01:33:45');

-- --------------------------------------------------------

--
-- Estrutura para tabela `passos_preparo`
--

CREATE TABLE `passos_preparo` (
  `id_passo` int(11) NOT NULL,
  `id_receita` int(11) DEFAULT NULL,
  `numero_passo` int(11) DEFAULT NULL,
  `descricao` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `passos_preparo`
--

INSERT INTO `passos_preparo` (`id_passo`, `id_receita`, `numero_passo`, `descricao`) VALUES
(1, 1, 1, 'Misture a farinha, o açúcar e o chocolate em pó.'),
(2, 1, 2, 'Adicione os ovos e o leite, e misture bem.'),
(3, 1, 3, 'Leve ao forno a 180 graus por 40 minutos.'),
(4, 2, 1, 'Lave as folhas de alface.'),
(5, 2, 2, 'Prepare o molho com azeite, alho e anchovas amassadas.'),
(6, 2, 3, 'Misture o molho e sirva.'),
(7, 3, 1, 'Bata a manteiga e o açúcar até formar um creme.'),
(8, 3, 2, 'Adicione o suco de limão e misture bem.');

-- --------------------------------------------------------

--
-- Estrutura para tabela `receitas`
--

CREATE TABLE `receitas` (
  `id_receita` int(11) NOT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `descricao` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `receitas`
--

INSERT INTO `receitas` (`id_receita`, `nome`, `descricao`) VALUES
(1, 'Bolo de Chocolate', 'Delicioso bolo de chocolate com cobertura cremosa.'),
(2, 'Salada Caesar', 'Salada Caesar tradicional com alface e molho especial.'),
(3, 'Torta de Limão', 'Torta com base crocante e creme de limão.'),
(4, 'Macarrão Carbonara', 'Macarrão ao molho cremoso de queijo e bacon.'),
(5, 'Sopa de Abóbora', 'Sopa cremosa de abóbora com um toque de gengibre.');

-- --------------------------------------------------------

--
-- Estrutura para tabela `receita_ingrediente`
--

CREATE TABLE `receita_ingrediente` (
  `id_receita` int(11) NOT NULL,
  `id_ingrediente` int(11) NOT NULL,
  `quantidade` decimal(5,2) DEFAULT NULL,
  `unidade_medida` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `receita_ingrediente`
--

INSERT INTO `receita_ingrediente` (`id_receita`, `id_ingrediente`, `quantidade`, `unidade_medida`) VALUES
(1, 1, 200.00, 'gramas'),
(1, 2, 3.00, 'unidades'),
(1, 3, 250.00, 'ml'),
(1, 4, 150.00, 'gramas'),
(2, 5, 50.00, 'gramas'),
(2, 7, 20.00, 'ml'),
(3, 8, 100.00, 'gramas'),
(4, 10, 200.00, 'gramas');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `celular` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nome`, `email`, `celular`) VALUES
(1, 'João Silva', 'joao.silva@email.com', '11987654321'),
(2, 'Maria Oliveira', 'maria.oliveira@email.com', '11981234567'),
(3, 'Pedro Costa', 'pedro.costa@email.com', '21987654321'),
(4, 'Ana Souza', 'ana.souza@email.com', '21981234567'),
(5, 'Lucas Mendes', 'lucas.mendes@email.com', '31987654321');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `contagem_cliques`
--
ALTER TABLE `contagem_cliques`
  ADD PRIMARY KEY (`id_usuario`);

--
-- Índices de tabela `historico_consultas`
--
ALTER TABLE `historico_consultas`
  ADD PRIMARY KEY (`id_consulta`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_receita` (`id_receita`);

--
-- Índices de tabela `ingredientes`
--
ALTER TABLE `ingredientes`
  ADD PRIMARY KEY (`id_ingrediente`);

--
-- Índices de tabela `pagamentos`
--
ALTER TABLE `pagamentos`
  ADD PRIMARY KEY (`id_pagamento`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Índices de tabela `passos_preparo`
--
ALTER TABLE `passos_preparo`
  ADD PRIMARY KEY (`id_passo`),
  ADD KEY `id_receita` (`id_receita`);

--
-- Índices de tabela `receitas`
--
ALTER TABLE `receitas`
  ADD PRIMARY KEY (`id_receita`);

--
-- Índices de tabela `receita_ingrediente`
--
ALTER TABLE `receita_ingrediente`
  ADD PRIMARY KEY (`id_receita`,`id_ingrediente`),
  ADD KEY `id_ingrediente` (`id_ingrediente`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `historico_consultas`
--
ALTER TABLE `historico_consultas`
  MODIFY `id_consulta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `ingredientes`
--
ALTER TABLE `ingredientes`
  MODIFY `id_ingrediente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de tabela `pagamentos`
--
ALTER TABLE `pagamentos`
  MODIFY `id_pagamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `passos_preparo`
--
ALTER TABLE `passos_preparo`
  MODIFY `id_passo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `receitas`
--
ALTER TABLE `receitas`
  MODIFY `id_receita` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `contagem_cliques`
--
ALTER TABLE `contagem_cliques`
  ADD CONSTRAINT `contagem_cliques_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Restrições para tabelas `historico_consultas`
--
ALTER TABLE `historico_consultas`
  ADD CONSTRAINT `historico_consultas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `historico_consultas_ibfk_2` FOREIGN KEY (`id_receita`) REFERENCES `receitas` (`id_receita`) ON DELETE CASCADE;

--
-- Restrições para tabelas `pagamentos`
--
ALTER TABLE `pagamentos`
  ADD CONSTRAINT `pagamentos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Restrições para tabelas `passos_preparo`
--
ALTER TABLE `passos_preparo`
  ADD CONSTRAINT `passos_preparo_ibfk_1` FOREIGN KEY (`id_receita`) REFERENCES `receitas` (`id_receita`) ON DELETE CASCADE;

--
-- Restrições para tabelas `receita_ingrediente`
--
ALTER TABLE `receita_ingrediente`
  ADD CONSTRAINT `receita_ingrediente_ibfk_1` FOREIGN KEY (`id_receita`) REFERENCES `receitas` (`id_receita`) ON DELETE CASCADE,
  ADD CONSTRAINT `receita_ingrediente_ibfk_2` FOREIGN KEY (`id_ingrediente`) REFERENCES `ingredientes` (`id_ingrediente`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
