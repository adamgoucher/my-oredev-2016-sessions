# Configuration Management

*Heuristic* - Without Configuration Management, you don't have infrastucture you have a garden of special snowflakes.

How you initially configure and maintain the configuration of your instances is largely dependent on whether or your you use ASG or not. If you don't then using a centralized server (Puppet, Chef) makes sense, but if you are using ASG then keeping track of certificates on machines that can appear and disappear is a pain so something like Ansible or Masterless Puppet is more relevant. Switching approaches, even from just classic Puppet to masterless Puppet, midstream is a pain.

And how do you get your configuration onto an instance? Well, now you get into the wonderful realm of Cloud-Init. Here is a sample User Data section from one of my ASG.

```yaml
#cloud-config
manage_etc_hosts: True

package_upgrade: False

packages:
- git

environment:
    MXCO_ENVIRONMENT: humans
    MXCO_ROLE: right

bootcmd:
- mkdir -p /root/.ssh

write_files:
-   content: |
        #!/usr/bin/env python3

        import json
        import yaml
        import os

        env_vars = {} 

        if os.path.exists('/etc/default/mobilexco'):
          with open('/etc/default/mobilexco', 'r') as f:
            for line in f:
              if '=' in line:
                pair = line.strip().split('=')
                env_vars[pair[0].upper()] = ( "%s=%s\n" % (pair[0].upper(),pair[1]) )

        if os.path.exists('/var/lib/cloud/instance/user-data.txt'):
          with open('/var/lib/cloud/instance/user-data.txt') as f: 
            user_data = yaml.load(f) 
            if (user_data is not None and 'environment' in user_data):
              for k, v in user_data['environment'].items(): 
                env_vars[k.upper()]=( "%s=%s\n" % (k.upper(), v) )

        with open('/etc/default/mobilexco', 'w') as f:
            f.writelines(env_vars.values())

        os.chmod('/etc/default/mobilexco', 0o644)
    path: /usr/local/bin/set-mobilexco-defaults
    owner: root:root
    permissions: "0744"
-   content: |
        #!/usr/bin/env bash
        
        source /etc/default/mobilexco
        export NAME=$MXCO_ENVIRONMENT-`curl -s http://169.254.169.254/latest/meta-data/instance-id | tr -d 'i-'`
        /usr/bin/hostnamectl set-hostname $NAME
        sed -i "0,/127.0.0.1/{s/^127.0.0.1.*$/127.0.0.1\ $NAME\ localhost/g}" /etc/hosts
    path: /usr/local/bin/set-hostname-from-instance-details
    owner: root:root
    permissions: "0744"
-   content: |
        -----BEGIN RSA PRIVATE KEY-----
        YOUR_KEY_HERE
        -----END RSA PRIVATE KEY----- 
    path: /root/.ssh/id_rsa-headless
    owner: root:root
    permissions: "0400"
-   content: |
      #!/usr/bin/env bash

      INSTANCE_ID=`curl -s http://169.254.169.254/latest/meta-data/instance-id`
      aws autoscaling complete-lifecycle-action --region us-west-2 --lifecycle-action-result CONTINUE --instance-id $INSTANCE_ID --lifecycle-hook-name slowstart --auto-scaling-group-name humans-right
    path: /usr/local/bin/asg-continue
    owner: root:root
    permissions: "0744"
-   content: |
      bitbucket.org,104.192.143.1 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAubiN81eDcafrgMeLzaFPsw2kNvEcqTKl/VqLat/MaB33pZy0y3rJZtnqwR2qOOvbwKZYKiEO1O6VqNEBxKvJJelCq0dTXWT5pbO2gDXC6h6QDXCaHo6pOHGPUy+YBaGQRGuSusMEASYiWunYN0vCAI8QaXnWMXNMdFP3jHAJH0eDsoiGnLPBlBp4TNm6rYI74nMzgz3B9IikW4WVK+dc8KZJZWYjAuORU3jc1c/NPskD2ASinf8v3xnfXeukU0sJ5N6m5E8VLjObPEO+mN2t/FZTMZLiFqPWc/ALSqnMnnhwrNi2rbfg/rd/IpL8Le3pSBne8+seeFVBoGqzHM9yXw==
    path: /root/.ssh/known_hosts
    owner: root:root
    permissions: "0644"
-   content: |
      #!/usr/bin/env bash

      cd /root/headless
      source /etc/default/mobilexco
      /opt/puppetlabs/bin/puppet apply --modulepath=/root/headless/code/modules --codedir /root/headless/code --environment $MXCO_ENVIRONMENT --confdir /root/headless/puppet code/environments/$MXCO_ENVIRONMENT/manifests/$MXCO_ROLE.pp
      /opt/puppetlabs/bin/puppet apply --modulepath=/root/headless/code/modules --codedir /root/headless/code --environment $MXCO_ENVIRONMENT --confdir /root/headless/puppet code/environments/$MXCO_ENVIRONMENT/manifests/$MXCO_ROLE.pp
    path: /usr/local/bin/headless
    owner: root:root
    permissions: "0744"
runcmd:
- /usr/local/bin/set-mobilexco-defaults
- /usr/local/bin/set-hostname-from-instance-details
- cd /root && ssh-agent bash -c 'ssh-add /root/.ssh/id_rsa-headless; git clone git@bitbucket.org:mobilexco/headless.git'
- /usr/local/bin/headless
- apt-get update; apt-get upgrade -y
- systemctl enable apt-daily.service
- /usr/local/bin/asg-continue

