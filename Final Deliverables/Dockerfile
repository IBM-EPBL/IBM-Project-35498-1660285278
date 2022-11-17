FROM python:3.8
MAINTAINER Abishek Kumar <anjaanabishek10@gmail.com>
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]