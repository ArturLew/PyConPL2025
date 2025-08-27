# Nowoczesna obsługa błędów w języku Python przy użyciu... torów

Todo:

- przykłady z automatycznymi annotacjami zarowno dla kodu synch jak i asynch
- zmierzyc narzut czasowy wprowadzany przez ROP

1. Obsługa błędów w Pythonie a inne języki programowania - 10 minut.  

   Standardowe podejście w Pythonie:
     - Python: try / except / finally jako główny mechanizm obsługi błędów.
     - Python promuje styl „EAFP” (Easier to Ask Forgiveness than Permission). → zamiast sprawdzania warunków wcześniej (if), często wyłapuje się wyjątki.
     - Problem: wyjątki są imperatywne i rozproszone – logika biznesowa miesza się z obsługą błędów.

   Obsluga bledow w innych jezykach:
     - Java / C# – checked exceptions (wymuszenie jawnego deklarowania wyjątków), co poprawia przewidywalność, ale bywa upierdliwe.
     - Go – brak wyjątków, zamiast tego zwraca się (result, error) → wymusza jawne sprawdzanie błędów.
     - Rust – `Result<T, E>` jako typ zwracany, wymuszający obsługę.
     - Python nie ma typów wynikowych wbudowanych → stąd biblioteki takie jak returns.????

   Problemy z wyjątkami:
     - „Wyjątek może wyskoczyć wszędzie” – trudniej o przewidywalny przepływ.
     - Ukryta dokumentacja: z sygnatury funkcji nie widać, jakie błędy mogą wystąpić.
     - Możliwe błędy w stylu: połknięcie wyjątku (except Exception: pass), albo zbyt ogólne obsługiwanie błędów.

   Wniosek dla słuchaczy: Python daje elastyczność, ale brakuje w nim bezpiecznych, funkcyjnych wzorców jawnej obsługi błędów.

2. Wprowadzenie do wzorca ROP - 5 minut.  

   Metafora „torów kolejowych”:
    - Funkcje traktowane jako operacje na danych (pociąg jedzie po torach).
    - Jeśli wszystko działa, jedziemy prawym torem (happy path).
    - Jeśli pojawi się błąd, przechodzimy na tor błędów (error track) i dalej już tam zostajemy.
    - Klucz: unikamy skakania z try/except i rozproszonej obsługi.

   Idea funkcyjna:
      - Zamiast wyjątku → wynik to Success albo Failure (Ok/Err).
      - Łańcuch transformacji działa tylko na sukcesie, a błąd „przepływa” dalej.

   Dlaczego to działa w praktyce?
   - Czytelniejszy przepływ danych.
   - Jawne informowanie o błędach.
   - Możliwość łatwego komponowania funkcji.

3. Biblioteka returns - 5 minut  

   Co daje returns?
    - Implementuje monadyczne podejście znane z języków funkcyjnych w Pythonie.
    - Główne typy:
        - Result[a, b] – sukces (Success) lub błąd (Failure).
        - Maybe[a] – Some lub Nothing.
        - IO, FutureResult, RequiresContext.
    - Funkcje: map, bind, alt, unwrap_or, failure(), itd.
  
   Zalety:
    - Typowanie dzięki mypy.
    - Bezpieczne i przewidywalne API.
    - Zgodność z ROP (Railway Oriented Programming).
  
   Krótki przykład:

   ```python
   from returns.result import Result, Success, Failure

   def parse_int(value: str) -> Result[int, str]:
      try:
         return Success(int(value))
      except ValueError:
         return Failure(f"Cannot parse {value}")

   result = parse_int("42").map(lambda x: x * 2)
   # -> Success(84)

   result = parse_int("abc").map(lambda x: x * 2)
   # -> Failure("Cannot parse abc")
   ```

4. Przykłady użycia wzorca ROP w aplikacjach synchronicznych - 10 minut.  

   Walidacja danych wejściowych (formularze, API):

    ```python
    from returns.result import Result, Success, Failure

    def validate_age(age: int) -> Result[int, str]:
        return Success(age) if age >= 18 else Failure("Too young")

    def parse_age(value: str) -> Result[int, str]:
        try:
            return Success(int(value))
        except ValueError:
            return Failure("Invalid number")

    result = (
        parse_age("21")
        .bind(validate_age)
        .map(lambda x: f"Welcome! Age: {x}")
    )
    # -> Success("Welcome! Age: 21")
    ```

   Łączenie kilku walidacji (ROP → łańcuch transformacji):
   - Pociąg jedzie → jeśli jeden etap zawiedzie, reszta się nie wykona.

   Integracja z kodem produkcyjnym:
   - Parsowanie plików konfiguracyjnych.
   - Walidacja requestów RESTowych.
   - Komunikacja z zewnętrznymi API.

5. Przykłady użycia wzorca ROP w aplikacjach asynchronicznych - 5 minut.  

   FutureResult w returns:
   - Łączy async/await z monadą Result.
   - Zamiast try/except w async kodzie mamy kompozycję monadyczną.

   Przykład:

   ```python
   import aiohttp
   from returns.future import FutureResult, future_safe

   @future_safe
   async def fetch_data(url: str) -> str:
         async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
               return await response.text()

   async def main():
         result = await fetch_data("https://example.com")
         # result to Success(...) lub Failure(...)
         final = result.map(lambda x: len(x))
         print(final)
   ```

   Zastosowanie:
   - Integracje z API.
   - Asynchroniczne pipeline’y ETL.
   - Obsługa błędów w mikroserwisach async.

6. Podsumowanie i pytania - 10 minut.
