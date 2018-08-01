import arrow
import os
import shutil

def run_backup(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('{0}.csv'.format(arrow.now().format('YYYY-MM-DD'))):
                shutil.copy(os.path.join(root,f), dst_dir)

    print ("\n------------------------------")
    print("")
    print ("Creating {0}".format(os.path.join(root,f)))


if __name__ == '__main__':

    s_dir = "E:/utilization/production/files"
    d_dir = "E:/utilization/backups/backup_files"
    run_backup(s_dir, d_dir)