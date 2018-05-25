## Project Description

Imagine that this is the early days of Wave's history, and that we are prototyping
a new payroll system with an early partner. Our partner is going to use our web
app to determine how much each employee should be paid in each _pay period_, so
it is critical that we get our numbers right.

The partner in question only pays its employees by the hour (there are no
salaried employees.) Employees belong to one of two _job groups_ which
determine their wages; job group A is paid $20/hr, and job group B is paid
$30/hr. Each employee is identified by a string called an "employee id" that is
globally unique in their system.

Hours are tracked per employee, per day in comma-separated value files (CSV).
Each individual CSV file is known as a "time report", and will contain:

1. A header, denoting the columns in the sheet (`date`, `hours worked`,
   `employee id`, `job group`)
1. 0 or more data rows
1. A footer row where the first cell contains the string `report id`, and the
   second cell contains a unique identifier for this report.

Our partner has guaranteed that:

1. Columns will always be in that order.
1. There will always be data in each column.
1. There will always be a well-formed header line.
1. There will always be a well-formed footer line.

An example input file named `sample.csv` is included in this repo.

### What your web-based application must do:

We've agreed to build the following web-based prototype for our partner.

1. Your app must accept (via a form) a comma separated file with the schema
   described in the previous section.
1. Your app must parse the given file, and store the timekeeping information in
   a relational database for archival reasons.
1. After upload, your application should display a _payroll report_. This
   report should also be accessible to the user without them having to upload a
   file first.
1. If an attempt is made to upload two files with the same report id, the
   second upload should fail with an error message indicating that this is not
   allowed.

The payroll report should be structured as follows:

1. There should be 3 columns in the report: `Employee Id`, `Pay Period`,
   `Amount Paid`
1. A `Pay Period` is a date interval that is roughly biweekly. Each month has
   two pay periods; the _first half_ is from the 1st to the 15th inclusive, and
   the _second half_ is from the 16th to the end of the month, inclusive.
1. Each employee should have a single row in the report for each pay period
   that they have recorded hours worked. The `Amount Paid` should be reported
   as the sum of the hours worked in that pay period multiplied by the hourly
   rate for their job group.
1. If an employee was not paid in a specific pay period, there should not be a
   row for that employee + pay period combination in the report.
1. The report should be sorted in some sensical order (e.g. sorted by employee
   id and then pay period start.)
1. The report should be based on all _of the data_ across _all of the uploaded
   time reports_, for all time.

As an example, a sample file with the following data:

<table>
<tr>
  <th>
    date
  </th>
  <th>
    hours worked
  </th>
  <th>
    employee id
  </th>
  <th>
    job group
  </th>
</tr>
<tr>
  <td>
    4/11/2016
  </td>
  <td>
    10
  </td>
  <td>
    1
  </td>
  <td>
    A
  </td>
</tr>
<tr>
  <td>
    14/11/2016
  </td>
  <td>
    5
  </td>
  <td>
    1
  </td>
  <td>
    A
  </td>
</tr>
<tr>
  <td>
    20/11/2016
  </td>
  <td>
    3
  </td>
  <td>
    2
  </td>
  <td>
    B
  </td>
</tr>
</table>

should produce the following payroll report:

<table>
<tr>
  <th>
    Employee ID
  </th>
  <th>
    Pay Period
  </th>
  <th>
    Amount Paid
  </th>
</tr>
<tr>
  <td>
    1
  </td>
  <td>
    1/11/2016 - 15/11/2016
  </td>
  <td>
    $300.00
  </td>
</tr>
  <td>
    2
  </td>
  <td>
    16/11/2016 - 30/11/2016
  </td>
  <td>
    $90.00
  </td>
</tr>
</table>

Your application should be easy to set up, and should run on either Linux or
Mac OS X. It should not require any non open-source software.

There are many ways that this application could be built; we ask that you build
it in a way that showcases one of your strengths. If you enjoy front-end
development, do something interesting with the interface. If you like
object-oriented design, feel free to dive deeper into the domain model of this
problem. We're happy to tweak the requirements slightly if it helps you show
off one of your strengths.

## Assumption in implementation:

1. Employees don't change job group, and if they do, this payroll system does not validate.
2. Employee IDs are simply used to aggregate payments in a pay period and aren't an identifier per se.

## Instructions to setup:

Please read _SETUP.md_ for set up and testing instructions.

## Notes from author (answers why I'm proud of this work):

### On choice of framework
I chose to use Flask on the backend because I was looking for something light,
but since I understand that this isn't the complete application, I went with something
that's easily extended as well. Flask allows me to cherry-pick what modules I want
included - since I didn't care for rendering presentation code on the backend, I did not
need a template package.

For the frontend, I went with React and no other major libraries - again, needed something
lightweight (bootstrapping with create-react-app is great for prototyping), but easily
extendible with libraries such as react-redux, redux-router, etc.

I made a conscious decision to separate the frontend from the backend since that provides
room for both to grow independently and not get locked into the same development cycle.
Ideally, I would even keep them in separate repos, but for the sake of this challenge, I
kept them together.

### On writing tests
I'm particularly happy with the more-or-less TDD approach I took while building the backend.
Given time constraints, I didn't add functional tests to the frontend, but I'm pretty confident
that I saved a ton of headache debugging bugs on the backend.

Having decent test coverage also enables me to refactor quickly since I like to look at code
organization from multiple angles, and I can quickly validate that I'm not breaking things when
I move them around.

### On using a database ORM and migrations
I knew that I'd be spending a significant amount of extra time getting things set up and 
writing models and reviewing migrations, but I think it's been a good investment. 
With Flask-SQLAlchemy and Flask-Migrate, I'm pretty confident in plugging in different storage
solutions and rebuilding the application in multiple environments.

Havings a database ORM also allowed me to focus on writing business logic and spend less time
worrying about storage/retrieval logic.

## Suggested improvements / backlog (in no particular order)

* Improve frontend test coverage
* Improve CSV validation and error reporting
* Consider if data compilation required for the payroll report can be done at the database level
either through a query or a stored procedure.
* Add pagination to payroll report to make endpoint scalable.
* Add logging and instrumentation
* Write CI/CD pipeline and deployment instructions
* Use MySQL/PostgresSQL instead of sqlite