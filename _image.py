#-*- coding: utf-8 -*-
import pytsk3 # raw image analysis and file system analysis
import pyewf  # ewf iamge file processing
import os
import time
import _conf
import _effi

class tsk():
    FILE_TYPE_LOOKUP = {
        pytsk3.TSK_FS_NAME_TYPE_UNDEF: "-",
        pytsk3.TSK_FS_NAME_TYPE_FIFO: "p",
        pytsk3.TSK_FS_NAME_TYPE_CHR: "c",
        pytsk3.TSK_FS_NAME_TYPE_DIR: "d",
        pytsk3.TSK_FS_NAME_TYPE_BLK: "b",
        pytsk3.TSK_FS_NAME_TYPE_REG: "r",
        pytsk3.TSK_FS_NAME_TYPE_LNK: "l",
        pytsk3.TSK_FS_NAME_TYPE_SOCK: "h",
        pytsk3.TSK_FS_NAME_TYPE_SHAD: "s",
        pytsk3.TSK_FS_NAME_TYPE_WHT: "w",
        pytsk3.TSK_FS_NAME_TYPE_VIRT: "v"}

    META_TYPE_LOOKUP = {
        pytsk3.TSK_FS_META_TYPE_REG: "r",
        pytsk3.TSK_FS_META_TYPE_DIR: "d",
        pytsk3.TSK_FS_META_TYPE_FIFO: "p",
        pytsk3.TSK_FS_META_TYPE_CHR: "c",
        pytsk3.TSK_FS_META_TYPE_BLK: "b",
        pytsk3.TSK_FS_META_TYPE_LNK: "h",
        pytsk3.TSK_FS_META_TYPE_SHAD: "s",
        pytsk3.TSK_FS_META_TYPE_SOCK: "s",
        pytsk3.TSK_FS_META_TYPE_WHT: "w",
        pytsk3.TSK_FS_META_TYPE_VIRT: "v"}

    ATTRIBUTE_TYPES_TO_PRINT = [
        pytsk3.TSK_FS_ATTR_TYPE_NTFS_IDXROOT,
        pytsk3.TSK_FS_ATTR_TYPE_NTFS_DATA,
        pytsk3.TSK_FS_ATTR_TYPE_DEFAULT]

    def __init__(self, url):
        self.url = url
        self._recursive = False
        self.extract_list = list()
        self.oCSV = _effi._CSVWriter("result.csv")

    def loadimage(self):
        ewformat = ['.s01', '.E01', '.Ex01', '.e01']
        rawformat = ['.dd', '.raw', '.001']
        ext = os.path.splitext(self.url)

        if ext[1] in ewformat:
            # TODO : pyewf
            filenames = pyewf.glob(self.url)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)
            img_info = ewf_Img_Info(ewf_handle)
            self.fs_info = pytsk3.FS_Info(img_info)

        elif ext[1] in rawformat:
            # TODO : pytsk
            img_info = pytsk3.Img_Info(url = self.url)
            self.fs_info = pytsk3.FS_Info(img_info)

    def setconf(self):
        # TODO : Extract condition from configuration file
        self.conf = _conf.extractconf()
        self.mtime = self.conf[0]
        self.atime = self.conf[1]
        self.ctime = self.conf[2]
        self.etime = self.conf[3]
        self.ext = self.conf[4]
        self.size = self.conf[5]
        self.path = self.conf[6]
        self.condition = self.conf[7]

    def list_directory(self, directory, stack=None):
        stack.append(directory.info.fs_file.meta.addr)

        for directory_entry in directory:
            print "[debug] ", type(directory_entry.info.meta)
            prefix = "+" * (len(stack) - 1)
            if prefix:
                prefix += " "

            # Skip ".", ".." or directory entries without a name.
            if (not hasattr(directory_entry, "info") or
                    not hasattr(directory_entry.info, "name") or
                    not hasattr(directory_entry.info.name, "name") or
                        directory_entry.info.name.name in [".", ".."]):
                continue

            self.print_directory_entry(directory_entry, prefix=prefix)

            if self._recursive:
                try:
                    sub_directory = directory_entry.as_directory()
                    inode = directory_entry.info.meta.addr

                    # This ensures that we don't recurse into a directory
                    # above the current level and thus avoid circular loops.
                    if inode not in stack:
                        self.list_directory(sub_directory, stack)

                except IOError:
                    pass

        stack.pop(-1)

    def open_directory(self, inode_or_path):
        inode = None
        path = None
        if inode_or_path is None:
            path = "/"
        elif inode_or_path.startswith("/"):
            path = inode_or_path
        else:
            inode = inode_or_path

        # Note that we cannot pass inode=None to fs_info.opendir().
        if inode:
            directory = self.fs_info.open_dir(inode=inode)
        else:
            directory = self.fs_info.open_dir(path=path)

        return directory

    def print_directory_entry(self, directory_entry, prefix=""):


        meta = directory_entry.info.meta
        name = directory_entry.info.name
        ext = os.path.splitext(name.name)

        mtime = time.ctime(meta.mtime)
        atime = time.ctime(meta.atime)
        ctime = time.ctime(meta.crtime)
        etime = time.ctime(meta.ctime)
        size = meta.size

        print mtime, atime, ctime, etime, name.name, size
        self.oCSV.writeCSVRow(name.name, str(ext[1]), "N/A", size, mtime, atime, ctime, etime, "N/A")

        name_type = "-"
        if name:
            name_type = self.FILE_TYPE_LOOKUP.get(int(name.type), "-")

        meta_type = "-"
        if meta:
            meta_type = self.META_TYPE_LOOKUP.get(int(meta.type), "-")

        directory_entry_type = "{0:s}/{1:s}".format(name_type, meta_type)

        for attribute in directory_entry:
            inode_type = int(attribute.info.type)
            if inode_type in self.ATTRIBUTE_TYPES_TO_PRINT:
                if self.fs_info.info.ftype in [
                    pytsk3.TSK_FS_TYPE_NTFS, pytsk3.TSK_FS_TYPE_NTFS_DETECT]:
                    #inode = "{0:d}-{1:d}-{2:d}".format(
                    #    meta.addr, int(attribute.info.type), attribute.info.id)
                    inode = "{0:d}".format(meta.addr)
                else:
                    inode = "{0:d}".format(meta.addr)

                attribute_name = attribute.info.name
                if attribute_name and attribute_name not in ["$Data", "$I30"]:
                    filename = "{0:s}:{1:s}".format(name.name, attribute.info.name)
                else:
                    filename = name.name

                if meta and name:
                    print("{0:s}{1:s} {2:s}:\t{3:s}".format(
                        prefix, directory_entry_type, inode, filename))
                    self.extract_list.append((inode, filename))

    def debug_print_extlist(self):
        print "[debug] extract_list"
        print self.extract_list

    def extract_directory_entry(self):

        for i in self.extract_list:
            f = self.fs_info.open_meta(inode = int(i[0]))
            print "[debug] TEST", int(i[0])
            name = i[1]
            print name

            offset = 0
            size = f.info.meta.size
            BUFF_SIZE = 1024 * 1024

            while offset < size:
                available_to_read = min(BUFF_SIZE, size - offset)
                data = f.read_random(offset, available_to_read)
                if not data: break

                offset += len(data)

                try:
                    # 여기에 디렉토리 엔트리로부터 경로를 추가해주면 경로 복구해서 출력?
                    output = open("./output/" + str(name), "w")
                    output.write(data)

                except:
                    pass

                finally:
                    output.close()

class ewf_Img_Info(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_Img_Info, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()

