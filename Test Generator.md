---
name: qasphere-test-generator
description: Generuje kompletny zestaw test case'ów (happy + negative paths, dążąc do 100% pokrycia przypadków użycia) na podstawie wykonanego zadania/feature'a i tworzy je bezpośrednio w QA Sphere przez REST API. Test casy są po polsku, standalone, z pełnymi repro stepami (dane wejściowe, wyjściowe, instrukcje konfiguracji) tak, by wykonała je osoba widząca aplikację pierwszy raz. Skill sam mapuje repozytorium na właściwy projekt w QA Sphere. UŻYWAJ ZAWSZE, gdy user prosi o wygenerowanie test case'ów, pokrycie testowe, "testy do tego feature'a", "pokryj testami", "wrzuć testy do QA Sphere", "test casy z tego co zrobiliśmy" — nawet jeśli nie padnie słowo "skill" ani "QA Sphere" wprost, a kontekstem jest ukończone zadanie deweloperskie.
user-invocable: true
version: loader
mode: remote-loader
remote:
  github_raw: "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/QA%20Sphere%20%E2%80%94%20Test%20Generator/SKILL.md"
  github_page: "https://github.com/DTCodePL/Claude_Skills/blob/main/QA%20Sphere%20%E2%80%94%20Test%20Generator/SKILL.md"
---

# QA Sphere — Test Generator (loader)

Ten plik jest **cienkim loaderem**. Nie zawiera logiki generowania testów ani endpointów —
pełna, zawsze aktualna i **wersjonowana** wersja jest trzymana na GitHubie i to ona jest źródłem prawdy.

## Krok obowiązkowy — pobierz i zastosuj wersję z GitHuba

Zanim wygenerujesz lub utworzysz jakikolwiek test case w QA Sphere:

**1. Pobierz pełny skill przez bash_tool:**
```bash
curl -sL "https://raw.githubusercontent.com/DTCodePL/Claude_Skills/main/QA%20Sphere%20%E2%80%94%20Test%20Generator/SKILL.md" \
  -o /tmp/qasphere_test_generator_skill.md
cat /tmp/qasphere_test_generator_skill.md
```

**2. Zastosuj pobraną treść ściśle** — to ona zawiera aktualne:
- konfigurację (BASE_URL, klucz API, wartości pola `automation`),
- przebieg: mapowanie repo→projekt, enumerację przypadków (100% pokrycia), reguły pisania standalone test case'ów po polsku,
- mapowanie na pola QA Sphere i endpointy REST API (foldery bulk-upsert, tworzenie test case'a),
- krok podglądu/potwierdzenia przed wysłaniem do API.

**3. Obsługa błędu pobierania** — jeśli `curl` zwróci błąd, plik jest pusty lub niedostępny:
- poinformuj użytkownika, że nie udało się pobrać aktualnej wersji z GitHuba,
- **zatrzymaj się i zapytaj, czy kontynuować** — nie zgaduj logiki, endpointów ani struktury z pamięci.

> ⚠️ Nie utrzymuj logiki w tym pliku i nie próbuj „aktualizować" go lokalnie.
> Wszystkie zmiany rób w repozytorium na GitHubie (z podbiciem `version:`) —
> loader zawsze pobierze najnowszą wersję.
