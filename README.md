# rpi_door
Using RPI to open the door.


## Install
```
git clone https://github.com/linnil1/rpi_door.git 
cd rpi_door
pip3 install -r requirments.txt
```

## Development
```
python3 app.py
```

## Production

### Add certification
Add your certification to `privkey.pem` and `cert.pem`.

or add self-signed certification
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out cert.pem
```

### Run
```
gunicorn app:app -b 0.0.0.0:5000 --keyfile privkey.pem --certfile cert.pem --worker-class eventlet -w 1 --access-logfile -
```

## Demo
![screenshot](https://raw.githubusercontent.com/linnil1/rpi_door/master/screenshot.jpg)
