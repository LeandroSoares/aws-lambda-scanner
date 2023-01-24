# aws-lambda-scanner

O projeto é composto por dois scripts:

- scan_lambdas.py: realiza um scan procurando pelos lambdas que o runtime está depreciado
- update_runtimes.py: altera o runtime para o runtime configurado no script.

## Pré requisitos

- python 3.9

## Preparação

Crie o ambiente virtual e ative-o, depois instale as dependências

```powershell
python -m virtualenv venv

.\venv\Scripts\activate.ps1

pip install -r requirements.txt
```

## scan_lambdas.py
```text
usage: scan_lambdas.py [-h] [-l LOG_LEVEL] -d DEPRECATED_RUNTIME_LIST -p PROFILES [PROFILES ...]

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log_level LOG_LEVEL
  -d DEPRECATED_RUNTIME_LIST, --deprecated_runtime_list DEPRECATED_RUNTIME_LIST
                        path to the deprecated_runtime_list file
  -p PROFILES [PROFILES ...], --profiles PROFILES [PROFILES ...]
                        env profile
```

## update_runtimes.py
```text
usage: update_runtimes.py [-h] [-l LOG_LEVEL] -s SOURCE_CSV -p PROFILE

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log_level LOG_LEVEL
  -s SOURCE_CSV, --source_csv SOURCE_CSV
                        path to the csv file
  -p PROFILE, --profile PROFILE
                        env profile
```
