FROM python:3
COPY . /app
WORKDIR /app
RUN python3 -m pip install requests numpy git+https://github.com/Rapptz/discord.py
CMD ["python3", "/app/salus_bot/main.py"]