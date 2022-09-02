Przygotuj aplikację w technologii Python (Django/Flask/FastAPI) z prostym interfejsem graficznym w formie formatki HTML pozwalającą na przeliczanie kursów między PLN a walutami: USD, EUR, CHF, JPY w danym dniu wg kursu średniego NBP.

NBP udostępnia archiwalne dane pod adresem https://www.nbp.pl/home.aspx?c=/ascx/archa.ascx
Przykład miesięcznego zestawienia tabel kursowych: https://www.nbp.pl/transfer.aspx?c=/ascx/ListABCH.ascx&Typ=a&p=rok;mies&navid=archa
Przykład dziennej tabeli kursów: https://www.nbp.pl/home.aspx?navid=archa&c=/ascx/tabarch.ascx&n=a127z160704
Tabela dostępna jest również w formacie XML: https://www.nbp.pl/kursy/xml/a127z160704.xml

Aplikacja powinna zapewniać przechowywanie tabele danych (lub tylko wybrane kursy USD, EUR, CHF, JPY) w bazie SQL (SQLite lub PostgreSQL).
Przetwarzanie żądania powinno przebiegać wg logiki:
- jeśli żądanie dotyczy dnia, dla którego dane przechowywane są już w bazie zwróć odpowiedni kurs z bazy
- jeśli żądanie dotyczy dnia, dla którego w bazie nie istnieją rekordy, wyślij zapytanie do serwisu NBP, przetwórz odpowiedź i zapisz odpowiednie rekordy w bazie aplikacji.

Od strony interfejsu aplikacji powinna umożliwić podanie:
- daty
- kwoty
- waluty wejściowej (jedna z PLN, USD, EUR, CHF, JPY)
- waluty wyjściowej (jedna z PLN, USD, EUR, CHF, JPY)

Interfejs aplikacji powinien komunikować się z backendem zgodnie ze standardem REST, w skład zadania wchodzi również opracowanie odpowiedniego routingu.

Aplikacja powinna być dostosowana do konteneryzacji, tj. powinien zostać przygotowany plik Dockerfile, który umożliwi zbudowanie kompletnej aplikacji razem z odpowiednią bazą danych. W Dockerfile powinny być odpowiednio zmapowane porty, aby pozwalały na uruchomienie aplikacji w przeglądarce.
