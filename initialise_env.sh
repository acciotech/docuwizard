initial_setup(){
  apt-get update
  apt-get install -y locales git curl software-properties-common

  echo "LC_ALL=en_US.UTF-8" >> /etc/default/local
  echo "LC_ALL=en_US.UTF-8" >> /etc/environment

  echo "LANG=en_US.UTF-8" >> /etc/default/local
  echo "LANG=en_US.UTF-8" >> /etc/environment
  export DROPLET_USER=ubuntu
}

create_ubuntu_user(){
  adduser --disabled-password --gecos "" $DROPLET_USER
  mkdir -p /home/$DROPLET_USER/.ssh
  cp ~/.ssh/authorized_keys /home/$DROPLET_USER/.ssh/
  chown -R $DROPLET_USER:$DROPLET_USER /home/$DROPLET_USER/
  # chown root:root /home/$DROPLET_USER
  chmod 700 /home/$DROPLET_USER/.ssh
  chmod 644 /home/$DROPLET_USER/.ssh/authorized_keys
  usermod -a -G admin $DROPLET_USER
  echo "$DROPLET_USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
}

disable_root_access(){
  sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
  /etc/init.d/ssh restart
}
change_user(){
  su $DROPLET_USER
}
setup_docker_env(){
  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install ca-certificates curl gnupg
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  # Add the repository to Apt sources:
  echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
  sudo usermod -aG docker $DROPLET_USER
}

install_environment(){
  sudo apt-get install apache2 -y
  sudo a2enmod proxy proxy_http headers
  sudo snap install --classic certbot
  sudo ln -s /snap/bin/certbot /usr/bin/certbot
  sudo systemctl restart apache2
}
install_git(){
  sudo apt-get install -y git curl software-properties-common
}

setup_certbot(){
    sudo touch /etc/apache2/sites-available/docuwizard.acciotech.net.conf
    sudo a2ensite docuwizard.acciotech.net.conf
    sudo apache2ctl restart
    sudo certbot --apache
}