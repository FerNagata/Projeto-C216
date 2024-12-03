DROP TABLE IF EXISTS "booking";
DROP TABLE IF EXISTS "accommodation";

CREATE TABLE "accommodation" (
    "id" SERIAL PRIMARY KEY,
    "category" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "address" VARCHAR(255) NOT NULL,
    "price_per_night" FLOAT NOT NULL,
    "owner" VARCHAR(255) NOT NULL
);

CREATE TABLE "booking" (
    "id" SERIAL PRIMARY KEY,
    "accommodation_id" INTEGER REFERENCES accommodation(id) ON DELETE CASCADE,
    "city" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "total_price" FLOAT NOT NULL,
    "checkin" TIMESTAMP NOT NULL, 
    "checkout" TIMESTAMP NOT NULL
);

INSERT INTO "accommodation" ("category", "city", "address", "price_per_night", "owner") VALUES ('praia', 'Rio de Janeiro', 'Av. Atlântica - 1657', 1300, 'Jorge Russo');
INSERT INTO "accommodation" ("category", "city", "address", "price_per_night", "owner") VALUES ('cidade', 'São Paulo', 'Av. Brasil - 1234', 2300, 'Brad Patt');
INSERT INTO "accommodation" ("category", "city", "address", "price_per_night", "owner") VALUES ('praia', 'Salvador', 'Rua do Pelourinho - 1500', 900, 'Renato Aragão');

INSERT INTO "booking" ("accommodation_id", "city", "name", "total_price", "checkin", "checkout") VALUES (1, 'Rio de Janeiro', 'Kléberson Souza', 6500, '2024-11-10T18:30:00Z', '2024-11-15T18:30:00Z');
INSERT INTO "booking" ("accommodation_id", "city", "name", "total_price", "checkin", "checkout") VALUES (2, 'São Paulo', 'João da Silva', 2300, '2024-11-24T14:30:00Z', '2024-11-25T14:30:00Z');