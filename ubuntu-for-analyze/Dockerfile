# Используем базовый образ Ubuntu
FROM ubuntu:22.04

COPY /analyze/ /home/dockeruser/Code/

RUN apt update
RUN apt install python3 python3-pip strace -y
RUN pip3 install watchdog fire

# Обновление пакетов и установка необходимых компонентов
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    && mkdir /var/run/sshd

# Создание пользователя dockeruser с паролем dockeruser
RUN useradd -m -s /bin/bash dockeruser && \
    echo "dockeruser:dockeruser" | chpasswd && \
    usermod -aG sudo dockeruser

# Настройка SSH-сервера
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "AllowUsers dockeruser" >> /etc/ssh/sshd_config

# Открытие порта 22 для SSH
EXPOSE 22

# Команда для запуска SSH-сервера
CMD ["/usr/sbin/sshd", "-D"]
