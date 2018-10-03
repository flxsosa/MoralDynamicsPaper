#!/bin/bash
rsync -azvv -e "ssh -i ~/.ssh/MyKeyPair.pem" ec2-user@34.216.147.249:/home/ec2-user/moral_dynamics/experiment_7/participants.db "../../data/empirical/experiment7.db"
