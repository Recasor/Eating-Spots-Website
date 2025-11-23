const pageID = new URLSearchParams(window.location.search).get('id');

async function renderItemPage() {
    const res = await fetch('/static/main/data/items.json'),
        cafes = await res.json(),
        cafe = cafes.find(r => r.id == pageID);
    document.title = cafe.title;

    return cafe;
}

renderItemPage().then(cafe => {
    console.log(cafe);

    window.renderCards = function (tabActive, searchText) {
        console.log('render', tabActive, searchText);
        const menu = document.getElementById('menu');
        menu.innerHTML = '';
        if (cafe.menu[tabActive]) {
            cafe.menu[tabActive].forEach(i => {
                const item = document.createElement('div');
                item.classList.add('menu__content-card', 'menu__card');
                item.innerHTML = `
            <img src="static/main/${i.photo}" alt="Фотография блюда">
            <h3>${i.name}</h3>
            <div><p>${i.weight}</p>
            <p>${i.price}</p></div>
            `
                menu.appendChild(item);
            });
        } else {
            menu.innerHTML = `<h3 class="empty-title">В заведении нет блюд такой категории<h3>`
        }
    }

    renderCards('салаты', '')
    document.querySelector('.promo__title').innerText = cafe.title;
    document.querySelector('.promo__rating').innerText = cafe.rating;
    document.querySelector('.promo__rating').append(document.createElement('span'));
    const elRating = document.querySelectorAll('.star-rating span'),
        fullStars = Math.floor(cafe.rating),
        halfStar = cafe.rating % 1 >= 0.5;
    let starsHTML = '';

    for (let i = 0; i < fullStars; i++) starsHTML += '<i class="fa-solid fa-star"></i>';
    if (halfStar) starsHTML += '<i class="fa-solid fa-star-half-stroke"></i>';
    for (let i = fullStars + halfStar + 1; i <= 5; i++) starsHTML += '<i class="fa-regular fa-star"></i>';

    elRating.forEach(el => {
        el.innerHTML = starsHTML;
    });
    cafe.gallery.forEach(imgSrc => {
        const img = document.createElement('img');
        img.src = imgSrc;
        img.alt = 'Фото заведения';
        img.classList.add('promo__gallery-item');

        document.querySelector('.promo__gallery').appendChild(img);
    });

    document.querySelector('.about__text').innerText = cafe.description;
    document.querySelector('.location__map').innerHTML = cafe.mapUrl;
    document.querySelector('.location__info .phone span').innerText = cafe.phone;
    document.querySelector('.location__info .phone').href = `tel:${cafe.phoneLink}`;
    document.querySelector('.location__info .map span').innerText = cafe.address;
    document.querySelector('.location__info .map').href = cafe.mapLink;

    document.querySelector('.reviews__left-title').innerText = cafe.rating;
    const reviewDescription = document.querySelector('.reviews__left-description');

    // Расчёт текстовой оценки
    switch (true) {
        case cafe.rating <= 2:
            reviewDescription.innerText = 'Плохо';
            break;
        case cafe.rating <= 3:
            reviewDescription.innerText = 'Нормально';
            break;
        case cafe.rating <= 4:
            reviewDescription.innerText = 'Хорошо';
            break;
        case cafe.rating <= 5:
            reviewDescription.innerText = 'Очень хорошо';
    }

    const foodPercent = document.getElementById('foodPercent'),
        staffPercent = document.getElementById('staffPercent'),
        purityPercent = document.getElementById('purityPercent');

    foodPercent.querySelector('.percent').innerText = cafe.foodRating;
    foodPercent.querySelector('.filled').style.width = cafe.foodRating;
    staffPercent.querySelector('.percent').innerText = cafe.staffRating;
    staffPercent.querySelector('.filled').style.width = cafe.staffRating;
    purityPercent.querySelector('.percent').innerText = cafe.purityRating;
    purityPercent.querySelector('.filled').style.width = cafe.purityRating;

    // ------------Обработка отзыва----------------
    const stars = document.querySelectorAll('.reviews__form-stars i');

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const value = star.getAttribute('data-value');
            stars.forEach(s => {
                s.classList.remove('fa-solid', 'active');
                s.classList.add('fa-regular');
            });

            for (let i = 0; i < value; i++) {
                stars[i].classList.remove('fa-regular');
                stars[i].classList.add('fa-solid', 'active');
            }

            document.getElementById('reviewRatingValue').value = value;
        });
    });

    document.getElementById('reviewsForm').addEventListener('submit', (e) => {
        if (document.querySelector('.reviews__form-stars .active')) {
            e.preventDefault();
            const data = new FormData(e.target);
            // !!!!!!!Данные из формы!!!!!!!!
            const reviewRatingValue = data.get('reviewRatingValue'),
                reviewsText = data.get('reviewsText');
            console.log(reviewRatingValue, reviewsText);

            document.getElementById('reviewsForm').reset();
            document.getElementById('reviewRatingValue').value = '';
            stars.forEach(s => {
                s.classList.remove('fa-solid', 'active');
                s.classList.add('fa-regular');
            });
            alert('Отзыв успешно отправлен. Спасибо!')
        } else {
            alert('Поставьте оценку заведению для отправки отзыва');
        }
    });

//     --------------------------------------

    const readyReviews = document.querySelector('.reviews__items');
    if (cafe.readyReviews) {
        cafe.readyReviews.forEach(i => {
            const item = document.createElement('div');
            item.classList.add('reviews__items-card');
            item.innerHTML = `<div class="reviews__items-card_top">
                                <h5 class="reviews__items-card_name">${i.author}</h5>
                                <div class="reviews__items-card_rating star-rating review-star-rating"><span></span></div>
                            </div>
                            <p class="reviews__items-card_text">${i.text}</p>`
            readyReviews.appendChild(item);
            const revRating = item.querySelector('.review-star-rating span'),
                fullStars = i.rating;
            let starsHTML = '';

            for (let i = 0; i < fullStars; i++) starsHTML += '<i class="fa-solid fa-star"></i>';
            for (let i = fullStars + 1; i <= 5; i++) starsHTML += '<i class="fa-regular fa-star"></i>';
            revRating.innerHTML = starsHTML;
        });
    } else {
        readyReviews.innerHTML = `<h3 class="empty-title">Отзывов на данное заведение пока нет<h3>`
    }
});