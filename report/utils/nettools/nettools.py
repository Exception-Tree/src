from pathlib import Path
from urllib.parse import urlparse

import requests
#from loguru import logger

#from mputils.nettools.Zipper import Zipper


class NetTools(object):
    PROCESSING_SERVER = 'http://tex.npcap.xyz'
    PROCESSING_PORT = '5000'

    multipart_headers = {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data',
    }

    def __init__(self, *, output_directory=''):
        self.__output_directory = output_directory
        pass

    @classmethod
    def base_url(cls):
        ret = cls.PROCESSING_SERVER
        if cls.PROCESSING_PORT:
            ret += f':{cls.PROCESSING_PORT}'
        return

    @classmethod
    def set_processing_server(cls, *, server: str, port=5000):
        path = urlparse(server)
        scheme = path.scheme if path.scheme else 'http'
        hostname = path.hostname if path.hostname else path.path
        cls.PROCESSING_SERVER = f'{scheme}://{hostname}'
        cls.PROCESSING_PORT = path.port if path.port else port if port else 5000

    @classmethod
    def check_connection(cls) -> bool:
        try:
            requests.get(f'{cls.PROCESSING_SERVER}:{cls.PROCESSING_PORT}')
            return True
        except requests.exceptions.ConnectionError as err:
            logger.error(err)
            return False

    @classmethod
    def tex2pdf(cls, tex_file: str, folder_map=None, output_directory: Path = None):
        """
        :param output_directory:
        :param extrn_folder:
        :param tex_file: Исходный tex-файл
        :param folder_map: Путь к папке с картинками
        :return:
        """
        files = {}
        tex_file = Path(tex_file)
        if not output_directory:
            output_directory = tex_file.parent
        print('Begin generate pdf over the network\nbe patient...')

        if folder_map:
            z = Zipper()
            z.add_folder(Path(folder_map))
            files['filename'] = tex_file.relative_to(folder_map)
            files['assets'] = ('assets.zip', z.generated_zip)
            endpoint = 'tex_to_pdf_assets'
        else:
            files['file'] = ('source.tex', open(tex_file, 'rb'))
            endpoint = 'tex_to_pdf'
        url = f'{cls.PROCESSING_SERVER}{f":{cls.PROCESSING_PORT}" if cls.PROCESSING_PORT else ""}/{endpoint}'
        response = requests.post(url=url, files=files)
        if response.ok:
            with (output_directory / f'{tex_file.stem}.pdf').open('wb') as f:
                f.write(response.content)
            return output_directory / f'{tex_file.stem}.pdf'
        else:
            with (output_directory / f'{tex_file.stem}.log').open('wb') as f:
                f.write(response.content)
            return output_directory / f'{tex_file.stem}.log'

    @classmethod
    def md2tex(cls, md_file: Path, output_directory: str = None) -> Path:
        md_file = Path(md_file)
        if not output_directory:
            output_directory = md_file.parent
        else:
            output_directory = Path(output_directory)
        files = {
            'file': ('source.md', open(md_file, 'rb')),
        }
        url = f'{cls.PROCESSING_SERVER}{f":{cls.PROCESSING_PORT}" if cls.PROCESSING_PORT else ""}/md_to_tex'
        response = requests.post(url=url, files=files)
        result_file = output_directory / f'{md_file.stem}.tex'
        with result_file.open('wb') as f:
            f.write(response.content)
        return result_file


if __name__ == '__main__':
    d = NetTools().check_connection()
    print(d)
