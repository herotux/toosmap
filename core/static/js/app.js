const signup = document.getElementById('login')
const boxCity = document.getElementById('box1')
const boxMap = document.getElementById('box-map')
const showCity = document.getElementById('mycol')
const boxDasteBandi = document.getElementById('box2');
const showDasteBandi = document.getElementById('mycol10');

const btnCity = document.getElementById('btn-city');
const btnDaste = document.getElementById('btn-daste');

const mycol1 = document.getElementById('btn-col1');
const btncol11 = document.getElementsByClassName('btn-col11')


const mycol2 = document.getElementById('btn-col2');
const btncol22 = document.getElementsByClassName('btn-col22')


const mycol3 = document.getElementById('btn-col3');
const btncol33 = document.getElementsByClassName('btn-col33')

const mycol4 = document.getElementById('mycol1');
const mycol5 = document.getElementById('mycol2');
const mycol6 = document.getElementById('mycol3');

const iconMycol = document.getElementById('icon-col1')
const iconMycol2 = document.getElementById('icon-col2')
const iconMycol3 = document.getElementById('icon-col3')

const colShow1 = document.getElementsByClassName('col-show1')
const colShow2 = document.getElementsByClassName('col-show2')
const colShow3 = document.getElementsByClassName('col-show3')

const footbal = document.getElementsByClassName('footbal-show')
const volyball = document.getElementsByClassName('volyball-show')
const swim = document.getElementsByClassName('swim-show')

const footbalPC = document.querySelectorAll('#footbal')
const volyballPC = document.querySelectorAll('#volyball')
const swimPC = document.querySelectorAll('#swim')
const showfootbalPC = document.querySelectorAll('#footbal1')
const showvolyballPC = document.querySelectorAll('#volyball1')
const showswimPC = document.querySelectorAll('#swim1')


if (window.outerWidth < 980) {
    boxCity.style.display = 'none'
    boxMap.classList.add('col-12')

} else {
    boxCity.style.display = 'block'
    boxMap.classList.remove('col-12')
}

window.addEventListener('resize', function () {
    if (window.outerWidth < 980) {
        boxCity.style.display = 'none'
        boxMap.classList.add('col-12')

    } else {
        boxCity.style.display = 'block'
        boxMap.classList.remove('col-12')
    }
});

if (window.outerWidth < 980) {
    boxDasteBandi.style.display = 'none'

} else {
    boxDasteBandi.style.display = 'none'
}

window.addEventListener('resize', function () {
    if (window.outerWidth < 980) {
        boxDasteBandi.style.display = 'none'
    } else {
        boxDasteBandi.style.display = 'none'
    }
});


const boxDasteContent = boxDasteBandi.innerHTML;
showDasteBandi.innerHTML += `${boxDasteContent}`
$('#daste').on('click', function () {
    $('#mycol10').addClass('show');
    $('.overlay2').fadeIn();
});

$('.overlay2').on('click', function () {
    $('#mycol10').removeClass('show');
    $(this).fadeOut();
});

$('#btn-close').on('click', function () {
    $('#mycol10').removeClass('show');
    $('.overlay2').fadeOut();
});



const boxCityContent = boxCity.innerHTML;
showCity.innerHTML += `${boxCityContent}`
$('#city').on('click', function () {
    $('#mycol').addClass('show');
    $('.overlay').fadeIn();
});

$('.overlay').on('click', function () {
    $('#mycol').removeClass('show');
    $(this).fadeOut();
});

$('#btn-close').on('click', function () {
    $('#mycol').removeClass('show');
    $('.overlay').fadeOut();
});


