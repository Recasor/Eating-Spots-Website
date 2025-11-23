function renderCards(tab, search) {
    fetch('/static/main/data/items.json')
        .then(res => res.json())
        .then(products => {
            const container = document.getElementById('cards');
            container.innerHTML = '';
            console.log('render', tab, search);
            let flag = 0;

            products.forEach(product => {
                if ((tab === 'все' || tab === product.type)  && product.title.toLowerCase().includes(search)) {
                    flag = 1;
                    const card = document.createElement('div');
                    card.classList.add('cafes__item-card', 'cafes__card');
                    card.setAttribute('data-type', `${product.type}`);
                    card.innerHTML = `
            <a href="/item?id=${product.id}" class="cafes__card-img"><img src="static/main/${product.img}" alt="Фотография заведения"></a>
                            <div class="cafes__card-content">
                                <a href="/item?id=${product.id}" class="cafes__card-content_title">${product.title}</a>
                                <div class="cafes__card-content_rating">${product.rating} 
                                <span class="cafes__card-content_rating-stars" style="font-size: 12px;"></span></div>
                                <p class="cafes__card-content_description"><span>Время работы: </span>${product.time}
                                </p>
                                <p class="cafes__card-content_description"><span>Адрес: </span>${product.address}
                                </p>
                                <a href="/item?id=${product.id}" class="cafes__card-content_btn">Подробнее</a>
                            </div>
            `;
                    container.appendChild(card);

                    const elRating = card.querySelector('.cafes__card-content_rating-stars'),
                        fullStars = Math.floor(product.rating),
                        halfStar = product.rating % 1 >= 0.5;
                    let starsHTML = '';

                    for (let i = 0; i < fullStars; i++) starsHTML += '<i class="fa-solid fa-star"></i>';
                    if (halfStar) starsHTML += '<i class="fa-solid fa-star-half-stroke"></i>';
                    for (let i = fullStars + halfStar + 1; i <= 5; i++) starsHTML += '<i class="fa-regular fa-star"></i>';

                    elRating.innerHTML = starsHTML;
                }
            });
            if (!flag) {
                container.innerHTML = '<h2 class="empty-title">По вашему запросу не удалось ничего найти</h2>';
            }
        });
}

renderCards('все', '');