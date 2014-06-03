========
Siri-API

Siri-API is a tool which opens Siri for your own wishes WITHOUT the requirement of a Jailbreak. It intercepts Yahoo searches and forwards them to [SPVoice](https://github.com/Hackworth/SPVoice), or runs internally defined commands in Python 3, depending on how you have it configured. Siri-API is configured to work with [SPVoice](https://github.com/Hackworth/SPVoice) without any configuration changes. Opening Siri and saying <code>"Yahoo turn on kitchen lights"</code> or <code>"Yahoo watch Game of Thrones Season 4 Episode 3"</code> is how I use it at my house. Alternatively, it also works with Google, with a keyword, which is by default "Siri." For example, "Google Siri turn off hallway" or searching for "Siri turn off hallway" in Safari. 

You need a Linux running computer (tested on Raspberry Pi and Ubuntu 11.04) and a Squid Proxy version compiled with SSL support. These versions aren't available from official package sources, so you have to compile it yourself. You can follow the instructions in the documentation.

You can watch the demo video on http://youtu.be/b2F7PAwpjcY to see what is possible with Siri-API. I use the program for my home automation system but any other usage is possible. You just have to write your own rules and commands in Python 3 or use SPVoice Plugins. 

Siri-API requires your Squid proxy to impersonate https://google.com and https://search.yahoo.com with a self-signed certificate

I tested Siri-API on an iPhone 5S with iOS 7 but it will work with any device capable of Google or Yahoo searches, by pointing them to the proxy URL.

To install, first install development packages:

    sudo apt-get install build-essential libssl-dev git

Next, download and install Squid. Compiling Squid can take a long time depending on your system:

    mkdir ~/squid && cd ~/squid
    wget http://www.squid-cache.org/Versions/v3/3.4/squid-3.4.4.tar.gz
    tar -xvzf squid-3.4.4.tar.gz
    cd squid-3.4.4/
    sudo ./configure --prefix=/usr/local/squid --enable-icap-client --enable-ssl --enable-ssl-crtd --with-default-user=squid    
    sudo make all
    sudo make install
    rm -rf ~/squid

Create a squid user, set permissions, and create a swap directory:

    sudo useradd squid
    sudo chown -R squid:squid /usr/local/squid/var/logs/
    sudo /usr/local/squid/sbin/squid -z 

Generate an SSL Certificate to impersonate https://google.com or https://yahoo.com

    cd /usr/local/squid
    sudo mkdir ssl_cert
    cd ssl_cert
    sudo openssl req -new -newkey rsa:1024 -days 3065 -nodes -x509 -keyout
    siri-api.pem -out siri-api.pem
    sudo chown -R squid:squid /usr/local/squid/ssl_cert

Create a DB for dynamically generated certificates:

    sudo mkdir /usr/local/squid/var/lib
    sudo /usr/local/squid/libexec/ssl_crtd -c -s /usr/local/squid/var/lib/ssl_db -M 4MB
    sudo chown -R squid:squid /usr/local/squid/var/lib/ssl_db/

Install Siri-API:

    mkdir ~/siri && cd ~/siri
    git clone https://github.com/HcDevel/Siri-API
    cd Siri-API
    sudo mv /usr/local/squid/etc/squid.conf /usr/local/squid/etc/squid.conf_BACKUP
    sudo cp squid.conf /usr/local/squid/etc/squid.conf

Enable IP Forwarding and modify iptables:

    sudo su
    echo "1" > /proc/sys/net/ipv4/ip_forward
    iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport 443 -j REDIRECT --to-ports 3128
    iptables -I INPUT -p tcp -m tcp --dport 3128 -j ACCEPT
    logout

Modify server.py and enter your server's hostname or IP Address under <code>squid_hostname</code>:

    vim ~/siri/Siri-API/server.py

Finally, start the Squid Proxy and Siri-API:

    sudo /usr/local/squid/sbin/squid
    python3 ~/siri/Siri-API/server.py

On your iOS device, naviagate to your Wifi settings, change your proxy to auto, and enter

    http://HOSTNAME:3030/proxy.pac

Change HOSTNAME to the name or IP of your server. The pac file will instruct your device to only use Siri-API for Yahoo or Google searches

You can test Siri-API by going to: 

    http://HOSTNAME:3030/search?p=ENTER+COMMAND+TO+TEST

If you have any problem, please report it by opening an issue in the issue tracker.
