import unittest
from indepProject.models import Enrollment, Student, Dataset, Course, db
from indepProject.tools import roundTime
from indepProject.counts import cohort_get_rank_counts
if __name__ != '__main__':
  from indepProject.models import Enrollment, Student, Dataset, Course, db
  from indepProject.tools import roundTime
  from indepProject.counts import cohort_get_rank_counts


class TestCounts(unittest.TestCase):
  def test_dummy_db(self):
    student1 = Student(
          student_id = "6666666",name = "Jimbo Slampson",campus = "FR",program ="BSSWE",
          start_date = "2021-09-01",dataset = roundTime(), prereq_rank = 'FIR',credit_rank  = 'FIR'
      )
    db.session.add(student1)
    db.session.commit()

  def test_count_students_by_rank_cohort(self):
    now=roundTime()
    dataset = Dataset(upload_datetime=now)
    db.session.add(dataset);
    db.session.commit();
    student1 = Student(
        student_number = "3573669",name = "Fletcher Donaldson",campus = "FR",program ="BSSWE",
        start_date = "2021-09-01",dataset = dataset,rank = 'FIR'
    )

    student2 = Student(
        student_number = "4567123",name = "Susie Lee",campus = "FR",program ="BSSWE",
        start_date = "2020-09-01",dataset = dataset,rank = 'SOP'
    )

    student3 = Student(
        student_number = "3617785",name = "Henry MacDonald",campus = "SJ",program ="BSSWE",
        start_date = "2019-09-01",dataset = dataset,rank = 'JUN'
    )

    student4 = Student(
        student_number = "3629987",name = "Felix Johnson",campus = "FR",program ="BSSWE",
        start_date = "2018-01-01",dataset = dataset,rank = 'SEN'
    )

    db.session.add(student1);
    db.session.add(student2);
    db.session.add(student3);
    db.session.add(student4);
    db.session.commit();
    
    course1 = Course(
        course_code = "CS*COOP",name = "CO-OP WORK TERM ",credit_hours = 0.00,
        section = "FR01B",upload_set = dataset
    )

    course2 = Course(
        course_code = "MATH*1503",name = "Linear Algebra",credit_hours = 3.00,
        section = "FR01A",upload_set = dataset
    )

    db.session.add(course1);
    db.session.add(course2);
    db.session.commit();

    enrolment1 = Enrollment(
        student = student1,course = course1,term = "2021/WI",upload_set = dataset,grade="A"
    )

    enrolment2 = Enrollment(
        student = student2,course = course2,term = "2021/WI",upload_set = dataset,grade="A"
    )

    enrolment3 = Enrollment(
        student = student3,course = course2,term = "2021/WI",upload_set = dataset,grade="A"
    )

    enrolment4 = Enrollment(
        student = student4,course = course2,term = "2021/WI",upload_set = dataset,grade="A"
    )

    db.session.add(enrolment1);
    db.session.add(enrolment2);
    db.session.add(enrolment3);
    db.session.add(enrolment4);
    db.session.commit();

    rank_counts = list(cohort_get_rank_counts(now,"2019-2020").values()) # count_students_by_rank returns dictionary
    self.assertTrue(rank_counts == [1,1,1,1])

#   def test_count_students_by_rank_semester(self):
#       from ..counts import count_students_by_rank_cohort
#       dataset = Dataset(upload_datetime=timezone.now())
#       dataset.save()
#       student1 = Student(
#           student_number = "3573669",name = "Fletcher Donaldson",campus = "FR",program ="BSSWE",
#           start_date = "2021-09-01",upload_set = dataset,rank = 'FIR'
#       )

#       student2 = Student(
#           student_number = "4567123",name = "Susie Lee",campus = "FR",program ="BSSWE",
#           start_date = "2021-09-01",upload_set = dataset,rank = 'SOP'
#       )

#       student3 = Student(
#           student_number = "3617785",name = "Henry MacDonald",campus = "SJ",program ="BSSWE",
#           start_date = "2021-09-01",upload_set = dataset,rank = 'JUN'
#       )

#       student4 = Student(
#           student_number = "3629987",name = "Felix Johnson",campus = "FR",program ="BSSWE",
#           start_date = "2021-09-01",upload_set = dataset,rank = 'SEN'
#       )


#       student1.save()
#       student2.save()
#       student3.save()
#       student4.save()

#       rank_counts = list(count_students_by_rank_cohort("2021-2022").values())

#       self.assertTrue(rank_counts == [1,1,1,1])

if __name__ == '__main__':
    unittest.main()

