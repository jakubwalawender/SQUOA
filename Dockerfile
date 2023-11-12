FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV TZ="Europe/Warsaw"
WORKDIR /gym_manager_bot
ADD requirements.txt /gym_manager_bot
RUN pip install -r requirements.txt
COPY . /gym_manager_bot
