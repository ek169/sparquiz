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
        s6 = School(name="Johnson and Wales", state="RI", classes=[])
        s6.put()
        s7 = School(name="Roger William University", state="RI", classes=[])
        s7.put()
        s8 = School(name="Brown University", state="RI", classes=[])
        s8.put()
        s9 = School(name="Bryant University", state="RI", classes=[])
        s9.put()