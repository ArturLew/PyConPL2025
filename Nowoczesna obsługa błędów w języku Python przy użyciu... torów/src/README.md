# "Nowoczesna obsługa błędów w języku Python przy użyciu... torów"  
Autor: Artur Lew - Prezentacja PyConPL 2025

# Inne języki
```java
try {
    int result = divide(10, 0);
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
}
```

```scala
import scala.util.{Try, Success, Failure}

def divide(a: Int, b: Int): Try[Int] = Try(a / b)

divide(10, 0) match {
  case Success(res) => println(s"Result: $res")
  case Failure(err) => println(s"Error: ${err.getMessage}")
}
```

```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

result, err := divide(10, 0)
if err != nil {
    fmt.Println("Error:", err)
}
```

```rust
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

fn main() {
    match divide(10, 0) {
        Ok(res) => println!("Result: {}", res),
        Err(e) => println!("Error: {}", e),
    }
}
```

```erlang
divide(A, 0) -> {error, division_by_zero};
divide(A, B) -> {ok, A div B}.

case divide(10, 0) of
    {ok, Result} -> io:format("Result: ~p~n", [Result]);
    {error, Reason} -> io:format("Error: ~p~n", [Reason])
end.
```

```haskel
divide :: Int -> Int -> Either String Int
divide _ 0 = Left "division by zero"
divide a b = Right (a `div` b)

main = case divide 10 0 of
    Right result -> print result
    Left err -> putStrLn ("Error: " ++ err)
```

## Przykłady

Prosty przykład:
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

Kolejny przykład:
```python
from returns.result import Result, Success, Failure

def validate_age(age: int) -> Result[int, str]:
    return Success(age) if age >= 18 else Failure("Za młody")

def parse_age(value: str) -> Result[int, str]:
    try:
        return Success(int(value))
    except ValueError:
        return Failure("Błędna liczba")

result = (
    parse_age("21")
    .bind(validate_age)
    .map(lambda x: f"Witaj! Wiek: {x}")
)
# -> Success("Welcome! Age: 21")
```

Przykład z asyncio:
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
         final = result.map(lambda x: len(x))
         print(final)
   ```