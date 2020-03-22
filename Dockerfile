FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install requests==2.22.0
CMD ["python","dnspod.py"]