# ICT2101-Lightning-MCQWEEN

## Description:
Lightning MCQween is an interactive web portal for primary school students to learn programming logic while controlling their robotic cars.


## Prototype Implementation
### Development Workflow
![Development Workflow](./images/development_workflow.png)

Listed below are all the pages of the web portal for students and Administrator. (How-To documentation)
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

![Student Dashboard](./images/student_dashboard.png)

#### Learning mode
The web portal redirects the student to learningPage.html when "Learning mode" is selected. The "Learning mode" will walk the student through each component
of the page with simple explanations.The student has to click on the explanations to go to the next component to ensure that they have read them.
![Learning Mode](./images/learning.png)

#### Freestyle mode
The web portal redirects the student to freestylePage.html when "Freestyle mode" is selected. The map will be displayed as an empty canvas to give
students the freedom to control their car to go any direction using the available commands.
![Freestyle Mode](./images/freestyle.png)

#### Quiz mode
The web portal redirects the student to quizPage.html when "Quiz mode" is selected. A map will be displayed for students to navigate the car through. The commands submitted
by the student will be validated before sending them out to the car itself.
![Quiz Mode](./images/quiz.png)

### Administrator
#### Profile Dashboard
Only accessible by the Admin where he/she is able to create/edit/delete admin/student accounts. The Profile dashboard will display the following details:
1. studentID
2. email
3. Account Type (0: student, 1: admin)
4. Account Status ( 0: Deactivated, 1: Active)
5. Add Account form with the following data fields:
  - Email, Password, Confirm Password, Account Type
![Profile Dashboard](./images/profile_dashboard.png)

#### Map Dashboard
Only accessible by the Admin where he/she is able to upload new maps which are displayed in "Learning mode" and "Quiz Mode".
![Map Dashboard](./images/map_dashboard.png)

