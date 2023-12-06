
const swiper = new Swiper('.swiperFirst', {
  // Optional parameters
  direction: 'horizontal',
  loop: true,
  
  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
  },
  
  autoplay: {
    delay: 5000,
  }
});

const swiper_second = new Swiper(".swiperSecond", {
  direction: 'horizontal',
  loop: true,
  

  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

