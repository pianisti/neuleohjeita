# Neuleohjeita

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen neuleohjeita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään neuleohjeita.
* Käyttäjä pystyy lisäämään ja poistamaan kuvia neuleohjeesta.
* Käyttäjä näkee sovellukseen lisätyt neuleohjeet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät neuleohjeet.
* Käyttäjä pystyy etsimään neuleohjeita hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä neuleohjeita.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilaston (julkaistujen ohjeiden määrä) ja käyttäjän lisäämät neuleohjeet.
* Käyttäjä pystyy valitsemaan neuleohjeelle yhden tai useamman luokittelun (neuletyön taitotaso, tekniikka ja tyyppi).
* Sovelluksessa on pääasiallisena tietokohteena neuleohje ja toissijaisena tietokohteena kommentti ohjeeseen. Käyttäjä pystyy lisäämään kommentteja omiin ja muiden käyttäjien neuleohjeisiin liittyen.

## Sovelluksen asentaminen

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulu ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistä sovelluksen näin:

```
$ flask run
```
