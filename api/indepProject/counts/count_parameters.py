from indepProject.models import Student, Enrollment

# Function to get the data to fill dropdowns for count range selection
def get_count_range_parameters():
  cohorts = []
  semesters = []

  start_dates = Student.query.with_entities(Student.start_date).distinct()
  for date in start_dates:
    start_date = date["start_date"][0:len(date["start_date"])-3]
    year = start_date[:4]
    month = start_date[5:]

    # If a student starts in sept then they are a part of the
    # currentYear-nextYear cohort
    # If a student starts in the winter or summer term, then they are
    # a part of the previousYear-currentYear cohort
    cohort = []
    if int(month) == 9:
      cohort = [year, "-", str(int(year) + 1)]
    else:
      cohort = [str(int(year) - 1), "-", year]

    cohorts.append("".join(cohort))

  # Remove dupliactes and sort list
  cohorts = list(dict.fromkeys(cohorts))
  cohorts.sort(reverse=True)

  enrollment_terms = Enrollment.query.with_entities(Enrollment.term).distinct()
  for term in enrollment_terms:
    semester = term["term"]
    semesters.append(semester)

  semesters.sort(reverse=True)
  semesters = semesters[1:]  # THIS IS TO REMOVE A STUPID WEIRD T AT THE FRONT

  return {"cohorts": cohorts, "semesters": semesters}