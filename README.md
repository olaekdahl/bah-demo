## BoardGame

### Overview

This is the *BoardGame* repo.

### Setup

On your local machine, create an SSH key pair that will be used by GitHub Actions to access your EC2 instance. Do not use a passphrase with this SSH key pair.

`ssh-keygen -t rsa -b 4096 -C "github-actions-deploy" -f github-actions-deploy`

Add the public key (github-actions-deploy.pub) to the ~/.ssh/authorized_keys file of the user on the EC2 instance you intend to use for deployments (e.g., ec2-user).

`ssh ec2-user@your-ec2-instance-ip "echo $(cat github-actions-deploy.pub) >> ~/.ssh/authorized_keys"`

* Go to your GitHub repository.
* Navigate to "Settings" > "Secrets and variables" > "Actions".
* Click on "New repository secret".
* Name the secret DEPLOY_KEY and paste the content of your private key file (github-actions-deploy) into the value field.

