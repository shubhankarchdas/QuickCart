    // Promo navber  

    // Promo Rotation after 2 seconds
    setTimeout(() => {
    const logo = document.getElementById('logoImage');
    const promo = document.getElementById('promoText');

    logo.classList.add('d-none');     // Hide logo
    promo.classList.remove('d-none'); // Show promo
    }, 2000);

    // Optional: Keep rotating messages every few seconds
    const promoMessages = [
    "Fast Delivery 🚚",
    "Best Offers 🛍️",
    "New Arrivals 👗",
    "Trending Now 🔥",
    "Limited Stock ⏳"
    ];

    let currentIndex = 0;
    setInterval(() => {
    const promo = document.getElementById('promoText');
    promo.textContent = promoMessages[currentIndex];
    currentIndex = (currentIndex + 1) % promoMessages.length;
    }, 3000);