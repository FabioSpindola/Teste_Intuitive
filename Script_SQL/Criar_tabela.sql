CREATE TABLE Relatorio_Cadop (
    Registro_ANS INT PRIMARY KEY,
    CNPJ VARCHAR(14) NOT NULL,
    Razao_Social VARCHAR(255) NOT NULL,
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(10),
    Complemento VARCHAR(255),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(8),
    DDD VARCHAR(3),
    Telefone VARCHAR(15),
    Fax VARCHAR(15),
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(255),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS DATE
);

CREATE TABLE transacoes_financeiras (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    Reg_Ans INT NOT NULL,
    Cd_Conta_Contabil BIGINT NOT NULL,
    Descricao TEXT NOT NULL,
    Vl_Saldo_Inicial DECIMAL(18,2) NOT NULL,
    Vl_Saldo_Final DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (Reg_Ans) REFERENCES Operadoras_Saude(Registro_ANS) ON DELETE CASCADE
);

-- Importando o arquivo Relatorio_cadop.csv para a tabela relatorio_cadop
COPY Relatorio_Cadop
FROM 'C:/Users/fabiospindola/Documents/Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- Importando o arquivo 1T2023.csv para a tabela transacoes_financeiras
COPY transacoes_financeiras
FROM 'C:/Users/fabiospindola/Documents/1T2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

SELECT 
    o.razao_social, 
    SUM(t.vl_saldo_final) AS total_despesas
FROM transacoes_financeiras t
JOIN operadoras_saude o ON t.reg_ans = o.registro_ans
WHERE t.descricao ILIKE '%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MÉDICO HOSPITALAR%'
AND t.data >= (CURRENT_DATE - INTERVAL '3 months')
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;


SELECT 
    o.razao_social, 
    SUM(t.vl_saldo_final) AS total_despesas
FROM transacoes_financeiras t
JOIN operadoras_saude o ON t.reg_ans = o.registro_ans
WHERE t.descricao ILIKE '%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MÉDICO HOSPITALAR%'
AND t.data >= (CURRENT_DATE - INTERVAL '1 year')
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;