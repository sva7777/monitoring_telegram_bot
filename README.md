# Общее описание  
Утилита для мониторинга работоспособности устройств.  
Утилита разделена на две части.  
**Server**- выполняет сам мониторинг, уведомление. Может наблюдать за работоспособностью многих устройств, отсылать данные в разные чаты от имени разных ботов. Предполагается работа в течении длительного времени.
На взаимодействие к пользователем напрямую.  
**Client** — получает параметры от пользователя из командной строки. Передает данные **Server**   

# Ограничения  
- уведомления отправляется в telegram от имени бота  
- работоспособность устройства определяется командой ping ( в сети в которой тесторовалось, были проблемы с сетью, ping терялись. Т.е. были ложные срабатывания)  
- при старте сервера, программа не сообщает работоспособно или нет устройство. Уведомления отсылаются только при изменении работоспособности  
- Отсутствует идемпотентность API взаимодействия Server и Client. На текущий момент предполагается, что будет локальное взаимодействие. Соответственно и проблемы во взаимодействии маловероятны  

# Подготовка  
- нужно иметь telegram token от бота  
- бот должен состоять в чате в который предполагается отправка сообщений  
- нужно знать chat_id. Проще всего его увидеть в Web версии телеграмм ( в URL).  
ToDo: добавить картинку, свой chat_id закрыть черным  
- ToDo: расписать скачивание репозитория  
Расписывать git clone или http. Может скачивание архивом  
- ToDo: Расписать запуск в venv?  
ToDo: подумать разделять venv или нет **Server** и **Client**.  
- ToDo: установить пакеты из requirements.txt для **Server** и/или **Client**  
- ToDo: подумать, насчет генерации `openapi.yaml`  
возможно стоит выкладывать файл в github  
- ToDo: расписать генерацию для **Client** stub интерфейса взаимодействия с **Server**

# Запуск Server  
- ToDo: проверить, будет ли работать Server на Windows(сомневаюсь насчет uvicorn. Он использует uvloop)?  
- `cd Server`  
- `python3 main.py`  
ToDo: возможно следует запускать uvicorn вручную, а не автоматически  
ToDo: указать возможность указать port  

# Запуск Client   
- ToDo: проверить, будет ли работать **Client** на Windows?  
Должно работать. Проблем не вижу  
- `cd Client`
- `python3 main.py [OPTIONS] COMMAND [ARGS]…`
опция:
`--help` вывод помощи по командной строке
  
команды:
`add-mon` – начать мониторинг  
аргументы для add-mon  
| аргумент | Тип | Описание| Обязательный | Пример |  Значение по умолчанию | 
| ------ | ------ | ------ | ------ | ------ | ------ | 
| `--server_address` | TEXT | адрес доступа к серверу | нет | `--server_address=http://0.0.0.0:8500` | `--server_address=http://0.0.0.0:8500` | 
| `--chat_id` | INTEGER | telegram chat id | да |  |  | 
| `--token` | TEXT | ToDo | да |  |  | 
| `--ip_address` | TEXT | IP (ipv4) адрес устройства работоспособность которого мониторируется.ToDo: проверить IPv6. Вроде нужно указывать имя интерфейса. | да |  |  | 
| `--mon_type` | TEXT | способ мониторинга. На текущий момент поддерживается только ping | нет |  | ping |   

Вывод:  
В случае успеха Client выдаст ID – уникальный идентификатор мониторинга  

`del-mon`  - удалить (остановить мониторинг)  
аргументы для del-mon  
| аргумент | Тип | Описание| Обязательный | Пример |  Значение по умолчанию | 
| ------ | ------ | ------ | ------ | ------ | ------ | 
| `--server_address` | TEXT | адрес доступа к серверу | нет | `--server_address=http://0.0.0.0:8500` | `--server_address=http://0.0.0.0:8500` | 
| `--id` | INTEGER | уникальный ID мониторинга. Может быть получен в качестве вывода выполнения команды add-mon или можно посмотреть вывод команды list-mon | да |  |  |   

`list-mon` – вывести данные по мониторингу  
| аргумент | Тип | Описание| Обязательный | Пример |  Значение по умолчанию | 
| ------ | ------ | ------ | ------ | ------ | ------ | 
| `--server_address` | TEXT | адрес доступа к серверу | нет | `--server_address=http://0.0.0.0:8500` | `--server_address=http://0.0.0.0:8500` |  

ToDo: добавить пример вывода  

# Известные проблемы  
- нет проверки правильности telegram bot token и chat_id при старте мониторинга  
О данной проблеме сейчас узнается когда отправляется сообщение в логах, при этом прекращается мониторинг (IMHO он бессмысленный, не сможем отправить данные в telegram, а в этом смысл программы)  

# Будущее развитие  
- возможно в будущем будет поддерживаться e-mail или другие средства  
- использование других средств кроме ping  
- Устанавливать ThresHold(порог) на время/количество ping пакетов которые последовательно могут быть потеряны  
- в телеграмм иметь возможность давать команды боту  
Т.е. я уже нахожусь в чате. Там есть бот. Можно указать IP устройства для мониторинга. Остановить мониторинг, получить данные о том что мониторится сейчас и так далее.  
ToDo: большой вопрос, что если запущено несколько экземпляров Server.  
Как я могу ограничить это?  
По факту запрос будет обработан **Server** который считает запрос.  
IMHO такое поведение будет нормальным

