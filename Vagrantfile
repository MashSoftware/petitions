Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "script/provision.sh"
  config.vm.network "forwarded_port", guest: 5001, host: 5001
  config.vm.provider "virtualbox" do |vb|
     vb.memory = "1024"
  end
end
