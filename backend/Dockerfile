FROM python:latest

RUN mkdir /backend
WORKDIR /backend

COPY . /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# for error message
ENV PYTHONUNBUFFERED 1

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]