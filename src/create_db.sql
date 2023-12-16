CREATE TABLE IF NOT EXISTS companies
(
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    link VARCHAR(250) NOT NULL
);

CREATE TABLE IF NOT EXISTS vacancies
(
    vacancy_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id),
    title_vacancy VARCHAR(150) NOT NULL,
    salary INT,
    link VARCHAR(250) NOT NULL,
    description TEXT
);