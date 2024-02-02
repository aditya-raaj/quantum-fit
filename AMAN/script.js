// script.js

// Sample reviews and quotes
const reviews = [
    "Quantum Fit has transformed my health and well-being. Highly recommended! - Jane Smith",
    "Quantum Fit has transformed my health and well-being. Highly recommended -Brock Lesner",
    "I love the variety of exercises and diet plans. Quantum Fit is my go-to fitness platform-Dwayne Johnson",
    "I was too lazy until I found his site.It's Amazing!-John Cena",
    
    
];

const quotes = [
    "I hated every minute of training, but I said, Don't quit. Suffer now and live the rest of your life as a champion.-Muhammad Ali",
        "We are what we repeatedly do. Excellence then is not an act but a habit.- Aristotle",
        "The body achieves what the mind believes.-Napoleon Hill",
        "Exercise should be regarded as tribute to the heart. - Gene Tunney",
        "Most people fail, not because of lack of desire, but, because of lack of commitment. -Vince Lombardi",
        "If something stands between you and your success, move it. Never be denied.-Dwayne (The Rock) Johnson",
        "All progress takes place outside the comfort zone.”– Michael John Bobak",
        "Just believe in yourself. Even if you don't, just pretend that you do and at some point, you will.” - Venus Williams",
];

// Function to update reviews and quotes dynamically
function updateContent() {
    const reviewBox = document.getElementById('reviewBox');
    const quoteBox = document.getElementById('quoteBox');

    // Clear existing content
    reviewBox.innerHTML = '';
    quoteBox.innerHTML = '';

    // Insert new reviews
    reviews.forEach(review => {
        const p = document.createElement('p');
        p.textContent = review;
        reviewBox.appendChild(p);
    });

    // Insert new quotes
    quotes.forEach(quote => {
        const blockquote = document.createElement('blockquote');
        blockquote.innerHTML = `<p>${quote}</p>`;
        quoteBox.appendChild(blockquote);
    });
}

// Call the function to update content when the page loads
window.onload = updateContent;
