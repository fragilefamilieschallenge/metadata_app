FROM python:2.7-slim

# Install app
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN cd /app; pip install -r requirements.txt
ADD . /app

# Run app
EXPOSE 5000
CMD ["python", "/app/application.py"]
