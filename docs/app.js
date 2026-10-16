// Register Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

let lessonsData = null;
let currentDayIndex = 0;

async function init() {
    try {
        const response = await fetch('./lessons.json');
        if (!response.ok) throw new Error('Failed to load lessons data');
        lessonsData = await response.json();

        // Determine day from URL or current date
        const urlParams = new URLSearchParams(window.location.search);
        const dayParam = urlParams.get('day');

        if (dayParam && !isNaN(dayParam)) {
            const dayNum = parseInt(dayParam);
            // 1-based index to 0-based index
            currentDayIndex = (dayNum - 1) % lessonsData.lessons.length;
            if (currentDayIndex < 0) currentDayIndex += lessonsData.lessons.length;
        } else {
            currentDayIndex = calculateCurrentDayIndex();
        }

        setupEventListeners();
        renderLesson();
    } catch (error) {
        console.error('Error initializing app:', error);
        document.getElementById('lesson-title').textContent = 'Error loading data. Are you offline?';
    }
}

function calculateCurrentDayIndex() {
    const tz = lessonsData.timezone;
    const startDateStr = lessonsData.start_date;

    // We want the current date in the specified timezone
    // Using Intl.DateTimeFormat is a standard way in JS to handle this
    const options = { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' };
    const formatter = new Intl.DateTimeFormat('en-US', options);

    // formatter returns MM/DD/YYYY
    const dateParts = formatter.formatToParts(new Date());
    const m = dateParts.find(p => p.type === 'month').value;
    const d = dateParts.find(p => p.type === 'day').value;
    const y = dateParts.find(p => p.type === 'year').value;

    const currentDate = new Date(`${y}-${m}-${d}T00:00:00Z`);
    const startDate = new Date(`${startDateStr}T00:00:00Z`);

    // Calculate difference in days
    const diffTime = currentDate - startDate;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return 0;

    return diffDays % lessonsData.lessons.length;
}

function setupEventListeners() {
    document.getElementById('prev-btn').addEventListener('click', () => {
        currentDayIndex = (currentDayIndex - 1 + lessonsData.lessons.length) % lessonsData.lessons.length;
        updateUrlAndRender();
    });

    document.getElementById('next-btn').addEventListener('click', () => {
        currentDayIndex = (currentDayIndex + 1) % lessonsData.lessons.length;
        updateUrlAndRender();
    });
}

function updateUrlAndRender() {
    const lesson = lessonsData.lessons[currentDayIndex];
    const newUrl = `${window.location.pathname}?day=${lesson.day}`;
    window.history.pushState({ path: newUrl }, '', newUrl);
    renderLesson();
}

function renderLesson() {
    if (!lessonsData || !lessonsData.lessons.length) return;

    const lesson = lessonsData.lessons[currentDayIndex];

    document.getElementById('day-display').textContent = `Day ${lesson.day}`;
    document.getElementById('lesson-title').textContent = lesson.title;
    document.getElementById('lesson-summary').textContent = lesson.summary;

    // The script path in lessons.json is like "lessons/01_images.py"
    // In the docs folder, it's served from "assets/lessons/01_images.py"
    const scriptFilename = lesson.script.split('/').pop();
    document.getElementById('code-link').href = `assets/lessons/${scriptFilename}`;

    const figuresContainer = document.getElementById('figures-container');
    figuresContainer.innerHTML = '';

    lesson.figures.forEach(fig => {
        const card = document.createElement('div');
        card.className = 'figure-card';

        const img = document.createElement('img');
        img.src = `assets/${fig}`;
        img.alt = `Figure for ${lesson.title}`;
        img.loading = 'lazy';

        card.appendChild(img);
        figuresContainer.appendChild(card);
    });
}

// Handle browser back/forward buttons
window.addEventListener('popstate', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const dayParam = urlParams.get('day');

    if (dayParam && !isNaN(dayParam)) {
        currentDayIndex = (parseInt(dayParam) - 1) % lessonsData.lessons.length;
    } else {
        currentDayIndex = calculateCurrentDayIndex();
    }
    renderLesson();
});

// Start the app
init();