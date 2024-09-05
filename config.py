import os
# Настройки конфига
config_path = 'config.ini'

encoding = 'UTF-8'

sessions_path = 'sessions'

tg_sess_path = os.path.join(sessions_path, 'tg_sess.session')

temp_path = 'temp'

# Тексты
t_config_first = 'Вы запустили софт в первый раз. Нам потребуются некоторые ваши данные. После того, как вы введёте их единожды, они больше не потребуются'
