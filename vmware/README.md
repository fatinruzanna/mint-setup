Mount VMWare Shared Folders
===========================

1. Install open-vm-tools:

        (sudo) apt-get install open-vm-tools


2. Open /etc/fstab file with your favourite editor:

        (sudo) nano /etc/fstab


3. Add the following line to /etc/fstab file to mount shared folders from Host:

        .host:/  /mnt/hgfs  vmhgfs  defaults,noauto,uid=1000,gid=1000   0   0


4. Create a udev rule file for the device:

        (sudo) nano /etc/udev/rules.d/10-local.rules


    **NOTE:** Naming the file as **10-local.rules** will ensure that it is looked at before other rules in the folder


5. Add the following line to your newly created 10-local.rules file:

        ACTION=="add", KERNEL=="vmhgfs", RUN+="/bin/mount /mnt/hgfs"


6. Create the _hgfs_ directory:

        (sudo) mkdir /mnt/hgfs

7. Add the mount and umount commands to /etc/init.d/open-vm-tools script:

        case "${1}" in
            start)
                # Check if we're running inside VMWare
                exit_if_not_in_vm

                log_daemon_msg "Loading open-vm-tools modules"
                log_progress_msg "vmhgfs"; modprobe vmhgfs
                log_progress_msg "vmsync"; modprobe vmsync
                log_progress_msg "vmblock"; modprobe vmblock
                modprobe -r pcnet32
                log_progress_msg "vmxnet"; modprobe vmxnet
                modprobe pcnet32
                log_end_msg 0

                log_daemon_msg "Mounting hgfs"
                mount -t vmhgfs .host:/ /mnt/hgfs    # ADD THIS LINE, THEN REMOVE THIS COMMENT
                log_end_msg 0

                log_daemon_msg "Starting open-vm daemon" "vmtoolsd"
                /usr/bin/vmtoolsd --background /var/run/vmtoolsd.pid
                log_end_msg 0
                ;;

            stop)
                # Check if we're running inside VMWare
                exit_if_not_in_vm

                log_daemon_msg "Stopping open-vm guest daemon" "vmtoolsd"

                if [ -f /var/run/vmtoolsd.pid ]
                then
                    kill $(cat /var/run/vmtoolsd.pid)
                fi

                log_end_msg 0

                log_daemon_msg "Unmounting hgfs"
                umount /mnt/hgfs                     # ADD THIS LINE, THEN REMOVE THIS COMMENT
                log_end_msg 0

                log_daemon_msg "Removing open-vm-tools modules"
                log_progress_msg "vmhgfs"; modprobe -r vmhgfs
                log_progress_msg "vmsync"; modprobe -r vmsync
                log_progress_msg "vmblock"; modprobe -r vmblock
                log_progress_msg "vmxnet"; modprobe -r vmxnet
                log_end_msg 0
                ;;


8. Restart your Linux Mint.


**References:**
* http://ubuntuforums.org/showthread.php?t=1596743
* http://ubuntuforums.org/showthread.php?t=168221



Optimize Linux VM with SSD
==========================

1. Open /etc/fstab file with your favourite editor:

        (sudo) nano /etc/fstab


2. Update the following line for SDA device in /etc/fstab file with **noatime,**:

        UUID=dbd586dd-28b0-485f-9750-b428a4aa8f00 /    ext4  noatime,  errors=remount-ro 0       1


3. Restart your Linux Mint.



**References:**
* https://sites.google.com/site/easylinuxtipsproject/ssd
