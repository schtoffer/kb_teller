INSERT INTO business_details (
    business_id,
    street,
    post_code,
    city,
    website_url
    )
VALUES (
    1,
    "Tollbugata 3",
    "0152",
    "Oslo",
    "https://kirkensbymisjon.no/tilbud-motestedet/kontaktinformasjon/#oslo"
);

CREATE TABLE business_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER,
    street TEXT,
    post_code TEXT,
    city TEXT,
    website_url TEXT,
    FOREIGN KEY (business_id) REFERENCES business (id) ON DELETE CASCADE
);

SELECT usr_fname FROM user_details WHERE user_id = 3
SELECT f FROM users WHERE id = ?"

-- Pupulate businesses test data

INSERT INTO businesses (name) VALUES ('Enga');
INSERT INTO businesses (name) VALUES ('Skattkammeret, Sveio');
INSERT INTO businesses (name) VALUES ('Frogner frivillighetssentral');
INSERT INTO businesses (name) VALUES ('Risenga');
INSERT INTO businesses (name) VALUES ('Viste strandhotell');
