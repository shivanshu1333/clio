# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

import csv
import os
from app import app
from datetime import datetime
from specification import *
from models import *
from tqdm import tqdm
import sys


def populate_license(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'license-info.csv'))
    sizecounter=0
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        size = os.stat(path).st_size
        for i in read_csv:
        	sizecounter += sys.getsizeof(i)
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        size = os.stat(path).st_size
        with tqdm(total=sizecounter,unit_scale=True, unit_divisor=128, unit='B') as pbar:
        	for row in (read_csv):
        	    full_name = row[0]
        	    identifier = row[1]
        	    if(row[2] == 'FSF Libre'):
        	        fsf_free_libre = True
        	    else:
        	        fsf_free_libre = False
        	    if(row[3] == 'OSI Approved'):
        	        osi_approved = True
        	    else:
        	        osi_approved = False
        	    license_category = row[4]
        	    license_text = row[5]
        	    l = License(full_name, identifier, fsf_free_libre,
        	                osi_approved, license_category, license_text)
        	    buf = sys.getsizeof(row)
        	    db.session.add(l)
        	    db.session.commit()
        	    pbar.set_postfix()
        	    pbar.update(buf)	


def populate_component(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'component-info.csv'))

    sizecounter=0
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        size = os.stat(path).st_size
        for i in read_csv:
        	sizecounter += sys.getsizeof(i)

    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        with tqdm(total=sizecounter, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for row in tqdm(read_csv):
                name = row[0]
                version = row[1]
                created_by = row[2]
                pub_date = row[3]
                if(pub_date):
                    pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
                else:
                    pub_date = None
                origin = row[4]
                source_url = row[5]
                license_expression = row[6]
                ext_link = row[7]
                c = Component(name, version, created_by, pub_date,
                              origin, source_url, license_expression, ext_link)

                buf = sys.getsizeof(row)
                db.session.add(c)
                db.session.commit()
                pbar.set_postfix()
                pbar.update(buf)


def populate_component_conn(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'component-relationship.csv'))
    sizecounter=0
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        size = os.stat(path).st_size
        for i in read_csv:
        	sizecounter += sys.getsizeof(i)
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        with tqdm(total=sizecounter, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        	for row in read_csv:
        	    if(row[1] in valid_relationship):
        	        input_c1_name = row[0]
        	        c1 = Component.query.filter_by(name=input_c1_name).first()
        	        input_c2_name = row[2]
        	        c2 = Component.query.filter_by(name=input_c2_name).first()
        	        c1.component.append(c2)
        	        buf = sys.getsizeof(row)
        	        pbar.set_postfix()
                	pbar.update(buf)
        	db.session.commit()

def populate_product(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'product-info.csv'))
    sizecounter=0
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        size = os.stat(path).st_size
        for i in read_csv:
        	sizecounter += sys.getsizeof(i)
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        with tqdm(total=sizecounter, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for row in tqdm(read_csv):
                name = row[0]
                version = row[1]
                owner = row[2]
                approver = row[3]
                approval_date = row[4]
                approval_date = datetime.strptime(approval_date, '%Y-%m-%d')
                license_identifier = row[5]
                l = License.query.filter_by(identifier=license_identifier).first()
                p = Product(name, version, owner, approver, approval_date)
                p.license = l
                buf = sys.getsizeof(row)
                db.session.add(p)
                db.session.commit()
                pbar.set_postfix()
                pbar.update(buf)

def populate_product_component_conn(directory):
    path = os.path.join(os.getcwd(), os.path.join(
        directory, 'product-component-relationship.csv'))
    sizecounter=0
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        size = os.stat(path).st_size
        for i in read_csv:
        	sizecounter += sys.getsizeof(i)
    with open(path, 'r', encoding='utf-8') as input_file:
        read_csv = csv.reader(input_file, delimiter=',')
        with tqdm(total=sizecounter, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        	for row in (read_csv):
        	    if(row[1] in valid_relationship):
        	        product_info = row[0].split('-')
        	        p = Product.query.filter_by(
        	            name=product_info[0], version=product_info[1]).first()
        	        relation = row[1]
        	        component_info = row[2].split('-')
        	        c = Component.query.filter_by(
        	            name=component_info[0], version=component_info[1]).first()
        	        modification = row[3]
        	        if(modification == 'MODIFIED'):
        	            modification = True
        	        else:
        	            modification = False
        	        delivery = row[4]
        	        product_component_conn = Product_Component_conn(
        	            p, c, relation, modification, delivery)
        	        buf = sys.getsizeof(row)
        	        db.session.add(product_component_conn)
        	        db.session.commit()
        	        pbar.set_postfix()
                	pbar.update(buf)


if __name__ == '__main__':
    # Recreate DB
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()

        directory = 'dataset'
        print("-> 5 processes will run.")
        populate_license(directory)
        populate_component(directory)
        populate_component_conn(directory)
        populate_product(directory)
        populate_product_component_conn(directory)
