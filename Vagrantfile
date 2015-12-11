Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "script/provision.sh"

  config.vm.provider "virtualbox" do |vb|
     vb.memory = "1024"
  end
end
