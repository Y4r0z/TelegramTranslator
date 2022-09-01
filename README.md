# Telegram Translator

Это **Python** программа для трансляции сообщений из Telegram во ВКонтакте. Она представляет из себя бота, работающего с API обеих платформ.

## Установка

Для установки программы, достаточно скопировать содержимое репозитория и через [pip](https://pip.pypa.io/en/stable/) установить *requirements.txt*.

```bash
pip install -r requirements.txt
```
После требуется:
- Создать сообщество ВКонтакте;
- Получить его [токен](https://dev.vk.com/api/access-token/getting-started#%D0%9A%D0%BB%D1%8E%D1%87%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B0);
- [Пригласить](https://vk.com/@articles_vk-vk) сообщество в беседу, которая будет принимать транслированные из Telegram сообщения;
- Дать приглашенному сообществу право на чтение переписки; 
- [Получить](https://teletype.in/@lavhost/telegram-api) Telegram API ID / Hash для Telegram;
- Подписаться в Telegram на интересующие вас каналы / чаты.


## Авторизация

Программа запускается через файл *main.py*.
```bash
python3 main.py
```
После запуска программы требуется ввести данные для API:
- Токен ВКонтакте;
- Telegram API ID;
- Telegram API Hash.

После ввода API нужно будет пройти авторизацию Telegram и тогда бот будет запущен.

Если вы хотите запустить бота на сервере, то легче будет сначала авторизироваться на вашем компьютере, а потом перенести на сервер папки ***config/*** и ***sessions/***.
## Использование

Бот имеет 5 команд для взаимодействия:
- !добавить - бот начнет отслеживать вашу беседу ВКонтакте;
- !подписка <НАЗВАНИЕ КАНАЛА> - бот подпишет вашу беседу на сообщения из канала или чата, название которого вы указали;
- !отписка <НАЗВАНИЕ КАНАЛА> - бот отпишет вашу беседу от канала или чата;
- !список - бот отправит в вашу беседу ваши подписки;
- !стоп - полная остановка программы с сохранением подписок.

### Пример работы

![Пример](https://raw.githubusercontent.com/Y4r0z/TelegramTranslator/main/example/vk.png)

### Со стороны Telegram

![Пример](https://raw.githubusercontent.com/Y4r0z/TelegramTranslator/main/example/telegram.png)

## Лицензия
[MIT](https://choosealicense.com/licenses/mit/)
