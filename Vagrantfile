Vagrant.configure("2") do |config|

    config.vm.box = "debian/bullseye64"

    config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    end

    config.vm.define "server_monitor" do |m|
    m.vm.network "public_network", ip: "192.168.3.127"
    end

end