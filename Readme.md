Procedure
---------


Setup RPi with Raspbian

Follow [this](http://mitchtech.net/vnc-setup-on-raspberry-pi-from-ubuntu/) guide to share your WiFi from Ubuntu over ethernet and access RPi over ssh. Also, helps to set up VNC. 

Installation
------------

We will pull the latest .debs from RPi mirror

1. Installing numpy

```
wget http://mirrordirector.raspbian.org/raspbian/pool/main/p/python-numpy/python-numpy_1.7.1-3_armhf.deb

sudo dpkg -i python-numpy_1.7.1-3_armhf.deb
```

2. Installing Pandas and dependencies
```
wget http://mirrordirector.raspbian.org/raspbian/pool/main/p/pandas/python-pandas-lib_0.12.0-2_armhf.deb

wget http://mirrordirector.raspbian.org/raspbian/pool/main/p/pandas/python-pandas_0.12.0-2_all.deb

wget http://mirrordirector.raspbian.org/raspbian/pool/main/s/six/python-six_1.5.2-1_all.deb

wget http://mirrordirector.raspbian.org/raspbian/pool/main/p/python-dateutil/python-dateutil_1.5+dfsg-1_all.deb 

wget http://mirrordirector.raspbian.org/raspbian/pool/main/p/python-tz/python-tz_2012c-1_all.deb

sudo dpkg -i python-dateutil_1.5+dfsg-1_all.deb
sudo dpkg -i python-tz_2012c-1_all.deb 
sudo dpkg -i python-six_1.5.2-1_all.deb
sudo dpkg -i python-pandas-lib_0.12.0-2_armhf.deb 
sudo dpkg -i python-pandas_0.12.0-2_all.deb 
```

3. Installing scikit-learn

```
wget http://mirrordirector.raspbian.org/raspbian/pool/main/s/scikit-learn/python-sklearn-lib_0.14.1-2_armhf.deb

wget http://mirrordirector.raspbian.org/raspbian/pool/main/s/scikit-learn/python-sklearn-lib_0.14.1-2_armhf.deb

sudo dpkg -i python-sklearn-lib_0.14.1-2_armhf.deb
sudo dpkg -i --ignore-depends="python-sklearn" "python-scikits-learn_0.14.1-2_all.deb" 
```

4. Installing git
```
sudo apt-get install git
```