### User Acceptance Testing
<Insert Video link here>
| ID  | Test Case Description | Precondition | Steps | Expected Result | Actual Result | P/F |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| ST1  | Opening the web application  | In Web Browser  | 1. Browse to web application URL 2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P |
| ST2  | Logging into Admin dashboard with valid email and valid password | In Login Page  | 1. Key in valid Admin email<br />2. Key in valid Admin password<br />3. Click the "Login" button<br />4. Observe screen"  | Sees the Profile Dashboard  | Sees the Profile Dashboard  | P |
| ST3  | Logging into Admin dashboard with invalid email and valid password  | In Login Page  | 1. Key in invalid Admin email<br />2. Key in valid Admin password<br />3. Click the "Login" button<br />4. Observe screen"    | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P |
| ST4  | Logging into Admin dashboard with valid email and invalid password  | In Login Page  | 1. Key in valid Admin email<br />2. Key in invalid Admin password<br />3. Click the "Login" button<br />4. Observe screen"    | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P |
| ST5  | Logging into Admin dashboard with invalid email and invalid password  | In Login Page  | 1. Key in invalid Admin email<br />2. Key in invalid Admin password<br />3. Click the "Login" button<br />4. Observe screen"    | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P |
| ST6  | Logging into Admin dashboard with no email and no password  | In Login Page  | 1. Key nothing for Admin email<br />2. Key nothing for Admin password<br />3. Click the "Login" button<br />4. Observe screen"    | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P |
| ST7  | Logging into Student dasboard  | In Login Page  | 1. Key in valid email<br />2. Key in valid password<br />3. Click the "Login" button<br />4. Observe screen  | sees the Student Dashboard  | sees the Student Dashboard  | P |
| ST8  | Logging into Student dashboard with invalid email and valid password  | In Login Page  | 1. Key in invalid email<br />2. Key in valid password<br />3. Click the "Login" button<br />4. Observe screen  | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P  |
| ST9  | Logging into Student dashboard with valid email and invalid password  | In Login Page  | 1. Key in valid email<br />2. Key in invalid password<br />3. Click the "Login" button<br />4. Observe screen  | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P  |
| ST10  | Logging into Student dashboard with invalid email and invalid password  | In Login Page  | 1. Key in invalid email<br />2. Key in invalid password<br />3. Click the "Login" button<br />4. Observe screen  | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P  |
| ST11  | Logging into Student dashboard with no email and no password  | In Login Page  | 1. Key nothing for email<br />2. Key nothing for password<br />3. Click the "Login" button<br />4. Observe screen  | Sees the User Login page with the message "Invalid login"  | Sees the User Login page with the message "Invalid login"  | P  |
| ST12  | Go to Learning Mode Page from Student Dashboard | In Student dashboard  | 1. Click the "Learning Mode" button in the navigation bar<br />2. Observe screen  | Sees the Learning Mode Page  | Sees the Learning Mode Page  | P  |
| ST13  | Go to Freestyle Mode Page from Student Dashboard | In Student dashboard  | 1. Click the "Freestyle Mode" button in the navigation bar<br />2. Observe screen  | Sees the Freestyle Mode Page  | Sees the Freestyle Mode Page  | P  |
| ST14  | Go to Quiz Mode Page from Student Dashboard | In Student dashboard  | 1. Click the "Quiz Mode" button in the navigation bar<br />2. Observe screen  | Sees the Quiz Mode Page  | Sees the Quiz Mode Page  | P  |
| ST15  | Logout from Student Dashboard  | In Student dashboard | 1. Click the "Logout" button in the navigation bar<br />2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P  |
| ST16  | Go to Freestyle Mode Page from Learning Mode Page  | In Learning mode Page  | 1. Click the "Freestyle Mode" button in the navigation bar<br />2. Observe screen  | Sees the Freestyle Mode Page  | Sees the Freestyle Mode Page  | P  |
| ST17  | Go to Quiz Mode Page from Learning Mode Page   | In Learning mode Page  | 1. Click the "Quiz Mode" button in the navigation bar<br />2. Observe screen  | Sees the Quiz Mode Page  | Sees the Quiz Mode Page  | P  |
| ST18  | Go to student dashboard from Learning Mode Page   | In Learning mode Page  | 1. Click the "Dashboard" button in the navigation bar<br />2. Observe screen  | Sees the student dashboard Page  | Sees the student dashboard Page  | P  |
| ST19  | logout from Learning Mode Page   | In Learning mode Page  | 1. Click the "Logout" button in the navigation bar<br />2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P  |
| ST20  | Go to Learning Mode Page from Freestyle Mode Page  | In Freestyle mode Page  | 1. Click the "Learning Mode" button in the navigation bar<br />2. Observe screen  | Sees the Learning Mode Page  | Sees the Learning Mode Page  | P  |
| ST21  | Go to Quiz Mode Page from Freestyle Mode Page  | In Freestyle mode Page  | 1. Click the "Quiz Mode" button in the navigation bar<br />2. Observe screen  | Sees the Quiz Mode Page  | Sees the Quiz Mode Page  | P  |
| ST22  | Go to student dashboard Page from Freestyle Mode Page  | In Freestyle mode Page  | 1. Click the "Dashboard" button in the navigation bar<br />2. Observe screen  | Sees the student dashboard Page  | Sees the student dashboard Page  | P  |
| ST23  | Logout from Freestyle Mode Page  | In Freestyle mode Page  | 1. Click the "Logout" button in the navigation bar<br />2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P  |
| ST24  | Go to Learning Mode Page from Quiz Mode Page  | In Quiz mode Page  | 1. Click the "Learning Mode" button in the navigation bar<br />2. Observe screen  | Sees the Learning Mode Page  | Sees the Learning Mode Page  | P  |
| ST25  | Go to Freestyle Mode Page from Quiz Mode Page  | In Quiz mode Page  | 1. Click the "Freestyle Mode" button in the navigation bar<br />2. Observe screen  | Sees the Freestyle Mode Page  | Sees the Freestyle Mode Page  | P  |
| ST26  | Go to student dashboard Page from Quiz Mode Page  | In Quiz mode Page  | 1. Click the "Dashboard" button in the navigation bar<br />2. Observe screen  | Sees the student dashboard Page  | Sees the student dashboard Page  | P  |
| ST27  | Logout from Quiz Mode Page  | In Quiz mode Page  | 1. Click the "Logout" button in the navigation bar<br />2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P  |
| ST28  | Logout from Profile dashboard  | In Profile dashboard  | 1. Click the "Logout" button in the navigation bar<br />2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P  |
| ST29  | Go to Map dashboard from Profile dashboard  | In Profile dashboard  | 1. Click the "Map Dashboard" button in the navigation bar<br />2. Observe screen  | Sees the Map dashboard Page  | Sees the Map dashboard Page  | P  |
| ST30  | Go to Profile dashboard from Map dashboard  | In Map dashboard  | 1. Click the "Profile Dashboard" button in the navigation bar<br />2. Observe screen  | Sees the Profile dashboard Page  | Sees the Profile dashboard Page  | P  |
| ST31  | Logout from Map dashboard  | In Map dashboard  | 1. Click the "Logout" button in the navigation bar<br />2. Observe screen  | Sees the Login Page  | Sees the Login Page  | P  |

## Whitebox Testing

