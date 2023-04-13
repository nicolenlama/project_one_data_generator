FROM registry.fedoraproject.org/f33/python3
#COPY into image
COPY . /tmp
WORKDIR /tmp
# Install dependencies
RUN pip install -r ./requirements.txt
# Setting Persistent data
VOLUME ["/temp_models"]
# Running Python Application
CMD ["python3" , "--size 10 --failureRate 1 --reason training" , "src/dataGenerator.py"]