from django.http import StreamingHttpResponse


def file_iterator(file_name):
    with open(file_name, 'rb') as f:  # 切记open打开文件的方式
        while True:
            c = f.read()
            if c:
                yield c
            else:
                break


def stream_download(file_path, filename):
    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename={0}".format(
        filename.encode('utf-8').decode('ISO-8859-1')
    )
    return response
