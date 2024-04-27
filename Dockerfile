FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y curl ca-certificates libnss3-tools python3-selenium

# Trust the pingo.example.com SSL certificate
COPY pingo.example.com.crt /usr/local/share/ca-certificates/pingo.example.com.crt
RUN update-ca-certificates
RUN mkdir -p $HOME/.pki/nssdb && \
    certutil -d $HOME/.pki/nssdb -N --empty-password && \
    certutil -d sql:$HOME/.pki/nssdb -A -t "CT,C,C" -n 'pingo.example.com' -i /usr/local/share/ca-certificates/pingo.example.com.crt

# Install the scoring bot
COPY ./app /app
WORKDIR /app

CMD ["python3", "test_selenium.py"]