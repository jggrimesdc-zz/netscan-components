import boto3
import datetime
import pandas as pd
import time
from datetime import date

from base_worker import BaseWorker


class ReadToolPKGBLD(BaseWorker):
    '''
    Class specifically for the breach jl files (json list) 
    '''

    def __init__(self, source, label, file, config, df=None):
        self.source = source
        self.label = label
        self.file = file
        self.s3_client = config.s3_client
        self.s3_resource = config.s3_resource
        self.bucket = self.s3_resource.Bucket(config.bucket)
        self.prefix = f"raw/{self.source}/{self.label}-{date.today()}/"
        self.df = pd.DataFrame()

    def get_pkgblds_from_s3(self):
        # save all blackarch tools to a list
        df_list = []

        index_val = 0
        for my_bucket_object in self.bucket.objects.filter(Prefix=self.prefix).all():
            obj_key = my_bucket_object.key

            tool_name = obj_key.split(self.prefix)[1].split('/')[0]
            print(obj_key)

            if obj_key.split('/')[-1] == 'PKGBUILD':
                # initialize all potential data fields
                name = tool_name
                category = []
                desc = ''
                package_url = ''
                license = ''
                pkgver = ''
                pkgrel = ''
                arch = []
                depends = []
                dlagents = []
                sha512 = []
                source_of_tool = 'blackarch'

                max_list_len = 0

                obj = my_bucket_object.get()
                obj_content = obj['Body'].read().decode('utf-8')

                for line in obj_content.split('\n'):
                    if line[:7] == 'groups=':
                        cat_str = line[7:]
                        cat_str = cat_str.strip()
                        cat_str = cat_str.strip('(')
                        cat_str = cat_str.strip(')')

                        cat_list = cat_str.split('\' \'')

                        count = 1
                        for cat in cat_list:
                            category.append(cat.replace('\'', ''))
                            count += 1

                    if line[:8] == 'pkgdesc=':
                        desc = line[8:].strip().strip('\'')
                    if line[:4] == 'url=':
                        homepage = line[4:].strip().strip('(').strip(')').strip('\'')
                    if line[:8] == 'license=':
                        license = line[8:].strip().strip('(').strip(')').strip('\'')
                    if line[:7] == 'pkgver=':
                        pkgver = line[7:].strip()
                    if line[:7] == 'pkgrel=':
                        pkgrel = line[7:].strip()
                    if line[:5] == 'arch=':
                        arch_str = line[5:]

                        arch_str = arch_str.strip()
                        arch_str = arch_str.strip('(')
                        arch_str = arch_str.strip(')')

                        arch_list = arch_str.split('\' \'')

                        count = 1
                        for arch_var in arch_list:
                            arch.append(arch_var.replace('\'', ''))
                            count += 1

                    if line[:8] == 'depends=':
                        depends_str = line[8:]

                        depends_str = depends_str.strip()
                        depends_str = depends_str.strip('(')
                        depends_str = depends_str.strip(')')

                        depends_list = depends_str.split('\' \'')

                        count = 1
                        for depends_var in depends_list:
                            depends.append(depends_var.replace('\'', ''))
                            count += 1

                    if line[:9] == 'DLAGENTS=':
                        d_str = line[9:]
                        d_str = d_str.strip()
                        d_str = d_str.strip('(')
                        d_str = d_str.strip(')')

                        d_list = d_str.split('\' \'')

                        count = 1
                        for d_var in d_list:
                            dlagents.append(d_var.replace('\'', ''))
                            count += 1

                    if line[:11] == 'sha512sums=':
                        s_str = line[11:]
                        s_str = s_str.strip()
                        s_str = s_str.strip('(')
                        s_str = s_str.strip(')')

                        s_list = s_str.split('\' \'')

                        count = 1
                        for s_var in s_list:
                            sha512.append(s_var.replace('\'', ''))
                            count += 1

                df_list.append(
                    pd.DataFrame(
                        data={
                            # 'id':[index_val],
                            'name': [name],
                            'category': [category],
                            'description': desc,
                            'package_url': package_url,
                            'author': '',
                            'license': license,
                            'package_version': pkgver,
                            'package_release': pkgrel,
                            'arch': [arch],
                            'depends': [depends],
                            'dlagents': [dlagents],
                            'sha512sums': [sha512],
                            'source_of_tool': source_of_tool,
                            'last_updated': str(date.today())
                        }
                    )
                )
                index_val += 1

        self.df = pd.concat(df_list)
        print("df concat'd at " + time.strftime("%H:%M:%S", time.localtime()))
        print(self.df.info())
        print(self.df.head())

    def run_all(self):
        self.get_pkgblds_from_s3()
        return self.df
