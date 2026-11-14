Directory: C:\Users\tuffg\sauchenik\urok-1-sreda-i-paketi\citat_na_denya


Mode                 LastWriteTime         Length Name                                                                                                                             
----                 -------------         ------ ----                                                                                                                             
d-----     14.11.2026 г.     22:31                .venv                                                                                                                            
d-----     14.11.2026 г.     22:29                data                                                                                                                             
-a----     14.11.2026 г.     22:29            238 .gitignore                                                                                                                       
-a----     14.11.2026 г.     22:29           2565 citat.py                                                                                                                         
-a----     14.11.2026 г.     22:29           2547 razmyana.md                                                                                                                      
-a----     14.11.2026 г.     22:29            387 README.md                                                                                                                        
-a----     14.11.2026 г.     22:29             72 requirements.txt                                                                                                                 


(.venv) PS C:\Users\tuffg\sauchenik\urok-1-sreda-i-paketi\citat_na_denya> dir data


    Directory: C:\Users\tuffg\sauchenik\urok-1-sreda-i-paketi\citat_na_denya\data


Mode                 LastWriteTime         Length Name                                                                                                                             
----                 -------------         ------ ----                                                                                                                             
-a----     14.11.2026 г.     22:29           1591 citati.txt                                                                                                                       


(.venv) PS C:\Users\tuffg\sauchenik\urok-1-sreda-i-paketi\citat_na_denya> type requirements.txt
markdown-it-py==4.3.0
mdurl==0.1.2
Pygments==2.21.0
rich==15.0.0
(.venv) PS C:\Users\tuffg\sauchenik\urok-1-sreda-i-paketi\citat_na_denya> Select-String "QUOTES" citat.py
                                                                                                                                                                                    
citat.py:18:QUOTES_FILE = Path(__file__).parent / "data" / "citati.txt"                                                                                                             
citat.py:21:def load_quotes(path: Path) -> list:                                                                                                                                    
citat.py:23:    quotes = []
citat.py:32:            quotes.append((text.strip(), author.strip()))
citat.py:33:    if not quotes:
citat.py:35:    return quotes
citat.py:38:def quote_of_the_day(quotes: list, day: datetime.date) -> tuple:
citat.py:40:    return quotes[day.toordinal() % len(quotes)]
citat.py:45:        quotes = load_quotes(QUOTES_FILE)
citat.py:51:    text, author = quote_of_the_day(quotes, today)
