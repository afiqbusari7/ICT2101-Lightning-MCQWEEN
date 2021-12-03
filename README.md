# ICT2101-Lightning-MCQWEEN

## Description:
Lightning MCQween is an interactive web portal for primary school students to learn programming logic while controlling their robotic cars.


## Prototype Implementation
### Student
#### Student Dashboard:
The student has to login using their accounts (Created by the Administrator). Once logged in, they will be able to see their student dashboard.
The following are the details display:
1. Student ID
2. email
3. Quiz score
4. Tutorial Progress

From the student dashboard, they should be able to select the available modes which will redirect them to the respective pages.
There are 3 Modes Available:
1. Learning mode
2. Freestyle mode
3. Quiz mode

#### Learning mode
The web portal redirects the student to learningPage.html when "Learning mode" is selected. The "Learning mode" will walk the student through each component
of the page with simple explanations.The student has to click on the explanations to go to the next component to ensure that they have read them.

#### Freestyle mode
The web portal redirects the student to freestylePage.html when "Freestyle mode" is selected. The map will be displayed as an empty canvas to give
students the freedom to control their car to go any direction using the available commands.

#### Quiz mode
The web portal redirects the student to quizPage.html when "Quiz mode" is selected. A map will be displayed for students to navigate the car through. The commands submitted
by the student will be validated before sending them out to the car itself.

### Administrator
#### Profile Dashboard
Only accessible by the Admin where he/she is able to create/edit/delete admin/student accounts. The Profile dashboard will display the following details:
1. studentID
2. email
3. Account Type (0: student, 1: admin)
4. Account Status ( 0: Deactivated, 1: Active)
5. Add Account form with the following data fields:
  - Email, Password, Confirm Password, Account Type

#### Map Dashboard
Only accessible by the Admin where he/she is able to upload new maps which are displayed in "Learning mode" and "Quiz Mode".

## Whitebox Testing

