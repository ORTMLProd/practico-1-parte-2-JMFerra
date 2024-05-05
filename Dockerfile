# Imagen base
FROM python:3.9.6 as base

# Crea y fija directorio de trabajo
WORKDIR /scrapers

# Copia los archivos de requerimientos
COPY requirements.in requirements.in

# Instala pip-tools y genera requirements.txt
RUN pip install -U pip
RUN pip install pip-tools
RUN pip-compile requirements.in

# Imagen principal
FROM python:3.9.6 as main
WORKDIR /scrapers

# Copia los archivos de requerimientos generados
COPY --from=base /scrapers/requirements.txt /scrapers/requirements.txt

# Instala las dependencias de nuestro proyecto
RUN pip install -r requirements.txt

# Instala ChromeDriver
RUN apt-get update && apt-get install -y wget unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Copia el resto del código al contenedor
COPY . .

# Ejecuta la araña
CMD ["bash"]

# docker build -t scrapy .
# docker run -it scrapy bash 
# scrapy crawl carone