output : { all : '| tee -a /var/log/cloud-init-output.log' }
```

Note: This is for a custom AMI based on Canonical's official Ubuntu 16.04 image which has
* the apt-daily.service disabled to prevent it from fighting with Cloud-init for the apt directories
* puppet is already installed

Note: This means you are now now reliant on both AWS and Bitbucket (or GitHub) for your infrastructure to be able to come up -- as I learned the hard way when Atlassian has an outage

Note: Eventually there will be another line to put a git pull and puppet apply into cron and have it run every 15 minutes

Note: It takes around 8 minutes for a machine to come up. This can cause problems with CodeBuild and ASG Lifecycle timeouts. I'm considering having machine images built periodically so they are ready to spin up. That's still in the 'think about' phase.

We use a variation of the Role/Profile pattern where each ASG is a role / business name ('Humans - Left Node') and those Roles are built by multiple Profiles ('Ubuntu, Contests, Surveys').

```ruby
node default {
  include profiles::ubuntu
  include profiles::contests
}
```

```ruby
class profiles::ubuntu {
  class { 'apt':
    update => {
      frequency => 'daily',
    },
  }

  class { 'unattended_upgrades':
    auto    => {
      'reboot' => false
    },
    update  => 1,
    upgrade => 1,
    package_ensure => 'latest'
  }

  include '::ntp'

  apt::source { 'ubuntu_archive_xenial':
    location        => 'http://us-west-2.ec2.archive.ubuntu.com/ubuntu/',
    release         => 'xenial',
    repos           => 'restricted multiverse',
    include_src     => false,
    notify          => Exec['apt_update']
  }

  apt::source { 'localpkgs':
    location    => 'http://apt.mobilexco.com',
    release     => 'xenial',
    repos       => 'main contrib non-free',
    #key         => 'A13BE713',
    key         => '5B9CB50FD9A6C1FB194F134E64441B46A13BE713',
    #key         => '285C90D7FA56AA3E5438AEC5BB5D5CEB5C8BD785',
    key_source  => 'http://apt.mobilexco.com/localpkgs.gpg',
    include_src => false,
    notify      => Exec['apt_update']
  }

  package{'amazon-ssm-agent':
   audit   => all,
   ensure  => 'latest',
   require => Class['apt::update']
  }
}
```

```ruby
class profiles::laravel {
  class { '::php::globals':
    php_version => '7.0',
    config_root => '/etc/php/7.0',
  } ->
  class { '::php':
    ensure       => latest,
    manage_repos => false,
    fpm          => false,
    dev          => false,
    composer     => true,
    pear         => false,
    phpunit      => false,
    extensions   => {
      curl      => { },
      gd        => { },
      mysql     => { },
      mcrypt    => { },
      simplexml => { },
      zip       => { },
      predis     => {
        provider       => 'apt',
        package_prefix => 'libphp-',
      },
    }
  }
  
  file { [ '/etc/php',
           '/etc/php/7.0',
           '/etc/php/7.0/fpm',
           '/etc/php/7.0/fpm/pool.d' ]:
    ensure => 'directory',
    group  => 'root',
    owner  => 'root',
    mode   => 'u=rwx,go+rx',
    before => Package['php7.0-fpm']
  }

  package { 'php7.0-fpm':
    ensure => present,
  }

  file { '/etc/php/7.0/fpm/pool.d/www.conf':
    ensure  => absent,
    require => Package['php7.0-fpm'],
  }

  file { '/etc/php/7.0/fpm/conf.d/20-mcrypt.ini':
    ensure => link,
    target => '../../mods-available/mcrypt.ini',
    require => Package['php7.0-fpm'],
  }

  class { 'nginx': }

  class { 'supervisord':
    install_pip       => false,
    install_init      => false,
    package_provider  => 'apt',
    config_include    => '/etc/supervisor/conf.d',
    config_file       => '/etc/supervisor.conf',
    service_name      => 'supervisor',
  }

  # terrible hack until codedeploy gets their act together
  apt::ppa { 'ppa:brightbox/ruby-ng':
    notify => Exec['apt_update']
  }

  package { 'ruby2.0':
    ensure  => latest,
    require => [ Apt::Ppa['ppa:brightbox/ruby-ng'], Class['apt::update'] ],
  }

  package { 'codedeploy-agent':
    ensure  => latest,
    require => [ Package['ruby2.0'], Class['apt::update'] ],
  }

  service { 'codedeploy-agent':
    ensure  => running,
    enable  => true,
    require => Package[ 'codedeploy-agent' ]
  }

  include 'nfs::client'

  notice($::ec2_metadata[placement][availability-zone])
  ::nfs::client::mount { 'efs':
    server  => hiera('efs'),
    mount   => '/efs',
    share   => '/',
    options => 'rw',
    ensure  => 'mounted'
  }

  class { 'mysql::client': }

  class { 'python':
    ensure     => 'present',
    version    => 'system',
    pip        => 'present',
    dev        => 'absent',
    virtualenv => 'absent',
    gunicorn   => 'absent',
  }
    
  python::pip { 'awscli': }
}
```

Credit to the folks at [Unif.io](https://unif.io/) for the /etc/default trick 