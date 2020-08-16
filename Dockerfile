FROM python:3.6.1-slim
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
ENV FLASK_APP="main.py"
CMD ["flask", "run", "--host", "0.0.0.0"]

