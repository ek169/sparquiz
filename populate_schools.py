from models import School


def pop_schools():
    schools = School.all()
    try:
        first_school = schools[0].name
        return None
    except IndexError:
        s1 = School(name="University of Rhode Island", state="RI", classes=[])
        s1.put()
        s2 = School(name="University of Massachusetts", state="MA", classes=[])
        s2.put()
        s3 = School(name="CCRI", state="RI", classes=[])
        s3.put()
        s4 = School(name="Penn State University", state="PA", classes=[])
        s4.put()
        s5 = School(name="New York University", state="NY", classes=[])
        s5.put()