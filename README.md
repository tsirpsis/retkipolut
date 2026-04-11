# Retkipolut

## Sovelluksen kuvaus
Sovelluksen tarkoituksena on jakaa vinkkejä ja kokemuksia Suomen
retkikohteista ja luontopoluista sekä niiden palveluista.
Valmiissa sovelluksessa tulevat olemaan nämä toiminnot:

* Käyttäjä voi luoda tunnuksen ja kirjautua sisään sovellukseen.
* Käyttäjä voi lisätä retkikohteen, muokata sitä ja poistaa sen.
*	Käyttäjä voi lisätä kuvan retkikohteesta.
*	Käyttäjä näkee muiden käyttäjien lisäämät retkikohteet.
*	Käyttäjä voi hakea retkikohteita hakusanalla.
*	Käyttäjä voi tarkastella omia kohteitaan omilla sivuilla.
*	Käyttäjä voi luokitella reitin esim. sen pituuden ja palveluiden mukaan.
*	Käyttäjä voi kommentoida retkikohdetta.

Pääasiallinen tietokohde on retkikohde ja toissijainen on sen kommentti.

## Ohjeet sovelluksen testaamiseen
* Kloonaa tämä repositorio.
* Luo tietokanta database.db skeemasta schema.sql komennolla sqlite3 database.db < schema.sql.
* Käynnistä sovellus komennolla flask run.
