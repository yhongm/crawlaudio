class FileEntry(object):
    def readUrl(self):
        url_file = open("crawl_url.txt", 'r')
        try:
            urlText = url_file.read()
            return urlText
        finally:
            url_file.close()

    def writeUrl(self, url):
        url_file = open("crawl_url.txt", 'w')
        try:
            url_file.write(url)
        finally:
            url_file.close()

    def readPath(self):
        path_file = open("crawl_path.txt", 'r')
        try:
            pathTxt = path_file.read()
            return pathTxt
        finally:
            path_file.close()

    def writePath(self, path):
        path_file = open("crawl_path.txt", 'w')
        try:
            path_file.write(path)
        finally:
            path_file.close()
