### install python3.6
    sudo apt-get update
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository -y ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get -y install python3.6 python3.6-dev python3-pip
    python3.6 -m pip install pip --upgrade

    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
    sudo update-alternatives --config python3
    python3 -V

when install protobuf fing error 
sudo pip3 install --upgrade pip setuptools wheel 
sudo pip install protobuf==2.6.1

### install protobuf3.11.3

    1.install and compress protobuf (version: protobuf 3.11.3)
    sudo wget https://github.com/protocolbuffers/protobuf/releases/download/v3.11.3/protobuf-python-3.11.3.tar.gz
    tar zxvf protobuf-python-3.11.3.tar.gz
    
    2.install protobuf compiler
    cd protobuf-3.11.3
    ./autogen.sh
    ./configure  --prefix=/usr/protobuf
    make
    make check
    sudo make install

    sudo cp /usr/protobuf/bin/protoc /usr/bin/protoc3
    sudo cp /usr/protobuf/bin/protoc /usr/local/bin/protoc3

### install opencv
sudo pip3 install opencv-python


### run example
    run example in different mode