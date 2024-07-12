/**
 * Define Global Variables
 * 
*/
let section = document.querySelectorAll('section')
let frg = document.createDocumentFragment()
let list = document.getElementById('navbar__list')
/**
 * End Global Variables
 * Start Helper Functions
 * 
*/
/*for loop to create list */
for (i = 1; i <= section.length; i++) {
    const listItem = document.createElement('li');
    const anchor = document.createElement('a');
    listItem.appendChild(anchor);
    anchor.textContent = document.getElementById('section' + i).getAttribute('data-nav');
    /*set attribute to <a> to run the CSS style */
    const href = '#section' + [i];
    anchor.setAttribute('href', href);
    anchor.setAttribute('data-nav', href)
    anchor.setAttribute('class', 'menu__link')
    frg.appendChild(listItem);
}
const lastlist = document.createElement('li')
const lastAnchor = document.createElement('a')
lastlist.appendChild(lastAnchor)
lastAnchor.textContent="CalenDent"
lastAnchor.setAttribute('href', "https://www.dentistomarashraf.tech/")
lastAnchor.setAttribute('data-nav', "https://www.dentistomarashraf.tech/")
lastAnchor.setAttribute('class', 'menu__link')
frg.appendChild(lastlist)
/* Create a Hamburger <nav> button when screen less than 600px */
const un = document.createElement('a');
un.setAttribute('href', "javascript:void(0)");
un.setAttribute('class', 'menu__link icon');//add class menu__link to aplly the style for the button
un.setAttribute('onclick', 'myFunction()')
let ine = document.createElement('i')
ine.setAttribute('class', 'fa fa-bars')
un.appendChild(ine)
frg.appendChild(un)
/*connect the new HTML fragment to <UL>*/
list.appendChild(frg);


/* Nav button function */
function myFunction() {
    var x = document.getElementById('navbar__list')
    if (x.className === 'navbar__list') {
        x.className += ' responsive'
    } else {
        x.className = 'navbar__list'
    }
}
/*that class added for the first section for apllying the intersectionHandelar down there */

var acti = document.getElementsByTagName('a');
acti[0].classList.add('active');

/*create intersectionObserver to scroll and change the style of container */
const options = {
    threshold: 0.3 //due to media only observe about 30% of the container
};
let observer = new IntersectionObserver(function (entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            intersectionHandelar(entry);
        } else {
            entry.target.classList.remove('your-active-class')
        }
    })
}, options);

//observer for each container
section.forEach(section => {
    observer.observe(section);
});

//helper function for intersectionObserver
function intersectionHandelar(entry) {
    const id = entry.target.id;
    const currentActive = document.querySelector('nav li .active');
    const shouldBeActive = document.querySelector('nav li [data-nav=\"#' + id + '\"]')
    entry.target.classList.add('your-active-class')
    if (currentActive) {
        currentActive.classList.remove('active')
    }
    if (shouldBeActive) {
        shouldBeActive.classList.add('active')
    }
}

/*clicking to navBar listItem to scroll smothly */
list.addEventListener('click', function (scrToSec) {
    /*previnting jumping to Anchor <a> = #section [i] immediatly*/
    scrToSec.preventDefault();
    const all_list = list.querySelectorAll('li')
    if (scrToSec.target == all_list[all_list.length - 1].children[0]){
        window.location.href = scrToSec.target.getAttribute("href")
        return
    }
    if (scrToSec.target.dataset.nav) {
        document
            .querySelector(`${scrToSec.target.dataset.nav}`)
            .scrollIntoView({ behavior: "smooth" });
    }
}
)
