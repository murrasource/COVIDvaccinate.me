var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline_view/',
    '/static/dino/dino.css',
    '/static/dino/dino.js',
    '/static/dino/images/small_covid_dino.png',
    '/static/dino/images/covid_dino.png',
    '/static/dino/sounds/button-press.mp3',
    '/static/dino/sounds/hit.mp3',
    '/static/dino/sounds/score-reached.mp3',
    '/static/css/django-pwa-app.css',
    '/static/assets/img/favicon.svg',
    '/static/assets/img/vaccine_apple.png',
    '/static/images/splash/iphone5_splash.png',
    '/static/images/splash/iphone6_splash.png',
    '/static/images/splash/iphoneplus_splash.png',
    '/static/images/splash/iphonex_splash.png',
    '/static/images/splash/iphonexr_splash.png',
    '/static/images/splash/iphonexsmax_splash.png',
    '/static/images/splash/ipad_splash.png',
    '/static/images/splash/ipadpro1_splash.png',
    '/static/images/splash/ipadpro2_splash.png',
    '/static/images/splash/ipadpro3_splash.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline_view/');
            })
    )
});
