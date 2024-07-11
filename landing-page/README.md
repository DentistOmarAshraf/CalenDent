# Landing Page Project

### Table of Contents

css
- styles.css    
index.html
js
- app.js
README.md

## Instructions

-this code is written by 'Visual Studio Code'
# Use Google Chrome to run Index.html
# its All features are usable across any Screen.

## Description

landing page with responsive layout and responsive NavBar
navBar was created dynamiclly with JavaScript

# app.JS ===>
### line 14 to 25

for loop that Create list Item and append anchor >> to navigate to the wanted section
all section even if there is a new one will be linked to nav bar and and dynmaclly create a new button inside a bar

### line 27 to 36 

Load an icon library to show a hamburger menu (bars) on small screens
disabled when screen width is more than 500px at line <96> in CSS
Enabled when Screen width is less than 500px at line <129> in CSS

note:
if you want the hamburger button become smaller
remove (menu__link ) from line #29. and you can create your style.

### line 40 to 47 

Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon 

### line 54 to 70

Creating InterSectionObserver >> observe each section
use (isIntersecting) condation will result data : boolean (true or fulse)

### line 73 to 84

Helper Function (intersectionHandeler) >>
if condation
if the section is at veiw port >> add an active state to the nav Button
if its not remove it and add it to onther button

### line 87 to 96

When clicking an item from the navigation menu, the link should scroll to the appropriate section
preventing defult from jumping to the section
scroll down there smoothly
_____________________________________________________________________

# styles.css ==>
### line 127 to 145

Update==>
NavBar style + responsive style in small screen 


## note :
i went to online resourses to understand the InterSectionObserver
this was my resource:
https://css-tricks.com/a-few-functional-uses-for-intersection-observer-to-know-when-an-element-is-in-view/
https://www.youtube.com/watch?v=2IbRtjez6ag&t=335s
https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API