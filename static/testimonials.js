// testimonials.js
$(document).ready(function () {
    $('.testimonials-container').owlCarousel({
      loop: true,
      autoplay: true,
      autoplayTimeout: 6000,
      margin: 20,
      nav: true,
      navText: [
        "<i class='fa-solid fa-arrow-left'></i>",
        "<i class='fa-solid fa-arrow-right'></i>"
      ],
      responsive: {
        0: {
          items: 1,
          nav: false
        },
        768: {
          items: 2,
          nav: true
        }
      }
    });
  });
  