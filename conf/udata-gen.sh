#!/bin/bash
printf "#!/bin/bash\n"
printf "exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1\n"
printf "export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\n"
printf "export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\n"
printf "python27 /home/ec2-user/deploy.py\n"