showDasteBandi.addEventListener('click', function (event) {
    if (event.target.classList.contains('btn-col1')) {
        if (btncol11[0].classList.contains('fa-caret-down')) {
            btncol11[0].classList.remove('fa-caret-down')
            btncol11[0].classList.add('fa-caret-left')
        } else {
            btncol11[0].classList.add('fa-caret-down')
            btncol11[0].classList.remove('fa-caret-left')

            btncol22[0].classList.remove('fa-caret-down')
            btncol22[0].classList.add('fa-caret-left')

            btncol33[0].classList.remove('fa-caret-down')
            btncol33[0].classList.add('fa-caret-left')

            colShow2[0].classList.remove('show')
            colShow3[0].classList.remove('show')
        }
    }

    if (event.target.classList.contains('btn-col2')) {
        if (btncol22[0].classList.contains('fa-caret-down')) {
            btncol22[0].classList.remove('fa-caret-down')
            btncol22[0].classList.add('fa-caret-left')



        } else {
            btncol22[0].classList.add('fa-caret-down')
            btncol22[0].classList.remove('fa-caret-left')

            btncol11[0].classList.remove('fa-caret-down')
            btncol11[0].classList.add('fa-caret-left')

            btncol33[0].classList.remove('fa-caret-down')
            btncol33[0].classList.add('fa-caret-left')

            colShow3[0].classList.remove('show')
            colShow1[0].classList.remove('show')
        }
    }

    if (event.target.classList.contains('btn-col3')) {
        if (btncol33[0].classList.contains('fa-caret-down')) {
            btncol33[0].classList.remove('fa-caret-down')
            btncol33[0].classList.add('fa-caret-left')

        } else {
            btncol33[0].classList.add('fa-caret-down')
            btncol33[0].classList.remove('fa-caret-left')

            btncol22[0].classList.remove('fa-caret-down')
            btncol22[0].classList.add('fa-caret-left')

            btncol11[0].classList.remove('fa-caret-down')
            btncol11[0].classList.add('fa-caret-left')

            colShow1[0].classList.remove('show')
            colShow2[0].classList.remove('show')
        }
    }


    if (event.target.classList.contains('footbal')) {
        swim[0].classList.remove('show')
        volyball[0].classList.remove('show')
    }

    if (event.target.classList.contains('volyball')) {
        swim[0].classList.remove('show')
        footbal[0].classList.remove('show')
    }

    if (event.target.classList.contains('swim')) {
        footbal[1].classList.remove('show')
        volyball[1].classList.remove('show')
    }


    if (event.target.classList.contains('footbal')) {
        swim[1].classList.remove('show')
        volyball[1].classList.remove('show')
    }

    if (event.target.classList.contains('volyball')) {
        swim[1].classList.remove('show')
        footbal[1].classList.remove('show')
    }

    if (event.target.classList.contains('swim')) {
        footbal[1].classList.remove('show')
        volyball[1].classList.remove('show')
    }


    if (event.target.classList.contains('swim')) {
        footbal[2].classList.remove('show')
        volyball[2].classList.remove('show')
    }


    if (event.target.classList.contains('footbal')) {
        swim[2].classList.remove('show')
        volyball[2].classList.remove('show')
    }

    if (event.target.classList.contains('volyball')) {
        swim[2].classList.remove('show')
        footbal[2].classList.remove('show')
    }

    if (event.target.classList.contains('swim')) {
        footbal[2].classList.remove('show')
        volyball[2].classList.remove('show')
    }
});



btnCity.addEventListener('click', () => {
    document.getElementById('box1').style.display = 'block'
    document.getElementById('box2').style.display = 'none'
    btnCity.classList.add('active')
    btnDaste.classList.remove('active')
})

btnDaste.addEventListener('click', () => {
    document.getElementById('box1').style.display = 'none'
    document.getElementById('box2').style.display = 'block'
    btnCity.classList.remove('active')
    btnDaste.classList.add('active')
})



function closeAllMycols() {
    mycol1.classList.remove('col-active');
    mycol2.classList.remove('col-active');
    mycol3.classList.remove('col-active');
    mycol4.classList.remove('show');
    mycol5.classList.remove('show');
    mycol6.classList.remove('show');
}



mycol1.addEventListener('click', () => {
    if (mycol1.classList.contains('col-active')) {
        closeAllMycols();
        iconMycol.classList.add('fa-caret-left')
        iconMycol.classList.remove('fa-caret-down')
    } else {
        closeAllMycols();
        mycol1.classList.add('col-active');
        mycol4.classList.add('show');

        iconMycol.classList.add('fa-caret-down')
        iconMycol.classList.remove('fa-caret-left')

        iconMycol2.classList.add('fa-caret-left')
        iconMycol2.classList.remove('fa-caret-down')

        iconMycol3.classList.add('fa-caret-left')
        iconMycol3.classList.remove('fa-caret-down')
    }
})

mycol2.addEventListener('click', () => {
    if (mycol2.classList.contains('col-active')) {
        closeAllMycols();
        iconMycol2.classList.add('fa-caret-left')
        iconMycol2.classList.remove('fa-caret-down')

    } else {
        closeAllMycols();
        mycol2.classList.add('col-active');
        mycol5.classList.add('show');

        iconMycol2.classList.add('fa-caret-down')
        iconMycol2.classList.remove('fa-caret-left')

        iconMycol.classList.add('fa-caret-left')
        iconMycol.classList.remove('fa-caret-down')

        iconMycol3.classList.add('fa-caret-left')
        iconMycol3.classList.remove('fa-caret-down')
    }
})

mycol3.addEventListener('click', () => {
    if (mycol3.classList.contains('col-active')) {
        closeAllMycols();
        iconMycol3.classList.add('fa-caret-left')
        iconMycol3.classList.remove('fa-caret-down')
    } else {
        closeAllMycols();
        mycol3.classList.add('col-active');
        mycol6.classList.add('show');

        iconMycol3.classList.add('fa-caret-down')
        iconMycol3.classList.remove('fa-caret-left')

        iconMycol2.classList.add('fa-caret-left')
        iconMycol2.classList.remove('fa-caret-down')

        iconMycol.classList.add('fa-caret-left')
        iconMycol.classList.remove('fa-caret-down')
    }
})

