Optimize Linux VM with SSD
==========================

1. Open /etc/fstab file with your favourite editor:

        (sudo) nano /etc/fstab


2. Update the following line for SDA device in /etc/fstab file with **noatime,**:

        UUID=dbd586dd-28b0-485f-9750-b428a4aa8f00 /    ext4  noatime,  errors=remount-ro 0       1


3. Restart your Linux Mint.



**References:**
* https://sites.google.com/site/easylinuxtipsproject/ssd
