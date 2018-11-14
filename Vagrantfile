# -*- mode: ruby -*-
# vi: set ft=ruby :

# Usage:
# vagrant up ubuntu

Vagrant.configure("2") do |config|

  # Please keep this as False, so we can deploy with SSHKit.
  # Otherwise, it should be True.
  config.ssh.insert_key = true

  config.vm.provider :virtualbox do |v|
    # Ubuntu is creating a kernel log file in the host machine called
    # ubuntu-xenial-16.04-cloudimg-console.log
    # This config below will prevent this.
    v.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
    v.memory = 512
    v.cpus = 2
    # Attempts to increase network speed. Check below for details
    # 
    # Here a list of virtual network adapters you can try if you feel the
    # guest machines are not performing well. To me, the best one was 
    # virtio.
    #
    # V-NIC:  Am79C970A, Am79C973, 82540EM, 82543GC, 82545EM, and virtio
    v.customize ["modifyvm", :id, "--nictype1", "virtio"]
    v.customize ["modifyvm", :id, "--nictype2", "virtio"]
    # 
    # minimal = Mac, kvm = Linux, hyperv = Windows or 'none' if doesn't work.
    v.customize ["modifyvm", :id, "--paravirtprovider", "minimal"]
  end

  config.vm.define :ubuntu, primary: true, autostart: true do |ubuntu|
    # Ubuntu 17.10 and newer removed legacy binary files that Vagrant 
    # uses to setup network interfaces and it only was solved in Vagrant 2.0.3.
    #
    # As for 14/11/2018, Ubuntu 18.04 / Bionic Beaver and other Linux variants 
    # uses Vagrant 2.0.2.
    #
    # For now, please keep using Ubuntu 16.04 / Xenial Xerus as a box, until
    # the updates arrives in Ubuntu 18.04 LTS to all desktop users. Details below:
    #
    # https://github.com/hashicorp/vagrant/issues/9134
    ubuntu.vm.box = "ubuntu/xenial64"
    ubuntu.vm.hostname = "ubuntu"
    ubuntu.vm.network :private_network, ip: "192.168.123.101"

    # Will uncomment after my flask app becomes available.
    #ubuntu.vm.provision "ansible" do |ansible|
    #  ansible.playbook = "ansible/ubuntu.yml"
    #  ansible.become = true
    #  ansible.become_user = "root"
    #  ansible.compatibility_mode = "2.0"
    #  # Ubuntu 18.04 LTS (Bionic Beaver) no longer has Python 2 installed.
    #  # Ubuntu 16.04 LTS (Xenial Xerus) has both Python 2 and 3.
    #  # Therefore, preparing for the future here.
    #  ansible.extra_vars = { ansible_python_interpreter: "/usr/bin/python3" }
    #end

  end

end