footbalPC[0].addEventListener('click', () => {
    showswimPC[0].classList.remove('show')
    showvolyballPC[0].classList.remove('show')
})

volyballPC[0].addEventListener('click', () => {
    showswimPC[0].classList.remove('show')
    showfootbalPC[0].classList.remove('show')
})

swimPC[0].addEventListener('click', () => {
    showfootbalPC[0].classList.remove('show')
    showvolyballPC[0].classList.remove('show')
})



footbalPC[1].addEventListener('click', () => {
    showswimPC[1].classList.remove('show')
    showvolyballPC[1].classList.remove('show')
})

volyballPC[1].addEventListener('click', () => {
    showswimPC[1].classList.remove('show')
    showfootbalPC[1].classList.remove('show')
})

swimPC[1].addEventListener('click', () => {
    showfootbalPC[1].classList.remove('show')
    showvolyballPC[1].classList.remove('show')
})


footbalPC[2].addEventListener('click', () => {
    showswimPC[2].classList.remove('show')
    showvolyballPC[2].classList.remove('show')
})

volyballPC[2].addEventListener('click', () => {
    showswimPC[2].classList.remove('show')
    showfootbalPC[2].classList.remove('show')
})

swimPC[2].addEventListener('click', () => {
    showfootbalPC[2].classList.remove('show')
    showvolyballPC[2].classList.remove('show')
})




if (window.outerWidth < 700) {
    signup.innerHTML = `<i class="fa fa-user" aria-hidden="true"></i>`
} else {
    signup.innerHTML = `ورود - ثبت نام<i class="fa fa-user me-2" aria-hidden="true"></i>`
}

window.addEventListener('resize', function () {
    if (window.outerWidth < 700) {
        signup.innerHTML = `<i class="fa fa-user " aria-hidden="true"></i>`
    } else {
        signup.innerHTML = `ورود - ثبت نام<i class="fa fa-user me-2" aria-hidden="true"></i>`
    }
});






// مختصات مرزهای ایران
var southWest = L.latLng(25.0, 44.0); // جنوب‌غربی
var northEast = L.latLng(39.0, 63.0); // شمال‌شرقی
var bounds = L.latLngBounds(southWest, northEast);

// ایجاد نقشه و محدود کردن آن به مرزهای ایران
var map = L.map('map', {
    maxBounds: bounds, // محدود کردن نقشه به مرزهای ایران
    maxZoom: 18, // حداکثر سطح زوم
    minZoom: 5 // حداقل سطح زوم
}).setView([32.4279, 53.6880], 6); // مرکز نقشه و سطح زوم اولیه (مختصات مرکز ایران)

// اضافه کردن لایه‌ی نقشه
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// محدود کردن حرکت نقشه به مرزهای ایران
map.setMaxBounds(bounds);

// ایجاد گروه مارکرها
var markers = L.markerClusterGroup();

// دریافت Placeها و Jobهای مستقل از API
Promise.all([
    fetch('/api/places/').then(response => response.json()),
    fetch('/api/independent-jobs/').then(response => response.json())
]).then(([placesData, jobsData]) => {
    // نمایش Placeها
    placesData.features.forEach(place => {
        var marker = L.marker([
            place.geometry.coordinates[1], // عرض جغرافیایی
            place.geometry.coordinates[0]  // طول جغرافیایی
        ]).bindPopup(`<b>${place.properties.name}</b><br>${place.properties.address}`);

        // اضافه کردن رویداد کلیک به مارکر
        marker.on('click', function () {
            // نمایش Jobهای مرتبط با Place
            var jobsList = place.properties.jobs.map(job => 
                `<li>${job.store_name} - ${job.address}</li>`
            ).join('');
            marker.getPopup().setContent(`
                <b>${place.properties.name}</b><br>
                ${place.properties.address}
                <ul>${jobsList}</ul>
            `).openOn(map);
        });

        // اضافه کردن مارکر به نقشه
        markers.addLayer(marker);
    });

    // نمایش Jobهای مستقل
    jobsData.features.forEach(job => {
        var marker = L.marker([
            job.geometry.coordinates[1], // عرض جغرافیایی
            job.geometry.coordinates[0]  // طول جغرافیایی
        ]).bindPopup(`<b>${job.properties.store_name}</b><br>${job.properties.address}`);

        // اضافه کردن مارکر به نقشه
        markers.addLayer(marker);
    });

    // اضافه کردن گروه مارکرها به نقشه
    map.addLayer(markers);
}).catch(error => console.error('Error fetching data:', error));

// اضافه کردن دکمه به نقشه
var mapControl = L.control({ position: 'bottomleft' });
mapControl.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'map-control');
    div.innerHTML = '<button id="my-button"><i class="fa fa-exchange" aria-hidden="true"></i></button>';
    return div;
};
mapControl.addTo(map);