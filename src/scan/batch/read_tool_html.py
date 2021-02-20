import boto3
import datetime
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from datetime import date

from base_worker import BaseWorker


class ReadToolHTML(BaseWorker):
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
        # save all kali tools to a list
        df_list = []

        for my_bucket_object in self.bucket.objects.filter(Prefix=self.prefix).all():
            # initialize all default values
            name = ''
            category = []
            desc = ''
            package_url = ''
            author = ''
            license = ''
            pkgver = ''
            pkgrel = ''
            arch = []
            depends = []
            dlagents = []
            sha512 = []
            source_of_tool = 'kali'

            obj = my_bucket_object.get()
            record_data = obj['Body'].read().decode('utf-8')
            record_soup = BeautifulSoup(record_data, 'html.parser')

            # get the url and parse out name and type (category) from it
            url_tag = record_soup.find("link", {"rel": "canonical"})
            link = url_tag.attrs['href']
            name = link.split('/')[-1]
            tool_type = link.split('/')[-2].replace('-', ' ')

            # add the type to the category list
            category.append(tool_type)

            # get description
            title = record_soup.find('h2')

            if title is None:
                title = record_soup.find('h3')

            desc_tag = title.next_sibling
            if desc_tag is not None:
                while desc_tag.name != 'p':
                    desc_tag = desc_tag.next_sibling

                    if desc_tag is None:
                        break
                if desc_tag is not None:
                    desc = desc_tag.get_text()

            # get package url (kali repo url)
            kali_repo_url = ''
            for a_tag in record_soup.find_all('a'):
                if re.search(r"^Kali .+ Repo$", a_tag.get_text()) is not None:
                    if a_tag.attrs is not None and 'href' in a_tag.attrs:
                        kali_repo_url = a_tag.attrs['href']
            package_url = kali_repo_url

            # get author and license
            for li_tag in record_soup.find_all('li'):
                if re.search(r"^Author: ", li_tag.get_text()) is not None:
                    author = li_tag.get_text().replace('Author: ', '').strip()

                if re.search(r"^License: ", li_tag.get_text()) is not None:
                    license = li_tag.get_text().replace('License: ', '').strip()

            df_list.append(
                pd.DataFrame(
                    data={
                        'name': [name],
                        'category': [category],
                        'description': desc,
                        'package_url': package_url,
                        'author': author,
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

        self.df = pd.concat(df_list)
        print("df concat'd at " + time.strftime("%H:%M:%S", time.localtime()))
        print(self.df.info())
        print(self.df.head())

    def run_all(self):
        self.get_pkgblds_from_s3()
        return self.df
