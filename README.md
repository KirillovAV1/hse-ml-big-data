# Домашнее задание #2. Big Data and ML

## Дашборд в Superset

<img width="1792" height="995" alt="image" src="https://github.com/user-attachments/assets/75fbd8ca-7c7b-465f-8fe9-c2d3b39dc42a" />

## Структура проекта

```
hse-ml-big-data/
├── .gitignore               
├── .dockerignore                
├── docker-compose.yml            # Docker Compose конфигурация
├── README.md              
│
├── postgres/                     # PostgreSQL скрипты
│   └── init/        
│       ├── 1_create_tables_script.sql        # Создание таблиц
│       └── 2_fill_tables_script.sql          # Заполнение данных
│
├── jupyter/                     
│   ├── Dockerfile               # Docker образ для Jupyter
│   ├── init.sh                  # Скрипт для создания пользователя
│   ├── requirements.txt         # Зависимости
│   └── jupyterhub_config.py     # Конфигурация JupyterHub
│
├── superset/                   
│   ├── Dockerfile               # Docker образ для Superset
│   └── init.sh                  # Скрипт для создания пользователя
│
├── notebooks/  
│    ├── *.ipynb                 # Jupyter ноутбуки
│    └── common/.                # Переиспользуемые части кода
│        ├── connections.py      # Создание движка и клиента для работы с БД и S3
│.       ├── ETL.py              # Функции по извлечению, обработке и выгрузке 
│        └── utils.py            # Агрегация функций из ETL.py в pipeline
```

## Быстрый старт

Для локального запуска необходимо:
- Создать `.env`
- Запустить `docker-compose`

### Пример файла .env

```env
# Postgres
DB_NAME=ml_analytic
DB_USER=root
DB_PASSWORD=root

# Minio
MINIO_USER=root
MINIO_PASSWORD=rootroot

# Jupyter
JUPYTER_USER=user
JUPYTER_PASSWORD=root

# Superset
SUPERSET_SECRET_KEY=rootkey
SUPERSET_ADMIN_USERNAME=root
SUPERSET_ADMIN_PASSWORD=root
SUPERSET_ADMIN_FIRST_NAME=root
SUPERSET_ADMIN_LAST_NAME=root
SUPERSET_ADMIN_EMAIL=root@example.com
```

### Запуск проекта

```bash
docker compose up -d --build
```

### Остановка проекта с удалением данных

```bash
docker compose down -v
```


## Описание процессов

1. БД. При запуске выполняются скрипты по созданию и заполнению таблиц
2. JupyterHub. При запуске с помощью скрипта создается пользователь, скачиваются необходимые для работы библиотеки. Также через конфиг прокидываются переменные окружения
3. Superset. При запуске с помощью скрипта создается пользователь
4. S3. Не требует никаких скриптов. Бакет будет создается позже из кода.
5. Общая агрегирующая функция pipeline из `utils.py` включает в себя следующие этапы:
    - Создание бакета для S3 (если его нет)
    - Загрузка сырых данных из БД
    - Выгрузка сырых данных в S3 (с разбитием по датам)
    - Выгрузка данных из S3
    - Обработка null значений
    - Обработка столбцов с датами
    - Обработка выбросов
