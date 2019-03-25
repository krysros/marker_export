try:
    from lxml import etree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company


def export(companies):
    root = ET.Element('marker')
    for company in companies:
        if company.upvote_count > 0:
            recommended = 'true'
        else:
            recommended = 'false'
        attrib = {'recommended': recommended,
                  'added': f'{company.added}',
                  'edited': f'{company.edited}'}
        c = ET.SubElement(root, 'company', attrib=attrib)
        name = ET.SubElement(c, 'name')
        name.text = company.name
        city = ET.SubElement(c, 'city')
        city.text = company.city
        voivodeship = ET.SubElement(c, 'voivodeship')
        voivodeship.text = company.voivodeship
        phone = ET.SubElement(c, 'phone')
        phone.text = company.phone
        email = ET.SubElement(c, 'email')
        email.text = company.email
        www = ET.SubElement(c, 'www')
        www.text = company.www
        nip = ET.SubElement(c, 'nip')
        nip.text = company.nip
        regon = ET.SubElement(c, 'regon')
        regon.text = company.regon
        krs = ET.SubElement(c, 'krs')
        krs.text = company.krs
        branches = ET.SubElement(c, 'branches')
        for branch in company.branches:
            b = ET.SubElement(branches, 'branch')
            b.text = branch.name
        people = ET.SubElement(c, 'people')
        for person in company.people:
            p = ET.SubElement(people, 'person')
            fullname = ET.SubElement(p, 'fullname')
            fullname.text = person.fullname
            position = ET.SubElement(p, 'position')
            position.text = person.position
            phone = ET.SubElement(p, 'phone')
            phone.text = person.phone
            email = ET.SubElement(p, 'email')
            email.text = person.email
    ET.ElementTree(root).write('marker.xml', encoding='utf-8')


engine = create_engine('sqlite:///../marker/marker.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

companies = session.query(Company)
export(companies)
print('DONE')
