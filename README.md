# Retkipolut

## Sovelluksen kuvaus ja toiminnot
Sovelluksen tarkoituksena on jakaa kokemuksia retkikohteista ja luontopoluista.

* Käyttäjä voi luoda tunnuksen ja kirjautua sisään sovellukseen.
* Käyttäjä voi lisätä retkikohteen, muokata sitä ja poistaa sen.
*	Käyttäjä voi lisätä kuvia retkikohteesta.
*	Käyttäjä voi luokitella reitin sen pituuden, kunnon ja vaativuuden mukaan.
*	Käyttäjä näkee muiden käyttäjien lisäämät retkikohteet ja niiden kommentit.
*	Käyttäjä voi hakea retkikohteita hakusanalla.
*	Käyttäjä näkee omilla sivuillaan tilastoja sekä omat kohteensa ja kommenttinsa.
*	Käyttäjä voi kommentoida omia ja muiden retkikohteita.

## Ohjeet sovelluksen testaamiseen
* Kloonaa tämä repositorio.
* Asenna `flask`-kirjasto:
```
$ pip install flask
```
* Luo tietokannan tarvitsemat taulut ja lisää tiedot luokista:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
* Käynnistä sovellus komennolla `flask run`.
