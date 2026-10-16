const CACHE_NAME = 'cv-from-scratch-v2d236285';
const URLS_TO_CACHE = [
  './',
  'index.html',
  'style.css',
  'app.js',
  'manifest.webmanifest',
  'lessons.json',
  'icons/icon-192x192.png',
  'icons/icon-512x512.png',
  'assets/lessons/01_images_arrays.py',
  'assets/01_rgb_vs_gray.png',
  'assets/lessons/02_color_spaces.py',
  'assets/02_color_spaces.png',
  'assets/02_segmentation.png',
  'assets/lessons/03_histograms.py',
  'assets/03_histograms.png',
  'assets/lessons/04_convolution.py',
  'assets/04_convolution.png',
  'assets/lessons/05_edge_detection.py',
  'assets/05_sobel.png',
  'assets/05_canny.png',
  'assets/lessons/06_thresholding_morphology.py',
  'assets/06_thresholding.png',
  'assets/06_morphology.png',
  'assets/lessons/07_contours.py',
  'assets/07_contours.png',
  'assets/lessons/08_harris_corners.py',
  'assets/08_harris.png',
  'assets/lessons/09_template_matching.py',
  'assets/09_template.png',
  'assets/lessons/10_hough_transform.py',
  'assets/10_hough_lines.png',
  'assets/10_hough_circles.png',
  'assets/lessons/11_orb_features.py',
  'assets/11_orb.png',
  'assets/lessons/12_hog_svm.py',
  'assets/12_confusion_matrix.png'
];

self.addEventListener('install', event => {
    // Pre-cache all files
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(URLS_TO_CACHE);
            })
            // Force the waiting service worker to become the active service worker
            .then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', event => {
    const cacheAllowlist = [CACHE_NAME];

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheAllowlist.indexOf(cacheName) === -1) {
                        // Delete old caches
                        return caches.delete(cacheName);
                    }
                })
            );
        })
        // Tell the active service worker to take control of the page immediately
        .then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', event => {
    // Cache-first strategy for offline viewing
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return response
                if (response) {
                    return response;
                }

                // Fallback to network
                return fetch(event.request).then(
                    response => {
                        // Check if we received a valid response
                        if(!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // We shouldn't cache dynamically fetched items as they might be from other domains
                        // but if we want to cache everything fetched locally, we could do it here.
                        return response;
                    }
                );
            })
    );
});
